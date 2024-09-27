import tkinter as tk
from tkinter import Menu
from status_bar import setup_status_bar, resize_status_bar

def setup_ui(root, on_file_select, on_convert):
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

    # Set up status bar
    setup_status_bar(root)

    return edit_menu  # Return reference to the convert menu for enabling/disabling

def resize_ui(root):
    # Handle dynamic UI resizing (e.g., resizing the status bar)
    resize_status_bar()
