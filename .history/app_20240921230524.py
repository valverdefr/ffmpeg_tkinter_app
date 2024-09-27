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
        print(f"Video duration: {duration} seconds")

        for line in process.stderr:
            print(line)  # Debugging: Print FFmpeg output
            match = time_pattern.search(line)
            if match:
                current_time = match.group(1)
                current_seconds = time_to_seconds(current_time)

                # Calculate progress as percentage
                progress_percent = (current_seconds / duration) * 100
                progress_bar['value'] = progress_percent
                root.update_idletasks()

        process.wait()  # Wait for the process to complete

        if process.returncode == 0:
            label.config(text=f"Processing complete: {output_file}")
            messagebox.showinfo("Success", f"Video processing complete!\nOutput file: {output_file}")
        else:
            raise subprocess.CalledProcessError(process.returncode, command)

    except FileNotFoundError as e:
        messagebox.showerror("File Error", f"File error: {str(e)}")
        print(f"Debug - File Error: {e}")  # Debugging: Print to console
    except subprocess.CalledProcessError as e:
        messagebox.showerror("FFmpeg Error", f"FFmpeg error during processing: {e}")
        print(f"Debug - FFmpeg Error: {e}")  # Debugging: Print to console
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n{str(e)}")
        print(f"Debug - Unexpected Error: {e}")  # Debugging: Print to console

def get_video_duration(file_path):
    # Get the video duration using ffprobe
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        duration_str = result.stdout.decode('utf-8').strip()
        if duration_str:
            return float(duration_str)
        else:
            raise ValueError(f"Could not get duration for file: {file_path}")
    except subprocess.CalledProcessError as e:
        raise Exception("Error fetching video duration with ffprobe.") from e

def time_to_seconds(time_str):
    # Convert the time format (HH:MM:SS.ms) to total seconds
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

# GUI setup
root = tk.Tk()
root.title("FFmpeg Video Processor with Progress")

root.geometry("400x250")
label = tk.Label(root, text="No file selected
