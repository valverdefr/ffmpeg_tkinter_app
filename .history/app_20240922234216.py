import tkinter as tk
from tkinter import Menu, messagebox
from file_handling import select_file, get_file_type
from video_conversion import convert_video
from audio_conversion import convert_audio
from image_conversion import convert_image
from ui_handlers import setup_ui, update_custom_progress_bar

# Global variables to store selected file and file type
selected_file_path = None
selected_file_type = None

# File selection handler
def on_file_select():
    global selected_file_path, selected_file_type
    selected_file_path = select_file()  # Open file dialog
    if selected_file_path:
        selected_file_type = get_file_type(selected_file_path)  # Determine file type
        update_custom_progress_bar(selected_file_path)  # Update the large blue bar with file info
        # Enable the Convert option after a file is selected
        edit_menu.entryconfig("Convert", state="normal")
        update_format_menu(selected_file_type)  # Show format options in the "Edit" menu

# Update the format options in the "Edit" menu based on file type
def update_format_menu(file_type):
    edit_menu.delete(2, "end")  # Remove any previous format entries
    if file_type == "video":
        for format_option in ['avi', 'mkv']:  # Exclude 'mp4' for mp4 files
            edit_menu.add_radiobutton(label=f"Convert to {format_option.upper()}", variable=selected_format, value=format_option)
        selected_format.set('avi')  # Default format for video conversion
    elif file_type == "audio":
        for format_option in ['mp3', 'wav', 'ogg']:  # Exclude the same format
            edit_menu.add_radiobutton(label=f"Convert to {format_option.upper()}", variable=selected_format, value=format_option)
        selected_format.set('mp3')  # Default format for audio
    elif file_type == "image":
        for format_option in ['png', 'jpg', 'bmp']:  # Exclude the same format
            edit_menu.add_radiobutton(label=f"Convert to {format_option.upper()}", variable=selected_format, value=format_option)
        selected_format.set('png')  # Default format for image

# Confirmation dialog before starting conversion
def show_confirmation_dialog(file_path, output_format):
    file_name = file_path.split('/')[-1]
    confirm_message = f"Do you wish to convert '{file_name}' to {output_format.upper()}?"
    return messagebox.askyesno("Confirm Conversion", confirm_message)

# Conversion trigger handler
def on_convert():
    if selected_file_path and selected_file_type:
        format_to_convert = selected_format.get()  # Get the selected format from the Edit menu
        
        # Show confirmation dialog
        confirm = show_confirmation_dialog(selected_file_path, format_to_convert)
        if confirm:
            # Perform conversion based on file type
            if selected_file_type == "video":
                convert_video(selected_file_path, format_to_convert)
            elif selected_file_type == "audio":
                convert_audio(selected_file_path, format_to_convert)
            elif selected_file_type == "image":
                convert_image(selected_file_path, format_to_convert)

# Main application setup
root = tk.Tk()  # Initialize the root window first
root.title("Media Converter")

# Now initialize the selected format variable after the root window is created
selected_format = tk.StringVar(value="")

# Setup Menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=on_file_select)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Edit menu (with format and convert options)
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Convert", command=on_convert, state="disabled")  # Initially disabled

# UI setup
setup_ui(root, on_file_select, on_convert)

# Start the main loop
root.mainloop()
