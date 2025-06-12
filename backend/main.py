from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from starlette import requests
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],      
)



@app.get("/")
def read_root():
    return {"status": "healthy"}

@app.post("/convert")
async def convert_to_audio(payload: LinkPayload):
    # Simulate processing
    print(f"Received URL: {payload.url}")

    # Return dummy response for now
    return {
        "status": "success",
        "message": f"Audio conversion started for {payload.url}",
        "audio_url": "https://example.com/audio.mp3"
    }



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
