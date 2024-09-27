import tkinter as tk
import ffmpeg
import os

def check_ffmpeg():
    input_file = 'dummy.mp4'
    
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    try:
        # Simple ffmpeg command to check if it works
        ffmpeg.input(input_file).output('dummy_output.mp4').run()
        print("FFmpeg ran successfully!")
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
