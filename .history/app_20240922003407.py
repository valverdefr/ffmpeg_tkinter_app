import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import re
import os
import time

selected_file_path = None  # Global variable to store the selected file path

def select_file():
    global selected_file_path
    # Open file dialog to select a video file
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    if file_path:
        selected_file_path = file_path
        label.config(text=f"Selected file: {file_path}")
        update_custom_progress_bar(file_path)  # Update the custom bar with video name
    else:
        label.config(text="No file selected")
        custom_canvas.delete("all")  # Clear the custom progress bar

def process_video():
    global selected_file_path
    if not selected_file_path:
        messagebox.showwarning("No file selected", "Please select a video file first.")
        return
    
    try:
        # Perform FFmpeg operation here (example: convert to AVI)
        output_file = selected_file_path.rsplit('.', 1)[0] + "_output.avi"

        # Check if the file exists before processing
        if not os.path.exists(selected_file_path):
            raise FileNotFoundError(f"File '{selected_file_path}' not found!")

        # Reset progress bar
        progress_bar['value'] = 0
        time_label.config(text="Estimated time remaining: Calculating...")
        root.update_idletasks()

        # Use Popen to capture real-time output
        command = ['ffmpeg', '-i', selected_file_path, output_file]
        process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Regex to match the time in the output
        time_pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')

        # Estimate duration using ffprobe (or provide duration manually)
        duration = get_video_duration(selected_file_path)
        print(f"Video duration: {duration} seconds")

        start_time = time.time()

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

                # Calculate time remaining
                elapsed_time = time.time() - start_time
                estimated_total_time = (elapsed_time / current_seconds) * duration
                remaining_time = estimated_total_time - elapsed_time

                # Update the time remaining label
                time_label.config(text=f"Estimated time remaining: {int(remaining_time)} seconds")
                root.update_idletasks()

        process.wait()  # Wait for the process to complete

        if process.returncode == 0:
            label.config(text=f"Processing complete: {output_file}")
            messagebox.showinfo("Success", f"Video processing complete!\nOutput file: {output_file}")
            time_label.config(text="Processing complete!")
        else:
            raise subprocess.CalledProcessError(process.returncode, command)

    except FileNotFoundError as e:
        messagebox.showerror("File Error", f"File error: {str(e)}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("FFmpeg Error", f"FFmpeg error during processing: {e}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n{str(e)}")

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

def toggle_fullscreen(event=None):
    # Toggle fullscreen mode on/off with F11
    is_fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not is_fullscreen)

def exit_app():
    root.quit()  # Exit the application

def update_custom_progress_bar(file_name):
    # Clear the canvas
    custom_canvas.delete("all")
    
    # Draw a thick light blue bar
    custom_canvas.create_rectangle(10, 10, 580, 80, fill="lightblue", outline="lightblue")
    
    # Add video name as caption inside the bar
    custom_canvas.create_text(300, 45, text=file_name.split('/')[-1], fill="white", font=('Arial', 14, 'bold'))

# GUI setup
root = tk.Tk()
root.title("FFmpeg Video Processor with Progress")

# Allow resizing
root.geometry("600x400")
root.resizable(True, True)  # Allow resizing both horizontally and vertically

# Bind F11 to toggle fullscreen
root.bind("<F11>", toggle_fullscreen)

# Menu setup
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=select_file)  # Open video
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)  # Exit app

# Big light blue custom progress bar canvas
custom_canvas = tk.Canvas(root, width=600, height=90)
custom_canvas.pack(pady=20)

label = tk.Label(root, text="No file selected")
label.pack(pady=20)

# Progress bar widget
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Time remaining label
time_label = tk.Label(root, text="Estimated time remaining: N/A")
time_label.pack(pady=10)

# Button to process the video after file selection
btn_process = tk.Button(root, text="Process Video", command=process_video)
btn_process.pack(pady=10)

root.mainloop()
