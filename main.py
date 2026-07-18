import os
import subprocess
import base64
import yt_dlp
import static_ffmpeg
import whisper
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

static_ffmpeg.add_paths()
load_dotenv()

def download_video(youtube_url, output_folder="media_files"):
    """
    Downloads the YouTube video as an MP4 file.
    Returns the path to the downloaded video.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    print(f"Starting video download for: {youtube_url}")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'quiet': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"\nVideo download complete! Saved to: {filename}")
            return filename
    except Exception as e:
        print(f"\nAn error occurred during download: {e}")
        return None

def extract_frames(video_path, output_folder="frames", frame_rate=0.1):
    """
    Uses FFmpeg to extract frames from the video.
    frame_rate=0.1 means 1 frame every 10 seconds.
    Returns a list of file paths to the extracted images.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    print("\nExtracting visual frames from the video...")
    
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_pattern = os.path.join(output_folder, f"{base_name}_%03d.jpg")
    
    command = [
        "ffmpeg", "-y", "-i", video_path, 
        "-vf", f"fps={frame_rate}", 
        output_pattern
    ]
    
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    extracted_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.startswith(base_name)]
    
    final_frames = sorted(extracted_files)[:5]
    print(f"Extracted {len(final_frames)} key frames for analysis.")
    return final_frames

def transcribe_video(video_path):
    """
    Passes the MP4 file directly into Whisper to extract the text.
    """
    print("\nLoading Whisper AI model...")
    model = whisper.load_model("small.en")
    
    print("Transcribing audio directly from the video file...")
    result = model.transcribe(video_path)
    
    transcript_text = result["text"]
    print("Transcription complete!")
    return transcript_text

def analyze_multimodal(transcript_text, frame_paths):
    """
    Sends the text transcript AND the visual frames to Gemini 
    to generate a comprehensive multimodal summary.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in the .env file.")
        return None
        
    print("\nInitializing Multimodal LLM Agent (Gemini 3.5 Flash)...")
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", google_api_key=api_key)
    
    content = [
        {
            "type": "text", 
            "text": f"""
            You are an expert AI video analyst. 
            Below is the audio transcript of a video, followed by a sequence of visual frames extracted from the video.
            
            TRANSCRIPT:
            {transcript_text}
            
            Please analyze both the text and the images and provide:
            1. A 3-sentence summary of what is happening (combining what is said and what is shown).
            2. A bulleted list of key visual elements you see in the frames.
            3. A bulleted list of key concepts mentioned in the audio.
            """
        }
    ]
    
    for frame_path in frame_paths:
        with open(frame_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"}
            })
            
    message = HumanMessage(content=content)
    
    print("Analyzing audio and visuals together. This may take a few seconds...\n")
    response = llm.invoke([message])
    
    raw_content = response.content
    if isinstance(raw_content, list):
        extracted_text = [block["text"] for block in raw_content if "text" in block]
        return "\n".join(extracted_text)
        
    return raw_content

if __name__ == "__main__":
    test_video_url = "https://www.youtube.com/watch?v=sNhhvQGsMEc" 
    
    video_file = download_video(test_video_url)
    
    if video_file:
        frames = extract_frames(video_file)
        
        transcript = transcribe_video(video_file)
        
        if transcript and frames:
            analysis = analyze_multimodal(transcript, frames)
            
            print("====================================")
            print("      MULTIMODAL AI ANALYSIS        ")
            print("====================================")
            print(analysis)