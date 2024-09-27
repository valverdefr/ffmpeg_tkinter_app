import tkinter as tk

custom_canvas = None  # Canvas for the large blue bar
status_label = None  # Label to display status messages
progress_canvas = None  # Canvas for the segmented progress bar
progress_bar_value = 0  # Store the current progress for resizing

selected_file_path = None  # Declare the selected_file_path as a global variable

def setup_ui(root, on_file_select, on_convert):
    global custom_canvas, status_label, progress_canvas

    # Set up a large blue bar canvas (for file display)
    custom_canvas = tk.Canvas(root, height=90)
    custom_canvas.pack(fill=tk.X, pady=20)  # Allow the bar to stretch horizontally with the window

    # Set up the status bar (with label and segmented progress bar)
    status_bar = tk.Frame(root, relief=tk.SUNKEN, bd=1)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Progress bar on the left
    progress_canvas = tk.Canvas(status_bar, height=20, width=100)  # Initial width for the segmented bar
    progress_canvas.pack(side=tk.LEFT, padx=10, pady=5)

    # Status label on the right
    status_label = tk.Label(status_bar, text="Ready for conversion", anchor=tk.W)
    status_label.pack(side=tk.LEFT, padx=10, pady=5)

    # Bind the resize event to ensure the grooved bar resizes correctly
    root.bind("<Configure>", on_resize)

    # Initially, update the UI with no file selected
    update_custom_progress_bar()

def update_custom_progress_bar(file_path=None):
    """Update the canvas (below the menu) to show the selected file, or an empty grooved bar if no file is selected."""
    global selected_file_path
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
        custom_canvas.create_rectangle(12, 12, window_width - 22, 78, outline="darkgrey", width=1)

    custom_canvas.update_idletasks()

def on_resize(event):
    """Resize the custom progress bar when the window is resized."""
    global selected_file_path
    update_custom_progress_bar(selected_file_path)  # Redraw the grooved bar dynamically based on window size

def draw_segmented_progress_bar(progress_percent):
    """Draw a custom segmented progress bar."""
    global progress_bar_value
    progress_bar_value = progress_percent  # Store progress for redrawing on resize
    progress_canvas.delete("all")  # Clear the canvas

    segments = 10  # Number of segments
    segment_width = (progress_canvas.winfo_width() - (segments - 1) * 5) // segments  # Dynamically calculate segment width
    gap = 5  # Gap between segments
    
    # Calculate the number of filled segments based on progress percentage
    filled_segments = int((progress_percent / 100) * segments)
    
    # Draw segments on the canvas
    for i in range(segments):
        color = "green" if i < filled_segments or progress_percent == 100 else "lightgrey"
        progress_canvas.create_rectangle(i * (segment_width + gap), 0, (i + 1) * segment_width + i * gap, 20, fill=color, outline=color)

def update_status_bar(message, progress):
    """Update the status bar and the progress bar."""
    status_label.config(text=message)
    draw_segmented_progress_bar(progress)

def reset_status_bar():
    """Reset the status bar and progress bar to default."""
    update_status_bar("Ready for conversion", 0)

def resize_progress_canvas():
    """Resize the segmented progress bar to take up 1/7th of the window's width."""
    window_width = progress_canvas.winfo_width() // 7
    progress_canvas.config(width=window_width)
    draw_segmented_progress_bar(progress_bar_value)  # Redraw the progress bar after resizing
