import os
from tkinter import filedialog

def select_file():
    """Open a file dialog to select a file."""
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("All files", "*.*"),)
    )
    return file_path

def get_file_type(file_path):
    """Determine the type of file (video, audio, image) based on its extension."""
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension in ['.mp4', '.avi', '.mkv', '.mov']:
        return "video"
    elif extension in ['.mp3', '.wav', '.ogg']:
        return "audio"
    elif extension in ['.png', '.jpg', '.jpeg', '.bmp']:
        return "image"
    else:
        raise ValueError("Unsupported file type")
