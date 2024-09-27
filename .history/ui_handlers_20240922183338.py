import tkinter as tk
from tkinter import Menu
from status_bar import setup_status_bar, resize_status_bar, update_custom_progress_bar

custom_canvas = None  # Canvas for the large blue bar

def setup_ui(root, on_file_select, on_convert):
    global custom_canvas

    # Set up menu bar
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # File menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=on_file_select)  # File open command
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)  # Exit app

    # Edit menu with convert option
    edit_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Convert", command=on_convert, state="disabled")  # Initially disabled

    # Set up a large blue bar canvas (for file display)
    custom_canvas = tk.Canvas(root, height=90)
    custom_canvas.pack(fill=tk.X, pady=20)  # Allow the bar to stretch

    # Set up the status bar (for progress and time estimation)
    setup_status_bar(root)

    return edit_menu  # Return reference to the convert menu for enabling/disabling

def update_custom_progress_bar(file_path):
    """Update the canvas (below the menu) to show the selected file."""
    custom_canvas.delete("all")  # Clear the canvas

    # Get the current width of the window
    window_width = custom_canvas.winfo_width()

    # Draw a thick light blue bar representing the file
    if file_path:
        custom_canvas.create_rectangle(10, 10, window_width - 20, 80, fill="lightblue", outline="lightblue")
        file_name = file_path.split('/')[-1]
        custom_canvas.create_text(window_width // 2, 45, text=file_name, fill="white", font=('Arial', 14, 'bold'))
    else:
        # Draw an empty bevel border if no file is selected
        custom_canvas.create_rectangle(10, 10, window_width - 20, 80, outline="lightgrey", width=3)

def resize_ui(root):
    """Handle dynamic resizing of the custom progress bar and the status bar."""
    # Resize the large blue bar (representing the file)
    if custom_canvas:
        custom_canvas.delete("all")
        window_width = root.winfo_width()
        custom_canvas.create_rectangle(10, 10, window_width - 20, 80, fill="lightblue", outline="lightblue")
    
    # Resize the status bar
    resize_status_bar()
