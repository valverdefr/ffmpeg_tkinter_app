import subprocess
import re
import threading
import time
from status_bar import draw_segmented_progress_bar, update_time_label
from file_handling import get_video_duration, time_to_seconds

def start_conversion_thread(overwrite=False, selected_file_path=None):
    # Start the conversion process in a thread
    conversion_thread = threading.Thread(target=process_video, args=(overwrite, selected_file_path))
    conversion_thread.start()

def process_video(overwrite, selected_file_path):
    if not selected_file_path:
        print("No file selected.")
        return

    # Generate output path
    output_file = selected_file_path.rsplit('.', 1)[0] + "_output.avi"

    # Set up FFmpeg command
    command = ['ffmpeg', '-y', '-i', selected_file_path, output_file]

    # Start FFmpeg process
    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)

    # Regular expression to extract progress
    time_pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')

    # Get video duration
    duration = get_video_duration(selected_file_path)
    start_time = time.time()

    # Track progress
    for line in process.stderr:
        match = time_pattern.search(line)
        if match:
            current_time = match.group(1)
            current_seconds = time_to_seconds(current_time)
            progress_percent = (current_seconds / duration) * 100
            draw_segmented_progress_bar(progress_percent)

            # Update remaining time
            elapsed_time = time.time() - start_time
            remaining_time = (elapsed_time / current_seconds) * duration - elapsed_time
            update_time_label(f"Estimated time remaining: {int(remaining_time)} seconds")

    process.wait()

    if process.returncode == 0:
        print("Conversion complete!")
        draw_segmented_progress_bar(100)
        update_time_label("Conversion Complete!")
    else:
        print("FFmpeg Error during processing")
