import tkinter as tk
from ui_handlers import setup_ui, resize_ui, update_custom_progress_bar  # Import update_custom_progress_bar
from file_handling import select_file
from conversion import start_conversion_thread

# Initialize the root window
root = tk.Tk()
root.title("FFmpeg Video Processor")

# Global variable to store the selected file path
selected_file_path = None

# File selection handler
def on_file_select():
    global selected_file_path
    selected_file_path = select_file()  # Select file and store the path
    if selected_file_path:
        # Enable the Convert option when a file is selected
        convert_menu.entryconfig("Convert", state="normal")
        # Update the blue bar to reflect the selected file (below the menu)
        update_custom_progress_bar(selected_file_path)

# Conversion trigger handler
def on_convert():
    if selected_file_path:
        start_conversion_thread(selected_file_path=selected_file_path)

# Allow resizing
root.geometry("800x400")  # Starting window size
root.resizable(True, True)  # Allow resizing

# Set up the UI (menus, status bar, and the file display blue bar)
convert_menu = setup_ui(root, on_file_select, on_convert)

# Bind keys for fullscreen and window resizing events
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Configure>", lambda event: resize_ui(root, selected_file_path))  # Pass selected_file_path

# Start the main event loop
root.mainloop()
