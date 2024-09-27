import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_file(label, custom_canvas):
    """Select file and update label and custom canvas."""
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    if file_path:
        label.config(text=f"Selected file: {file_path}")
        draw_empty_video_bar(custom_canvas)
    else:
        label.config(text="No file selected")

def draw_empty_video_bar(custom_canvas):
    """Draw an empty video bar when no file is selected."""
    window_width = custom_canvas.winfo_width()
    custom_canvas.create_rectangle(10, 10, window_width - 20, 80, outline="lightgrey", width=3)
