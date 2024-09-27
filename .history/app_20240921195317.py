import tkinter as tk
import ffmpeg

# Create the main window
root = tk.Tk()
root.title("FFmpeg Tkinter App")

# Set the size of the window
root.geometry("400x200")

# Add a label to the window
label = tk.Label(root, text="Hello, FFmpeg and Tkinter!")
label.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
