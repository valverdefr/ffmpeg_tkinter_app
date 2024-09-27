import subprocess
import os

def convert_video(file_path, output_format="avi"):
    """Convert video file to the specified format using FFmpeg."""
    output_file = file_path.rsplit('.', 1)[0] + f"_output.{output_format}"
    
    # Command to convert video with overwrite enabled
    command = ['ffmpeg', '-y', '-i', file_path, output_file]
    
    # Run the FFmpeg command and handle any exceptions
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error during video conversion: {e}")
    
    return output_file
