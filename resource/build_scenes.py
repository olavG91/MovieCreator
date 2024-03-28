from moviepy.editor import CompositeVideoClip, ImageClip, AudioFileClip, TextClip, transfx, VideoFileClip

from resource.video_tools import resize_clip_to_fit, adjust_text_to_max_length
from resource.external_audio import create_audio

logo_path = "./logo.png"
logo_clip = ImageClip(logo_path).set_position((50, 50))
logo_clip = logo_clip.resize(width=200)

clips = []

def create_scenes(scenes):
    for scene in scenes:
        for content in scene["content"]:
            #audio_filename = "7a068442-7351-485c-a2d8-60d579fd7aa7.mp3"
            audio_filename = create_audio(scene["transcribe"])
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

    return edited_clip, clips