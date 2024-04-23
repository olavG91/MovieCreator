# Advanced Video Creation Toolkit

## Overview
This Python toolkit automates the creation of videos by dynamically generating scenes based on user input. It leverages external content fetching, advanced audio processing, and custom scene composition including branding elements.

## Features
- Interactive video type selection through command-line input.
- Automated scene generation with tailored audio and visual elements.
- Dynamic content fetching from Pixabay for images and videos.
- Integration of custom audio transcriptions using ElevenLabs API.
- Incorporation of logos and text overlays on video clips.
- Cleanup of temporary files to maintain system hygiene.

## Dependencies
- Python 3.x
- Libraries:
  - `os`
  - `IPython`
  - `moviepy`
  - `requests`
  - `python-dotenv`
  - `uuid`
  - Additional dependencies for handling API communications and environment variables.

## Install required Python packages with pip:
pip install moviepy requests python-dotenv

## Setup
Clone or download the repository containing the script.
Install all required libraries as listed above.
Set up environment variables for API keys (ELEVENLABS_API_KEY, PIXABAY_API_KEY, OPENAI_API_KEY) in a .env file in the root directory.

## Usage
Execute the script in a Python environment capable of handling IPython displays (e.g., Jupyter Notebook, IPython shell). Start the script and follow the on-screen prompts to specify the type of video you wish to create. The script orchestrates the entire process from content fetching to video compilation, outputting the final product in the specified directory.

## Output Files
Temporarily saves screenshots in temp/screenshot.png.
Outputs the final compiled video to output/final_video.mp4.

## Cleanup Process
The script is designed to clean up all temporary files stored in the temp directory to prevent clutter and manage storage efficiently.

## Contributing
Contributions to improve the toolkit are welcome. Please fork the repository and submit pull requests with your suggested changes.

License
This project is available under [License Name]. For more details, see the LICENSE file in the repository.

Note
Ensure the creation of necessary directories (temp/ and output/) if they do not exist, or verify that the script includes their creation to avoid errors during runtime.
