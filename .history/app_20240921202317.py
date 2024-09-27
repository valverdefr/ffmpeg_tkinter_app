import tkinter as tk
import ffmpeg
import os


def check_ffmpeg():
    try:
        # Check FFmpeg installation by printing its version
        ffmpeg_version = ffmpeg.probe('-version')
        print("FFmpeg is working correctly")
    except ffmpeg.Error as e:
        stderr_output = e.stderr or b""
        print(f"FFmpeg error: {stderr_output.decode()}")
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
