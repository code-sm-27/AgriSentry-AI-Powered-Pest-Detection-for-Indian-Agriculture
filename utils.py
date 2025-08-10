import os
import subprocess
from pytube import YouTube

def download_youtube_video(url, output_path='.', filename='downloaded_video.mp4'):
    """
    Downloads a video from YouTube. Useful for getting dataset source material.

    Args:
        url (str): The URL of the YouTube video.
        output_path (str): The directory where the video will be saved.
        filename (str): The desired filename for the downloaded video.

    Returns:
        str: The full path to the downloaded video, or None if failed.
    """
    print(f"Attempting to download video from: {url}")
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        
        if not stream:
            print("No progressive mp4 stream found.")
            return None
            
        print(f"Downloading '{yt.title}'...")
        stream.download(output_path=output_path, filename=filename)
        
        video_filepath = os.path.join(output_path, filename)
        print(f"Video downloaded successfully to: {video_filepath}")
        return video_filepath
        
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return None

def extract_frames(video_path, output_folder, fps=1):
    """
    Extracts frames from a video using ffmpeg.

    Args:
        video_path (str): The path to the video file.
        output_folder (str): The folder where the frames will be saved.
        fps (int): The number of frames to extract per second.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return
        
    os.makedirs(output_folder, exist_ok=True)
    print(f"Extracting frames from '{video_path}' at {fps} FPS...")

    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'fps={fps}',
        os.path.join(output_folder, 'frame_%05d.png')
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Frames extracted successfully to '{output_folder}'.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running ffmpeg: {e.stderr}")

if __name__ == '__main__':
    # Example usage for creating a dataset from a video about pests.
    VIDEO_URL = 'https://www.youtube.com/watch?v=YOUR_PEST_VIDEO_ID_HERE'
    DOWNLOAD_DIR = 'temp_data'
    FRAMES_DIR = 'data/raw_images'
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    downloaded_video_path = download_youtube_video(VIDEO_URL, DOWNLOAD_DIR)
    
    if downloaded_video_path:
        extract_frames(downloaded_video_path, FRAMES_DIR, fps=2)
