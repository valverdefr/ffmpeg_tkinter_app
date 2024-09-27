import tkinter as tk
import ffmpeg

def check_ffmpeg():
    try:
        # Simple ffmpeg probe command to check if it works
        ffmpeg.input('dummy.mp4').output('dummy_output.mp4').run()
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode()}")

root = tk.Tk()
root.title("FFmpeg Tkinter App")

root.geometry("400x200")
label = tk.Label(root, text="Hello, FFmpeg and Tkinter!")
label.pack(pady=20)

# Add a button to trigger FFmpeg
btn = tk.Button(root, text="Test FFmpeg", command=check_ffmpeg)
btn.pack(pady=10)

root.mainloop()
