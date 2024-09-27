import os
import tkinter as tk
from tkinter import Menu, messagebox
from file_handling import select_file, get_file_type
from video_conversion import convert_video
from audio_conversion import convert_audio
from image_conversion import convert_image
from ui_handlers import setup_ui, update_custom_progress_bar, update_status_bar, reset_status_bar

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
        reset_status_bar()  # Reset the status bar when a new file is selected
        clear_edit_menu()  # Clear the previous menu options
        update_format_menu(selected_file_type)  # Show format options in the "Edit" menu
    else:
        update_custom_progress_bar(None)  # Show empty grooved bar when no file is selected

# Clear the Edit menu
def clear_edit_menu():
    edit_menu.delete(0, "end")  # Clear all menu items

# Confirmation dialog before starting conversion
def show_confirmation_dialog(file_path, output_format):
    file_name = file_path.split('/')[-1]
    confirm_message = f"Do you wish to convert '{file_name}' to {output_format.upper()}?"
    return messagebox.askyesno("Confirm Conversion", confirm_message)

# Check for file overwriting and show confirmation
def check_overwrite(output_file):
    if os.path.exists(output_file):
        return messagebox.askyesno("File Exists", f"'{output_file}' already exists. Do you want to overwrite it?")
    return True

# Conversion trigger handler (directly triggered by selecting format in Edit menu)
def on_convert(format_to_convert):
    if selected_file_path and selected_file_type:
        # Show confirmation dialog
        confirm = show_confirmation_dialog(selected_file_path, format_to_convert)
        if confirm:
            # Determine output file name
            output_file = f"{selected_file_path.rsplit('.', 1)[0]}_output.{format_to_convert}"
            if check_overwrite(output_file):  # Check if file exists and confirm overwriting
                update_status_bar("Conversion started...", 0)  # Update status bar
                if selected_file_type == "video":
                    convert_video(selected_file_path, format_to_convert)
                elif selected_file_type == "audio":
                    convert_audio(selected_file_path, format_to_convert)
                elif selected_file_type == "image":
                    convert_image(selected_file_path, format_to_convert)
                update_status_bar("Conversion complete!", 100)  # Show completion status

# Update the format options in the "Edit" menu based on file type
def update_format_menu(file_type):
    clear_edit_menu()  # Clear any previous options
    file_extension = selected_file_path.split('.')[-1].lower()

    if file_type == "video":
        if file_extension != "avi":
            edit_menu.add_command(label="Convert to AVI", command=lambda: on_convert('avi'))
        if file_extension != "mkv":
            edit_menu.add_command(label="Convert to MKV", command=lambda: on_convert('mkv'))

    elif file_type == "audio":
        if file_extension != "mp3":
            edit_menu.add_command(label="Convert to MP3", command=lambda: on_convert('mp3'))
        if file_extension != "wav":
            edit_menu.add_command(label="Convert to WAV", command=lambda: on_convert('wav'))
        if file_extension != "ogg":
            edit_menu.add_command(label="Convert to OGG", command=lambda: on_convert('ogg'))

    elif file_type == "image":
        if file_extension != "png":
            edit_menu.add_command(label="Convert to PNG", command=lambda: on_convert('png'))
        if file_extension != "jpg":
            edit_menu.add_command(label="Convert to JPG", command=lambda: on_convert('jpg'))
        if file_extension != "bmp":
            edit_menu.add_command(label="Convert to BMP", command=lambda: on_convert('bmp'))

# Main application setup
root = tk.Tk()
root.title("Media Converter")
root.state('zoomed')  # Full-size window on startup

# Setup Menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=on_file_select)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Edit menu (with format options)
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# UI setup
setup_ui(root, on_file_select, on_convert)

# Start the main loop
root.mainloop()
