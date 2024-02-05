import os
import requests
import googleapiclient.discovery
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()  # take environment variables from .env.

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Use /video to extract video link from YouTube. Pass the query as a parameter."}

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

@app.get("/image")
async def get_image(query: str):
    api_key = os.getenv("UNSPLASH_API_KEY")  # replace with your environment variable name
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {"query": query, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    first_image_url = data['results'][0]['urls']['small']
    return {"image_url": first_image_url}