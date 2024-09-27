import tkinter as tk
import ffmpeg
import os

import subprocess

def check_ffmpeg():
    try:
        # Run the ffmpeg -version command to check if FFmpeg is accessible
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        
        # Print the result in the terminal
        print(result.stdout)
        if result.returncode == 0:
            print("FFmpeg is working correctly")
        else:
            print("FFmpeg encountered an issue.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

root = tk.Tk()
root.title("FFmpeg Tkinter App")

root.geometry("400x200")
label = tk.Label(root, text="Hello, FFmpeg and Tkinter!")
label.pack(pady=20)

# Add a button to trigger FFmpeg
btn = tk.Button(root, text="Test FFmpeg", command=check_ffmpeg)
btn.pack(pady=10)

root.mainloop()