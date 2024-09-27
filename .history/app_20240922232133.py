import tkinter as tk
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
        convert_menu.entryconfig("Convert", state="normal")
        show_format_options(selected_file_type)  # Show format options for the file type

# Show format options based on the file type (video, audio, or image)
def show_format_options(file_type):
    if file_type == "video":
        format_options.set(['avi', 'mp4', 'mkv'])  # Video formats
    elif file_type == "audio":
        format_options.set(['mp3', 'wav', 'ogg'])  # Audio formats
    elif file_type == "image":
        format_options.set(['png', 'jpg', 'bmp'])  # Image formats

# Conversion trigger handler
def on_convert():
    if selected_file_path and selected_file_type:
        selected_format = format_dropdown.get()  # Get the selected format from dropdown
        
        # Perform conversion based on file type
        if selected_file_type == "video":
            convert_video(selected_file_path, selected_format)
        elif selected_file_type == "audio":
            convert_audio(selected_file_path, selected_format)
        elif selected_file_type == "image":
            convert_image(selected_file_path, selected_format)

# Main application setup
root = tk.Tk()
root.title("Media Converter")

# Format options
format_options = tk.StringVar(value=[])

# Format dropdown (for selecting output format)
format_dropdown = tk.OptionMenu(root, format_options, *format_options.get())
format_dropdown.pack()

# Convert button (disabled until a file is selected)
convert_menu = tk.Menu(root)
convert_menu.add_command(label="Convert", command=on_convert, state="disabled")
root.config(menu=convert_menu)

# UI setup
setup_ui(root, on_file_select, on_convert)

# Start the main loop
root.mainloop()
