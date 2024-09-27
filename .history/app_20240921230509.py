import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
import subprocess
import re
import os

def select_file():
    # Open file dialog to select a video file
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    if file_path:
        label.config(text=f"Selected file: {file_path}")
        return file_path
    else:
        label.config(text="No file selected")
        return None

def process_video():
    file_path = select_file()
    if not file_path:
        messagebox.showwarning("No file selected", "Please select a valid video file.")
        return

    try:
        # Perform FFmpeg operation here (example: convert to AVI)
        output_file = file_path.rsplit('.', 1)[0] + "_output.avi"

        # Check if the file exists before processing
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found!")

        # Reset progress bar
        progress_bar['value'] = 0
        root.update_idletasks()

        # Use Popen to capture real-time output
        command = ['ffmpeg', '-i', file_path, output_file]
        process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Regex to match the time in the output
        time_pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')

        # Estimate duration using ffprobe (or provide duration manually)
        duration = get_video_duration(file_path)
        print(f"
