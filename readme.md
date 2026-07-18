# Multimodal AI Video Summarizer
 
An AI agent that acts as your personal **Video Analyst**. Give it a YouTube URL, and it will automatically download the video, transcribe the audio, extract key visual frames, and use Google's Gemini multimodal AI to generate a comprehensive summary of both what is *said* and what is *shown*.
 
---
 
## Features
 
| Feature | Description |
|---|---|
| **Video Downloading** | Uses [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) to grab the highest-quality MP4 from YouTube. |
| **Visual Extraction** | Uses `static-ffmpeg` to slice the video and capture key visual frames. |
| **Local Audio Transcription** | Uses OpenAI's **Whisper** (`small.en`) running locally to convert audio to text with high accuracy. |
| **Multimodal Synthesis** | Uses `langchain` and Google's `gemini-3.5-flash` model to analyze text and images simultaneously. |
 
---
 
## Prerequisites
 
- Python 3.8 or higher
- A free **Google Gemini API Key** — get one at [Google AI Studio](https://aistudio.google.com/)
---
 
## Setup Instructions
 
### 1. Clone the repository
 
```bash
git clone <your-repository-url>
cd LLM-Video-Summarizer
```
 
### 2. Create and activate a virtual environment
 
```bash
python -m venv venv
```
 
```bash
# On Windows:
venv\Scripts\activate
 
# On macOS/Linux:
source venv/bin/activate
```
 
### 3. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Set up your API key
 
Create a `.env` file in the root directory and add your Google API key:
 
```env
GOOGLE_API_KEY=your_api_key_here
```
 
---
 
## Usage
 
1. Open `main.py` and modify the `test_video_url` variable at the bottom of the script to any YouTube URL you want to analyze.
2. Run the script:
```bash
python main.py
```
 
---
 
## Hardware Note
 
By default, this script runs the Whisper transcription model on your **CPU**. This makes it highly portable and easy to run on any machine.
 
> **Tip:** For faster transcription times, you can upgrade your PyTorch installation to use **CUDA** (NVIDIA GPUs).
 
---
 
## Tech Stack
 
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [static-ffmpeg](https://pypi.org/project/static-ffmpeg/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [LangChain](https://www.langchain.com/)
- [Google Gemini](https://ai.google.dev/)
---
 
## License
 
This project is licensed under the [MIT License](LICENSE).