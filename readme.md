Multimodal AI Video Summarizer 

This project is a fully automated AI agent that acts as a "Video Analyst." Given a YouTube URL, it downloads the video, transcribes the audio, extracts key visual frames, and uses Google's Gemini Multimodal AI to generate a comprehensive summary of both what is said and what is shown.

Features

Video Downloading: Uses yt-dlp to grab the highest-quality MP4 from YouTube.

Visual Extraction: Uses static-ffmpeg to slice the video and capture key visual frames.

Local Audio Transcription: Uses OpenAI's whisper model (small.en) running locally to convert audio to text with high accuracy.

Multimodal Synthesis: Uses langchain and Google's gemini-3.5-flash model to analyze the text and images simultaneously.

Prerequisites

Python 3.8 or higher

A free Google Gemini API Key (get one at Google AI Studio)

Setup Instructions

Clone the repository:

git clone <your-repository-url>
cd LLM-Video-Summarizer


Create and activate a virtual environment:

python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Set up your API Key:
Create a .env file in the root directory and add your Google API key:

GOOGLE_API_KEY=your_api_key_here


Usage

Open main.py and modify the test_video_url variable at the bottom of the script to any YouTube URL you want to analyze.

Then, run the script:

python main.py


Hardware Note

By default, this script runs the Whisper transcription model on your CPU. This makes it highly portable and easy to run on any machine. For faster transcription times, you can upgrade your PyTorch installation to use CUDA (NVIDIA GPUs).