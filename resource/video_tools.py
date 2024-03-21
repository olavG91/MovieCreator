from moviepy.editor import CompositeVideoClip

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