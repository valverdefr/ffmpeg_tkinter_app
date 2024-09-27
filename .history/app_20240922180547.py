import tkinter as tk
from ui_helpers import create_menu, setup_ui
from status_bar import setup_status_bar
from file_handling import select_file
from conversion import start_conversion_thread

# Main application setup
root = tk.Tk()
root.title("FFmpeg Video Processor with Progress")
root.geometry("800x400")  # Start with a larger window size
root.resizable(True, True)  # Allow resizing both horizontally and vertically

# Menu setup
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
create_menu(menu_bar, root)

# Setup the UI (video bar, labels, etc.)
custom_canvas, label = setup_ui(root)

# Setup the status bar (progress bar, time label)
progress_canvas, time_label = setup_status_bar(root)

# File selection command
def open_file():
    select_file(label, custom_canvas)

# Conversion command
def convert_video():
    start_conversion_thread()

# Main event loop
root.mainloop()
