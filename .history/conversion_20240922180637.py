import subprocess
import re
import time
from ui_helpers import draw_segmented_progress_bar
from status_bar import update_time_label

def process_video(selected_file_path, output_file, progress_canvas, time_label):
    """Handles video conversion using FFmpeg."""
    command = ['ffmpeg', '-y', '-i', selected_file_path, output_file]

    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
    
    # Regex to match the time in the output
    time_pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')
    duration = get_video_duration(selected_file_path)

    start_time = time.time()

    for line in process.stderr:
        match = time_pattern.search(line)
        if match:
            current_time = match.group(1)
            current_seconds = time_to_seconds(current_time)
            progress_percent = (current_seconds / duration) * 100
            draw_segmented_progress_bar(progress_percent, progress_canvas)
            update_time_label(current_seconds, duration, time_label, start_time)

    process.wait()
    return process.returncode == 0

def get_video_duration(file_path):
    """Get video duration using ffprobe."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    return float(result.stdout.decode('utf-8').strip())

def time_to_seconds(time_str):
    """Convert HH:MM:SS.ms format to total seconds."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def start_conversion_thread():
    """Start the conversion process in a separate thread."""
    # This will be called from the UI to kick off the conversion process in a thread.
    pass
