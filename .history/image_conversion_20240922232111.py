import subprocess

def convert_image(file_path, output_format="png"):
    """Convert image file to the specified format using FFmpeg."""
    output_file = file_path.rsplit('.', 1)[0] + f"_output.{output_format}"
    
    # Command to convert image
    command = ['ffmpeg', '-i', file_path, output_file]
    subprocess.run(command, check=True)
    
    return output_file
