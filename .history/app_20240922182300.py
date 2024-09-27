import tkinter as tk
from ui_handlers import setup_ui, resize_ui
from file_handling import select_file
from conversion import start_conversion_thread

# Initialize the root window
root = tk.Tk()
root.title("FFmpeg Video Processor")

# Allow resizing
root.geometry("800x400")  # Starting window size
root.resizable(True, True)  # Allow resizing

# Set up the UI (menus, status bar, etc.)
setup_ui(root, select_file, start_conversion_thread)

# Bind keys for fullscreen and window resizing events
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Configure>", lambda event: resize_ui(root))  # Update only layout dynamically

# Start the main event loop
root.mainloop()
