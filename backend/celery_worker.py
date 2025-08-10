import os
import asyncio
from celery import Celery
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from datetime import datetime
import logging
from bson import ObjectId

# Import your services
from services import scraper, summarize, tts, send_email

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")

celery = Celery('worker', broker=REDIS_URI, backend=REDIS_URI)

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.read2speech

redis_client = redis.from_url(REDIS_URI)

logging.basicConfig(level=logging.INFO)


@celery.task
def run_worker():
    asyncio.run(main_loop())


async def main_loop():
    group_name = "read2speech_group"
    consumer_name = "worker1"

    try:
        await redis_client.xgroup_create("tasks_stream", group_name, id="$", mkstream=True)
    except Exception:
        pass

    while True:
        resp = await redis_client.xreadgroup(group_name, consumer_name, {"tasks_stream": ">"}, count=1, block=5000)
        if not resp:
            continue

        for stream_name, messages in resp:
            for message_id, message in messages:
                task_id = message.get(b"task_id").decode()
                username = message.get(b"username").decode()
                link = message.get(b"link").decode()

                logging.info(f"Processing task {task_id} for user {username} link: {link}")

                await db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"status": "processing"}})

                # 1. Scrape the article using your scraper service (blocking call, run in threadpool)
                try:
                    article_text = await asyncio.to_thread(scraper.scrape_text_from_url, link)
                except Exception as e:
                    logging.error(f"Scraping failed: {e}")
                    article_text = ""

                if not article_text:
                    await db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"status": "failed"}})
                    await redis_client.xack("tasks_stream", group_name, message_id)
                    continue

                # 2. Summarize the article text (blocking, run in threadpool)
                try:
                    summary_text = await asyncio.to_thread(summarize.generate_response, article_text)
                except Exception as e:
                    logging.error(f"Summarization failed: {e}")
                    summary_text = article_text  # fallback to raw text

                # 3. Generate speech audio file from summary using tts service (blocking, run in threadpool)
                output_path = f"./audiobooks/{task_id}.mp3"
                try:
                    await asyncio.to_thread(tts.text_to_speech, summary_text, output_path)
                    success = True
                except Exception as e:
                    logging.error(f"TTS failed: {e}")
                    success = False

                # 4. Update DB task status accordingly
                if success:
                    await db.tasks.update_one(
                        {"_id": ObjectId(task_id)},
                        {
                            "$set": {
                                "status": "completed",
                                "completed_at": datetime.utcnow(),
                                "output_file": output_path,
                            }
                        },
                    )
                else:
                    await db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"status": "failed"}})

                # 5. Send notification email to user (run in threadpool)
                user = await db.users.find_one({"username": username})
                if user and "email" in user:
                    email_body = (
                        f"Hello {username},\n\nYour audiobook for the article {link} is ready.\n\n"
                        "You can download it from the app."
                    )
                    try:
                        await asyncio.to_thread(
                            send_email.send_mails,
                            email_body,
                            [user["email"]],
                        )
                        logging.info(f"Email sent to {user['email']}")
                    except Exception as e:
                        logging.error(f"Email sending failed: {e}")

                # 6. Acknowledge the Redis stream message
                await redis_client.xack("tasks_stream", group_name, message_id)
