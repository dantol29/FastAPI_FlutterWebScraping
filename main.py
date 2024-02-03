import os
import googleapiclient.discovery
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()  # take environment variables from .env.

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.get("/video")
async def get_video(query: str):
    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query 
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    video_link = f"https://www.youtube.com/watch?v={video_id}"
    thumbnail_url = response['items'][0]['snippet']['thumbnails']['default']['url']
    return {"video_link": video_link, "thumbnail_url": thumbnail_url}