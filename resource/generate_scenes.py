from openai import OpenAI
import json

client = OpenAI()

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