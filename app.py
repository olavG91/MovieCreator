from openai import OpenAI
from moviepy.editor import concatenate_videoclips, CompositeVideoClip, ImageClip, AudioFileClip, TextClip, transfx, VideoFileClip
import requests
import json
import ffmpeg
import os
import uuid
from IPython.display import Image
import random

from resource.external_content import get_content
from resource.generate_scenes import generate_search_keywords_and_text
from resource.build_scenes import create_scenes

client = OpenAI()

pixabay_api_key = '42911360-3ee40ed889ed85ecce5deb39e'
elevenlabs_api_key = 'aeda2f6f52219ccc7705f99513d93cb1'

if not os.path.exists('temp'):
    os.makedirs('temp')

video_type = input("What type of video would you like to create?")

scenes = generate_search_keywords_and_text(video_type)

get_content(scenes)

edited_clip, clips = create_scenes(scenes)

filename = f"temp/screenshot.png"
edited_clip.save_frame(filename, t=clips[0].duration - 0.5)
Image(filename=filename, width=200)

edited_clip.write_videofile("output/final_video.mp4", codec="libx264", audio_codec="mp3", fps=24)

for file in os.listdir('temp'):
    os.remove(f'temp/{file}')