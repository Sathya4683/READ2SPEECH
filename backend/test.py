from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from jose import jwt
import os
import time

app = FastAPI()

# ----------------- Settings -----------------
SECRET_KEY = "secret"
ALGORITHM = "HS256"
AUDIO_FOLDER = r"E:\CODE\READ2SPEECH\backend\audio"

AUDIO_FOLDER = os.path.normpath(AUDIO_FOLDER)

# ----------------- CORS for frontend access -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Models -----------------
class AuthInput(BaseModel):
    username: str
    password: str

class LinkInput(BaseModel):
    username: str
    link: str

class MailPrefInput(BaseModel):
    username: str
    send_mails: bool

# ----------------- Routes -----------------

@app.post("/signin")
def signin(data: AuthInput):
    token_data = {
        "user": data.username,
        "exp": time.time() + 3600  # expires in 1 hour
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return { "access_token": token }

@app.post("/signup")
def signup(data: AuthInput):
    # Simulate user save
    return { "msg": "Account created!" }

@app.post("/add")
def add_link(data: LinkInput):
    print(f"[LOG] {data.username} submitted link: {data.link}")
    return { "msg": "Link received!" }

@app.post("/set-email-preference")
def set_email(data: MailPrefInput):
    print(f"[LOG] {data.username} wants email = {data.send_mails}")
    return { "msg": "Preference saved!" }

@app.get("/userdetails/{username}")
def get_user_data(username: str):
    return {
        "webpages": [
            "https://www.geeksforgeeks.org/os-basics",
            "https://realpython.com/python-oop/"
        ],
        "finished": [
            {
                "website": "GeeksforGeeks - OS Basics",
                "download_link": "http://localhost:8000/download/os-basics.mp3"
            },
            {
                "website": "RealPython - OOP",
                "download_link": "http://localhost:8000/download/oop.mp3"
            },
            {
                "website": "Recording Sample",
                "download_link": "http://localhost:8000/download/recording.mp3"
            }
        ],
        "send_mail": True
    }

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(AUDIO_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ----------------- Static mount (optional) -----------------
# This is useful if you still want to allow in-browser streaming.
app.mount("/audio", StaticFiles(directory=AUDIO_FOLDER), name="audio")

# ----------------- Run -----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test:app", host="127.0.0.1", port=8000, reload=True)
