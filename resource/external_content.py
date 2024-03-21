import requests
import json
import random

pixabay_api_key = '42911360-3ee40ed889ed85ecce5deb39e'

def search_pixabay_videos(query):
    response = requests.get(f"https://pixabay.com/api/videos/?key={pixabay_api_key}&q={query}")
    if response.status_code == 200:
        data = json.loads(response.text)
        return [hit['videos']['large']['url'] for hit in data['hits'] if hit['videos']['large']['url']]
    else:
        return []
    
def search_pixabay_images(query):
    response = requests.get(f"https://pixabay.com/api/?key={pixabay_api_key}&q={query}")
    if response.status_code == 200:
        data = json.loads(response.text)
        return [hit['largeImageURL'] for hit in data['hits'] if hit['largeImageURL']]
    else:
        return []
    
def get_content(scenes):
    for scene in scenes:
        for content in scene["content"]:
            videos = search_pixabay_videos(content["name"])
            if videos:
                video = random.choice(videos)
                video_url = download(video)
                if video_url:
                    content["url"] = video_url
                    content["type"] = "video"
                    continue
            images = search_pixabay_images(content["name"])
            if images:
                image = random.choice(images)
                image_url = download(image)
                if image_url:
                    content["url"] = image_url
                    content["type"] = "image"
                    continue
            return False

def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"temp/{url.split('/')[-1].split('?')[0]}"
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return None