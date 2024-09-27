import tkinter as tk

custom_canvas = None  # Canvas for the large blue bar
status_label = None  # Label to display status messages
progress_bar = None  # Placeholder for the segmented progress bar

def setup_ui(root, on_file_select, on_convert):
    global custom_canvas, status_label, progress_bar

    # Set up a large blue bar canvas (for file display)
    custom_canvas = tk.Canvas(root, height=90)
    custom_canvas.pack(fill=tk.X, pady=20)  # Allow the bar to stretch

    # Set up the status label (at the bottom for progress and status text)
    status_frame = tk.Frame(root)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)

    status_label = tk.Label(status_frame, text="Ready for conversion", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Set up the segmented progress bar (inside the status bar, 1/7 of the window's width)
    progress_bar = tk.Canvas(status_frame, height=20)
    progress_bar.pack(side=tk.RIGHT, padx=10, pady=5)

def update_custom_progress_bar(file_path):
    """Update the canvas (below the menu) to show the selected file, or an empty grooved bar if no file is selected."""
    custom_canvas.delete("all")  # Clear the canvas

    # Get the current width of the window
    window_width = custom_canvas.winfo_width()

    if file_path:
        # Draw a thick light blue bar representing the file
        custom_canvas.create_rectangle(10, 10, window_width - 20, 80, fill="lightblue", outline="lightblue")
        file_name = file_path.split('/')[-1]
        custom_canvas.create_text(window_width // 2, 45, text=file_name, fill="white", font=('Arial', 14, 'bold'))
    else:
        # Draw an empty grooved bevel border when no file is selected
        custom_canvas.create_rectangle(10, 10, window_width - 20, 80, outline="lightgrey", width=3)

def update_status_bar(message, progress):
    """Update the status bar and the progress bar."""
    status_label.config(text=message)
    
    # Update the segmented progress bar
    progress_bar.delete("all")
    progress_bar_width = progress_bar.winfo_width() // 7  # One-seventh of the window width
    filled_segments = int(progress / 100 * 7)  # Calculate how many segments should be filled

    for i in range(7):
        if i < filled_segments:
            progress_bar.create_rectangle(i * progress_bar_width, 0, (i + 1) * progress_bar_width, 20, fill="green")
        else:
            progress_bar.create_rectangle(i * progress_bar_width, 0, (i + 1) * progress_bar_width, 20, outline="grey")

def reset_status_bar():
    """Reset the status bar and progress bar to default."""
    update_status_bar("Ready for conversion", 0)
