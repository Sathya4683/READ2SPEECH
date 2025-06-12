from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth,feed,users
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

app.include_router(auth.router)
app.include_router(feed.router)
app.include_router(users.router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
