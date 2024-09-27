import tkinter as tk
from tkinter import filedialog
import subprocess

def select_file():
    # Open file dialog to select a video file
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    if file_path:
        # Display selected file in the label
        label.config(text=f"Selected file: {file_path}")
        return file_path
    else:
        label.config(text="No file selected")
        return None

def process_video():
    file_path = select_file()
    if file_path:
        # Perform FFmpeg operation here (example: convert to AVI)
        output_file = file_path.rsplit('.', 1)[0] + "_output.avi"
        try:
            result = subprocess.run(['ffmpeg', '-i', file_path, output_file], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Video processing complete. Output file: {output_file}")
            else:
                print(f"Error during processing: {result.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

root = tk.Tk()
root.title("FFmpeg Video Processor")

root.geometry("400x200")
label = tk.Label(root, text="No file selected")
label.pack(pady=20)

# Add a button to select a video and process it
btn = tk.Button(root, text="Select and Process Video", command=process_video)
btn.pack(pady=10)

root.mainloop()
