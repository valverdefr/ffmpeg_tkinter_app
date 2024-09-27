import tkinter as tk

custom_canvas = None  # Canvas for the large blue bar

def setup_ui(root, on_file_select, on_convert):
    global custom_canvas

    # Set up menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=on_file_select)  # File open command
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)  # Exit app

    # Edit menu with convert option
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Convert", command=on_convert, state="disabled")  # Initially disabled

    # Set up a large blue bar canvas (for file display)
    custom_canvas = tk.Canvas(root, height=90)
    custom_canvas.pack(fill=tk.X, pady=20)  # Allow the bar to stretch

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
