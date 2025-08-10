
# Read2Speech

Read2Speech is a web application that converts articles from URLs into audiobooks using a modern asynchronous backend pipeline. It leverages Redis Streams, Celery, MongoDB, and a powerful LLM-based text-to-speech system to provide fast and scalable audiobook generation, with email notifications when the audiobook is ready.

---

## Features

- User authentication with hashed passwords stored securely in MongoDB.
- JWT-based authentication for secure API access.
- Asynchronous task processing with Redis Streams and Celery workers.
- Article scraping, LLM-powered text-to-speech conversion, and audiobook generation (.mp3).
- Task status tracking with MongoDB for real-time frontend updates.
- Email notification system to inform users when their audiobook is ready.

---

## Architecture Overview

### Redis Streams

Redis Streams is used as a high-performance message queue to handle incoming user requests. It supports ordered message storage, consumer groups for scaling, and persistence. When a user submits an article link, the backend pushes a message into a Redis stream that Celery workers consume for processing.

### Celery

Celery is a distributed task queue system that processes background jobs asynchronously. Celery workers listen to the Redis stream, scrape the article, run it through the LLM text-to-speech pipeline, generate an audiobook, save the file, and trigger email notifications — all without blocking the main API.

### MongoDB

MongoDB stores two main collections:

- **Users collection**: Stores user credentials with hashed passwords and supports JWT authentication.
- **Tasks collection**: Tracks each audiobook generation task, including status (`pending`, `processing`, `completed`, or `failed`), timestamps, and output file paths.

MongoDB’s flexible, JSON-like schema allows easy updates and additions of new fields without complex migrations.

---

## Data Flow and Workflow

1. User logs in or signs up (password stored securely as a hash in MongoDB).
2. JWT token is issued containing the username and verified on protected routes.
3. User submits an article URL for conversion.
4. Backend creates a new task entry in MongoDB with status `pending`.
5. The URL and task info is pushed into a Redis stream.
6. Celery workers consume tasks from the stream and:
   - Update task status to `processing`.
   - Scrape the article content.
   - Generate audiobook using an LLM-based text-to-speech pipeline.
   - Save the audiobook locally and update task status to `completed` with output file path.
   - Send an email notification via Google SMTP to the user.
7. Frontend polls the API to get updated task status and displays it to the user.

---

## MongoDB Schemas

### User Collection (`users`)

```json
{
  "_id": ObjectId(),
  "username": "john_doe",
  "password_hash": "hashed_password_here",
  "email": "john@example.com",
  "created_at": ISODate("2025-08-10T12:00:00Z")
}
````

* Passwords are stored as hashes (never plain text).
* Used for JWT authentication (token contains `username` or `user_id` as payload).

### Task Collection (`tasks`)

```json
{
  "_id": ObjectId(),
  "username": "john_doe",
  "link": "https://example.com/article",
  "status": "pending",  // pending, processing, completed, failed
  "created_at": ISODate("2025-08-10T12:05:00Z"),
  "completed_at": null,
  "output_file": null  // or file path if completed
}
```

## Technologies Used

* **Backend:** FastAPI, Celery, Redis, MongoDB
* **Authentication:** JWT, password hashing
* **Task Queue:** Redis Streams
* **Task Processing:** Celery workers
* **Text-to-Speech:** LLM-powered pipeline for audiobook creation
* **Email:** Google SMTP service for notifications
* **Database:** MongoDB (users & tasks)

---

## Setup and Running

1. Clone the repo
2. Configure environment variables (MongoDB URI, Redis URI, SMTP credentials, JWT secret)
3. Install dependencies
4. Run Redis and MongoDB instances
5. Start FastAPI backend
6. Start Celery worker(s)
7. Use frontend to login, submit articles, and receive audiobooks

---

## Future Improvements

* Support file uploads and multiple audiobook formats
* Use cloud storage for audiobook files (e.g., AWS S3)
* Add retry logic and error handling for failed tasks
* Implement real-time WebSocket updates for task status
* Enhance email notifications with detailed status reports

---

