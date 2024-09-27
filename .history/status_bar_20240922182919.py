import tkinter as tk

progress_canvas = None
time_label = None
selected_file_path = None  # To store selected file path for display

def setup_status_bar(root):
    global progress_canvas, time_label

    # Create status bar
    status_bar = tk.Frame(root, relief=tk.SUNKEN, bd=1)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Set up custom progress bar (for file display)
    progress_canvas = tk.Canvas(status_bar, height=90)
    progress_canvas.pack(fill=tk.X, padx=20, pady=5)  # Allow the bar to stretch

    # Set up time label (for conversion time estimate)
    time_label = tk.Label(status_bar, text="Estimated time remaining: N/A")
    time_label.pack(side=tk.LEFT, padx=20)

def update_custom_progress_bar(file_path):
    """Update the canvas to show the selected file."""
    global selected_file_path
    selected_file_path = file_path

    progress_canvas.delete("all")  # Clear the canvas

    # Get the current width of the window
    window_width = progress_canvas.winfo_width()

    # Draw a thick light blue bar representing the file
    if selected_file_path:
        progress_canvas.create_rectangle(10, 10, window_width - 20, 80, fill="lightblue", outline="lightblue")
        file_name = selected_file_path.split('/')[-1]
        progress_canvas.create_text(window_width // 2, 45, text=file_name, fill="white", font=('Arial', 14, 'bold'))
    else:
        # Draw an empty bevel border if no file is selected
        progress_canvas.create_rectangle(10, 10, window_width - 20, 80, outline="lightgrey", width=3)

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
    """Update the time label with remaining time or conversion complete message."""
    time_label.config(text=text)

def resize_status_bar():
    """Handle dynamic resizing of the custom progress bar."""
    if selected_file_path:
        update_custom_progress_bar(selected_file_path)
