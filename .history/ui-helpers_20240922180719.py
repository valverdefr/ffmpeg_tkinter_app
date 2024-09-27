import tkinter as tk
from tkinter import filedialog

def create_menu(menu_bar, root):
    """Create the menu with File and Edit options."""
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=lambda: open_file_dialog(root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Convert", command=start_conversion_thread, state="disabled")

def open_file_dialog(root):
    """Open file dialog to select a video file."""
    filedialog.askopenfilename(title="Select a video file", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))

def setup_ui(root):
    """Setup main UI elements."""
    # Create custom canvas for video bar and a label for displaying video name
    custom_canvas = tk.Canvas(root, height=90)
    custom_canvas.pack(fill=tk.X, pady=20)

    label = tk.Label(root, text="No file selected")
    label.pack(pady=20)

    return custom_canvas, label

def draw_segmented_progress_bar(progress_percent, progress_canvas):
    """Draw the segmented progress bar."""
    segments = 10
    progress_canvas.delete("all")
    segment_width = (progress_canvas.winfo_width() - (segments - 1) * 5) // segments
    for i in range(segments):
        color = "green" if i < int(progress_percent / 100 * segments) else "lightgrey"
        progress_canvas.create_rectangle(i * (segment_width + 5), 0, (i + 1) * segment_width, 20, fill=color)

