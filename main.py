import os
import subprocess
from pathlib import Path


def main():
    # Initialize the font settings
    font_path, font_size, font_weight, font_color = accept_font_settings()
    while True:
        # Prompt for the path to the input MP4 file
        video_path = input('Input the path to your video file: ').strip('"')
        # Prompt for the  text to overlay on the GIF
        input_text = input('Input the text to overlay on the GIF: ').strip('"')

        # Prompt to change the font settings
        while True:
            override_font_settings = input('Would you like to change any font settings? (y/n): ').lower()
            if override_font_settings == 'y':
                font_path, font_size, font_weight, font_color = accept_font_settings()
                break
            elif override_font_settings == 'n':
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        output_folder = Path(video_path).parent/"Output"
        # Create the output folder if it doesn't exist
        output_folder.mkdir(exist_ok=True)
        # The output GIF file name is the same as the input video path but with a .gif extension
        output_gif_path = output_folder / Path(video_path).with_suffix('.gif').name
        # The base name for the output frames
        frame_base_name = 'frame_'
        # The prefix for the output frames
        output_frame_prefix = 'output'

        video_frames = convert_video_to_frames(frame_base_name, video_path)
        overlay_text_on_video_frames(video_frames, output_frame_prefix, font_path, font_size, font_weight, font_color, input_text)
        create_gif_from_frames(frame_base_name, output_frame_prefix, output_gif_path)
        cleanup_frames(video_frames, output_frame_prefix)

        # Ask the user if they want to process another GIF
        while True:
            another = input('Do you want to process another GIF? (y/n): ').lower()
            if another == 'y':
                break
            elif another == 'n':
                return
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


def convert_video_to_frames(frame_base_name, video_path):
    # Extract frames from the MP4 file
    subprocess.run(['ffmpeg', '-i', video_path, '-vf', 'fps=30', f"{frame_base_name}%04d.png"])

    # Get the list of extracted frames
    return list(Path('.').glob(f"{frame_base_name}*.png"))


def overlay_text_on_video_frames(video_frames, output_frame_prefix,
                                 font_path, font_size, font_weight, font_color, input_text):
    # Apply localized text to each frame with centered alignment
    for frame in video_frames:
        output_frame = f"{output_frame_prefix}_{frame.name}"
        subprocess.run(
            ['magick', frame.name, '-font', font_path, '-pointsize', font_size, '-weight', font_weight, '-fill',
             font_color, '-gravity', 'center', '-draw', f"text 0,0 '{input_text}'", output_frame])


def create_gif_from_frames(frame_base_name, output_frame_prefix, output_gif):
    # Reassemble the frames into a GIF
    subprocess.run(['magick', '-delay', '3', '-loop', '0', f"{output_frame_prefix}_{frame_base_name}*.png",
                    '-colors', '32', output_gif])


def accept_font_settings():
    font_path = input('Input the path to your font file: ').strip('"')
    font_size = input('Input the font size: ').strip('"')
    font_weight = input('Input the font weight: ').strip('"')
    font_color = input('Input the font color: ').strip('"')
    return font_path, font_size, font_weight, font_color


def cleanup_frames(video_frames, output_frame_prefix):
    # Optional: Clean up the intermediate frame files
    for frame in video_frames:
        frame.unlink()
    for frame in Path('.').glob(f"{output_frame_prefix}_*.png"):
        frame.unlink()


if __name__ == "__main__":
    main()
