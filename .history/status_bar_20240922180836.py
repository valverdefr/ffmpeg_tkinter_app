import tkinter as tk

def setup_status_bar(root):
    """Create the status bar with progress bar and time label."""
    status_bar = tk.Frame(root, relief=tk.SUNKEN, bd=1)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    progress_canvas = tk.Canvas(status_bar, width=100, height=20)
    progress_canvas.pack(side=tk.LEFT, padx=20, pady=5)

    time_label = tk.Label(status_bar, text="Estimated time remaining: N/A")
    time_label.pack(side=tk.LEFT, padx=20)

    return progress_canvas, time_label

def update_time_label(current_seconds, duration, time_label, start_time):
    """Update the time label with remaining time."""
    elapsed_time = time.time() - start_time
    remaining_time = ((elapsed_time / current_seconds) * duration) - elapsed_time
    time_label.config(text=f"Estimated time remaining: {int(remaining_time)} seconds")
