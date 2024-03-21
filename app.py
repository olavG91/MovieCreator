from openai import OpenAI
from moviepy.editor import concatenate_videoclips, CompositeVideoClip, ImageClip, AudioFileClip, TextClip, transfx, VideoFileClip
import requests
import json
import ffmpeg
import os
import uuid
from IPython.display import Image
import random

client = OpenAI()

pixabay_api_key = '42911360-3ee40ed889ed85ecce5deb39e'
elevenlabs_api_key = 'aeda2f6f52219ccc7705f99513d93cb1'

if not os.path.exists('temp'):
    os.makedirs('temp')

video_type = input("What type of video would you like to create?")
def generate_search_keywords_and_text(video_type):
    messages=[
        {
            "role": "user", "content": f"Craft a video script for a Facebook Reel that concisely and engagingly explains {video_type}." +
            "The script itself must be in Swedish, maintaining a clear and accessible language style suitable for a broad audience." +
            "However, all search queries specified for sourcing videos and images should be provided in English." +
            "The first scene should mention what the video is about. The video should not have any introduction or outro."
        }
    ]

    functions = [
    {
        "name": "create_video_script",
        "description": "Create a video script with scenes that has videos.",
        "parameters": {
            "type": "object",
            "properties": {
                "scenes": {
                    "type": "array",
                    "description": "Scenes to use in the video",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Scene name"
                            },
                            "transcribe": {
                                "type": "string",
                                "description": "A short text to use in the scene for the transcribe."
                            },
                            "content": {
                                "type": "array",
                                "description": "Content to use in the scene",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "Search query for a video that should be displayed in the scene, maximum one word. Should be used for searching content at Pixabay. Written in English."
                                        },
                                        "text": {
                                            "type": "string",
                                            "description": "Short text to display on the video."
                                        },
                                    },
                                    "required": ["name", "text"]
                                },
                                "minItems": 1,
                                "maxItems": 1
                            }
                        },
                        "required": ["name", "transcribe", "content"]
                    },
                    "minItems": 5,
                    "maxItems": 10
                },
            },
            "required": ["scenes"]
        }
    }
    ]

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        functions=functions,
        temperature=0.5
    )

    arguments = json.loads(response.choices[0].message.function_call.arguments)
    return arguments["scenes"]

scenes = generate_search_keywords_and_text(video_type)

def search_pixabay_videos(query):
    response = requests.get(f"https://pixabay.com/api/videos/?key={pixabay_api_key}&q={query}")
    if response.status_code == 200:
        data = json.loads(response.text)
        return [hit['videos']['large']['url'] for hit in data['hits']]
    else:
        return []
    
def search_pixabay_images(query):
    response = requests.get(f"https://pixabay.com/api/?key={pixabay_api_key}&q={query}")
    if response.status_code == 200:
        data = json.loads(response.text)
        return [hit['largeImageURL'] for hit in data['hits']]
    else:
        return []
    
def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"temp/{url.split('/')[-1].split('?')[0]}"
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return None
    
def create_audio(text):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/nPczCjzI2devNBz1zQrb"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": elevenlabs_api_key
    }

    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.7,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)

    filename = f"temp/{uuid.uuid4()}.mp3"  # Generate a random filename
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    
    return filename

for scene in scenes:
    for content in scene["content"]:
        videos = search_pixabay_videos(content["name"])
        if videos:
            video = random.choice(videos)
            if video:
                video_url = download(video)
                if video_url:
                    content["url"] = video_url
                    content["type"] = "video"
                else:
                    print(f"Failed to download {video}")
            else:
                print(f"No videos found for {content['name']}")
                print(videos)
        else:
            images = search_pixabay_images(content["name"])
            if images:
                image = random.choice(images)
                if image:
                    image_url = download(image)
                    if image_url:
                        content["url"] = image_url
                        content["type"] = "image"
                    else:
                        print(f"Failed to download {image}")
                else:
                    print(f"No images found for {content['name']}")
            else:
                print(f"No videos or images found for {content['name']}")
                print(images)

def resize_clip_to_fit(clip, target_size):
    clip_aspect_ratio = clip.w / clip.h
    target_aspect_ratio = target_size[0] / target_size[1]
    
    if clip_aspect_ratio > target_aspect_ratio:
        scale_factor = target_size[1] / clip.h
    else:
        scale_factor = target_size[0] / clip.w
    
    resized_clip = clip.resize(height=int(clip.h * scale_factor))
    pos_x = (target_size[0] - resized_clip.w) // 2
    pos_y = (target_size[1] - resized_clip.h) // 2
    
    final_clip = CompositeVideoClip([resized_clip.set_position((pos_x, pos_y))], size=target_size)
    return final_clip

def adjust_text_to_max_length(text, max_length=25):
    if len(text) <= max_length:
        return text
    # Split text into words
    words = text.split()
    adjusted_text = words[0]
    for word in words[1:]:
        # Check if adding the next word exceeds max length
        if len(adjusted_text) + len(word) + 1 <= max_length:
            adjusted_text += " " + word
        else:
            break
    return adjusted_text

logo_path = "logo.png"
logo_clip = ImageClip(logo_path).set_position((50, 50))
logo_clip = logo_clip.resize(width=200)

clips = []

for scene in scenes:
    for content in scene["content"]:
        audio_filename = "7a068442-7351-485c-a2d8-60d579fd7aa7.mp3"
        #audio_filename = create_audio(scene["transcribe"])
        audio = AudioFileClip(audio_filename)

        if content["type"] == "video":
            content_clip = VideoFileClip(content["url"]).set_duration(audio.duration + 1).set_audio(audio)
        else:
            content_clip = ImageClip(content["url"]).set_duration(audio.duration + 1).set_audio(audio)

        resized_clip = resize_clip_to_fit(content_clip, (1080, 1920))

        adjusted_text = adjust_text_to_max_length(content["text"], 25)
        text_clip = TextClip(adjusted_text, fontsize=70, color='white')
        text_clip = text_clip.on_color(size=(text_clip.w + 140, text_clip.h + 40), color=(0,0,0), pos=('center','center'), col_opacity=1)
        text_clip = text_clip.set_position(('center', 'bottom')).set_duration(audio.duration + 1)

        final_clip = CompositeVideoClip([resized_clip, text_clip, logo_clip.set_duration(content_clip.duration)], size=(1080, 1920))

        clips.append(final_clip)
edited_clip = clips[0]

for next_clip in clips[1:]:
    transition_clip = next_clip.fx(transfx.slide_in, 1, 'right')
    combined_clip = CompositeVideoClip([edited_clip, transition_clip.set_start(edited_clip.duration - 1)])
    edited_clip = combined_clip

filename = f"temp/screenshot.png"
edited_clip.save_frame(filename, t=clips[0].duration - 0.5)
Image(filename=filename, width=200)
edited_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="mp3", fps=3)

for file in os.listdir('temp'):
    os.remove(f'temp/{file}')