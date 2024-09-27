import subprocess

def convert_audio(file_path, output_format="mp3"):
    """Convert audio file to the specified format using FFmpeg."""
    output_file = file_path.rsplit('.', 1)[0] + f"_output.{output_format}"
    
    # Command to convert audio with overwrite enabled
    command = ['ffmpeg', '-y', '-i', file_path, output_file]
    
    # Run the FFmpeg command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error during audio conversion: {e}")
    
    return output_file
