import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import subprocess
import re
import os
import time
import threading

selected_file_path = None  # Global variable to store the selected file path
convert_menu = None  # Reference to the "Convert" menu item
process = None  # Global reference for the FFmpeg process
time_label = None  # Global reference for the time estimate label
progress_canvas = None  # Global reference for the custom progress canvas

def select_file():
    global selected_file_path
    global convert_menu
    # Open file dialog to select a video file
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    if file_path:
        selected_file_path = file_path
        label.config(text=f"Selected file: {file_path}")
        convert_menu.entryconfig("Convert", state="normal")  # Enable Convert option
        update_custom_progress_bar()  # Update the custom bar with video name
    else:
        label.config(text="No file selected")
        custom_canvas.delete("all")  # Clear the custom progress bar
        convert_menu.entryconfig("Convert", state="disabled")  # Disable Convert option
        update_custom_progress_bar()  # Redraw empty bar with bevel border

def start_conversion_thread(overwrite=False):
    # Start the conversion process in a separate thread to keep the GUI responsive
    conversion_thread = threading.Thread(target=process_video, args=(overwrite,))
    conversion_thread.start()

def process_video(overwrite=False):
    global selected_file_path
    global process  # Use global reference to allow process termination
    if not selected_file_path:
        messagebox.showwarning("No file selected", "Please select a video file first.")
        return

    # Generate the output file path
    output_file = selected_file_path.rsplit('.', 1)[0] + "_output.avi"

    # Check if the output file already exists
    if os.path.exists(output_file) and not overwrite:
        # Show the prompt window for overwrite or cancel
        show_overwrite_prompt(output_file)
        return

    # Reset progress bar and time label
    draw_segmented_progress_bar(0)  # Reset the segmented progress bar
    time_label.config(text="Estimated time remaining: N/A")
    root.update_idletasks()

    def complete_conversion():
        # After conversion, update the UI and show success message
        time_label.config(text="Conversion Complete!")
        messagebox.showinfo("Success", f"Video conversion complete!\nOutput: {output_file}")

    try:
        # Use Popen to capture real-time output
        command = ['ffmpeg', '-y', '-i', selected_file_path, output_file]  # Added '-y' to overwrite the file
        process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)

        # Regex to match the time in the output
        time_pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')

        # Estimate duration using ffprobe (or provide duration manually)
        duration = get_video_duration(selected_file_path)
        print(f"Video duration: {duration} seconds")

        start_time = time.time()

        # Update the progress bar while conversion happens
        for line in process.stderr:
            match = time_pattern.search(line)
            if match:
                current_time = match.group(1)
                current_seconds = time_to_seconds(current_time)

                # Calculate progress as percentage
                progress_percent = (current_seconds / duration) * 100
                draw_segmented_progress_bar(progress_percent)  # Update the custom segmented progress bar
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
            complete_conversion()
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

def update_custom_progress_bar():
    # Clear the canvas
    custom_canvas.delete("all")
    
    # Get the current width of the window for dynamic resizing
    window_width = root.winfo_width()
    
    # Draw bevel border effect
    if not selected_file_path:
        # Simulating a bevel effect with two rectangles
        custom_canvas.create_rectangle(10, 10, window_width - 20, 80, outline="lightgrey", width=3)
        custom_canvas.create_rectangle(12, 12, window_width - 22, 78, outline="darkgrey", width=1)
    else:
        # Draw a thick light blue bar with the video name when a file is selected
        custom_canvas.create_rectangle(10, 10, window_width - 20, 80, fill="lightblue", outline="lightblue")
        file_name = selected_file_path.split('/')[-1]
        custom_canvas.create_text(window_width // 2, 45, text=file_name, fill="white", font=('Arial', 14, 'bold'))

def on_resize(event):
    # Trigger the update of the custom progress bar when the window is resized
    update_custom_progress_bar()
    resize_progress_canvas()

def resize_progress_canvas():
    """Resize the segmented progress bar to take up 1/7th of the window's width."""
    window_width = root.winfo_width()
    progress_canvas.config(width=window_width // 7)
    draw_segmented_progress_bar(progress_bar_value)  # Redraw the progress bar after resizing

def draw_segmented_progress_bar(progress_percent):
    """Draw a custom segmented progress bar."""
    global progress_bar_value
    progress_bar_value = progress_percent  # Store progress for redrawing on resize
    progress_canvas.delete("all")  # Clear the canvas
    segments = 10  # Number of segments (reduced for smaller bar)
    segment_width = (progress_canvas.winfo_width() - (segments - 1) * 5) // segments  # Dynamically calculate segment width
    gap = 5  # Gap between segments
    
    # Calculate the number of filled segments based on progress percentage
    filled_segments = int((progress_percent / 100) * segments)
    
    # Draw segments on the canvas
    for i in range(segments):
        color = "green" if i < filled_segments else "lightgrey"
        progress_canvas.create_rectangle(i * (segment_width + gap), 0, (i + 1) * segment_width + i * gap, 20, fill=color, outline=color)

def show_overwrite_prompt(output_file):
    # Show a floating window to ask whether to overwrite or cancel
    prompt_window = Toplevel(root)
    prompt_window.title("File Already Exists")

    message = tk.Label(prompt_window, text=f"The file '{os.path.basename(output_file)}' already exists.\nDo you want to overwrite it?")
    message.pack(pady=10)

    # Overwrite button
    overwrite_button = tk.Button(prompt_window, text="Overwrite", command=lambda: overwrite_and_proceed(prompt_window))
    overwrite_button.pack(side=tk.LEFT, padx=20, pady=10)

    # Cancel button
    cancel_button = tk.Button(prompt_window, text="Cancel", command=prompt_window.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=20, pady=10)

def overwrite_and_proceed(window):
    # Close the prompt window and proceed with the overwrite
    window.destroy()
    start_conversion_thread(overwrite=True)

# GUI setup
root = tk.Tk()
root.title("FFmpeg Video Processor with Progress")

# Allow resizing
root.geometry("800x400")  # Start with a larger window size
root.resizable(True, True)  # Allow resizing both horizontally and vertically

# Bind F11 to toggle fullscreen and resizing event to update the bar dynamically
root.bind("<F11>", toggle_fullscreen)
root.bind("<Configure>", on_resize)  # Bind resizing event to dynamically adjust the bar

# Menu setup
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=select_file)  # Open video
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)  # Exit app

# Edit menu with Convert option
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Convert", command=start_conversion_thread, state="disabled")  # Disabled until a video is selected
convert_menu = edit_menu  # Save the reference for later enabling/disabling

# Big light blue custom progress bar canvas
custom_canvas = tk.Canvas(root, height=90)
custom_canvas.pack(fill=tk.X, pady=20)  # Allow the bar to stretch horizontally with the window

# Initially draw the empty bar with a bevel border
update_custom_progress_bar()

label = tk.Label(root, text="No file selected")
label.pack(pady=20)

# Status bar at the bottom with a custom segmented progress bar and time estimate
status_bar = tk.Frame(root, relief=tk.SUNKEN, bd=1)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

progress_canvas = tk.Canvas(status_bar, width=100, height=20)  # Initial width for the segmented bar
progress_canvas.pack(side=tk.LEFT, padx=20, pady=5)

time_label = tk.Label(status_bar, text="Estimated time remaining: N/A")
time_label.pack(side=tk.LEFT, padx=20)

root.mainloop()
