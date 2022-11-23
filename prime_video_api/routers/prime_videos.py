from typing import List
from fastapi import APIRouter
from prime_video_api.schemas import prime_videos as prime_videos_schema
from prime_video_api.cruds import prime_videos as prime_videos_cruds

router = APIRouter()

@router.get("/prime_videos", response_model=List[prime_videos_schema.Video])
async def search_videos(keyword: str) -> List[prime_videos_schema.Video]:
  return await prime_videos_cruds.search_videos(keyword)

@router.get("/prime_videos_v2", response_model=List[prime_videos_schema.Video])
async def search_videos_v2(keyword: str) -> List[prime_videos_schema.Video]:
  return await prime_videos_cruds.search_videos_v2(keyword)

@router.get("/prime_videos/leaving_soon")
async def get_leaving_soon_videos() -> prime_videos_schema.LeavingSoonVideos:
  return await prime_videos_cruds.get_leaving_soon_videos()

@router.post("/prime_videos/video_info", response_model=prime_videos_schema.VideoInfo)
async def get_video_info(getVideoInfoDto: prime_videos_schema.GetVideoInfoDto) -> prime_videos_schema.VideoInfo:
  return await prime_videos_cruds.get_video_info(getVideoInfoDto)