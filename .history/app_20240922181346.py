import tkinter as tk
from ui import setup_menu, setup_status_bar
from conversion import Conversion
from file_handling import FileHandler

def main():
    root = tk.Tk()
    root.title("FFmpeg Video Processor with Progress")

    # Allow resizing
    root.geometry("800x400")  # Start with a larger window size
    root.resizable(True, True)  # Allow resizing both horizontally and vertically

    # Create a FileHandler and Conversion instance
    file_handler = FileHandler(root)
    conversion_handler = Conversion(root, file_handler)

    # Setup UI components (menu, status bar)
    setup_menu(root, file_handler, conversion_handle
