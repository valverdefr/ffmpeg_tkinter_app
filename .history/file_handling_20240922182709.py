import tkinter as tk
from tkinter import filedialog
import subprocess

def select_file():
    # Open file dialog to select a video file
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    return file_path  # Return the selected file path

def get_video_duration(file_path):
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        duration_str = result.stdout.decode('utf-8').strip()
        return float(duration_str) if duration_str else 0
    except subprocess.CalledProcessError:
        return 0

def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
