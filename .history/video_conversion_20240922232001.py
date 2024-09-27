import subprocess
import re

def convert_video(file_path, output_format="avi"):
    """Convert video file to the specified format using FFmpeg."""
    output_file = file_path.rsplit('.', 1)[0] + f"_output.{output_format}"
    
    # Command to convert video
    command = ['ffmpeg', '-i', file_path, output_file]
    subprocess.run(command, check=True)
    
    return output_file

def get_video_duration(file_path):
    """Get the duration of the video file using FFmpeg."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    duration_str = result.stdout.decode('utf-8').strip()
    return float(duration_str) if duration_str else 0

def time_to_seconds(time_str):
    """Convert time in the format 'hh:mm:ss' or 'mm:ss' to seconds."""
    parts = time_str.split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    else:
        raise ValueError("Invalid time format")
