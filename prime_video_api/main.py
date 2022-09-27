from fastapi import FastAPI
from  prime_video_api.routers import prime_videos

app = FastAPI()

app.include_router(prime_videos.router)