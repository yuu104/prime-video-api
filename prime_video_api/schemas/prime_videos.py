from typing import Optional, List
from pydantic import BaseModel

class Video(BaseModel):
  title: str
  url: str
  image: Optional[str]

class VideoInfo(BaseModel):
  is_available: bool
  is_leaving_soon: bool

class GetVideoInfoDto(BaseModel):
  url: str

class LeavingSoonVideos(BaseModel):
  videos: List[str]