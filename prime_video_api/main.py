from fastapi import FastAPI
from  prime_video_api.routers import prime_videos
from starlette.middleware.cors import CORSMiddleware # 追加

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(prime_videos.router)