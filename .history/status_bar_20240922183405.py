import tkinter as tk

progress_canvas = None
time_label = None
selected_file_path = None  # To store selected file path for display

def setup_status_bar(root):
    global progress_canvas, time_label

    # Create status bar
    status_bar = tk.Frame(root, relief=tk.SUNKEN, bd=1)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Set up segmented progress bar
    progress_canvas = tk.Canvas(status_bar, width=100, height=20)
    progress_canvas.pack(side=tk.LEFT, padx=20, pady=5)

    # Set up time label (hidden initially)
    time_label = tk.Label(status_bar, text="")
    time_label.pack(side=tk.LEFT, padx=20)

def draw_segmented_progress_bar(progress_percent):
    """Draw a segmented progress bar representing conversion progress."""
    progress_canvas.delete("all")  # Clear the canvas

    segments = 10
    segment_width = (progress_canvas.winfo_width() - (segments - 1) * 5) // segments
    gap = 5
    filled_segments = int((progress_percent / 100) * segments)

    for i in range(segments):
        color = "green" if i < filled_segments else "lightgrey"
        progress_canvas.create_rectangle(i * (segment_width + gap), 0, (i + 1) * segment_width + i * gap, 20, fill=color, outline=color)

def update_time_label(text):
    """Update the time label during conversion and clear it afterward."""
    if text:
        time_label.config(text=text)
    else:
        time_label.config(text="")

def resize_status_bar():
    """Handle dynamic resizing of the status bar."""
    window_width = progress_canvas.winfo_width()
    progress_canvas.config(width=window_width // 7)
