import os
import subprocess
from pathlib import Path


def main():
    # Prompt for the path to the input MP4 file
    input_video = input('Input the path to your video file: ')

    # The output GIF file name is the same as the input video path but with a .gif extension
    output_gif = Path(input_video).with_suffix('.gif')
    # The base name for the output frames
    frame_base_name = 'frame_'
    # Prompt for the localized text to overlay on the GIF
    localized_text = input('Input your localized text: ')
    # Font settings for ImageMagick
    font = 'C:\\Users\\Thomas\\AppData\\Local\\Microsoft\\Windows\\Fonts\\CourierPrime-Bold.ttf'
    font_size = '34'
    font_weight = 'bold'
    text_color = '#00ff9b'
    # Position for the text
    position = '10,20'


def convert_video_to_frames(frame_base_name, video_path):
    # Extract frames from the MP4 file
    subprocess.run(['ffmpeg', '-i', video_path, '-vf', 'fps=10', f"{frame_base_name}%04d.png"])

    # Get the list of extracted frames
    return list(Path('.').glob(f"{frame_base_name}*.png"))


def overlay_text_on_video_frames(video_frames, font_path, font_size, font_weight, text_color, text):
    # Apply localized text to each frame with centered alignment
    for frame in video_frames:
        localized_frame = f"localized_{frame.name}"
        subprocess.run(
            ['magick', frame.name, '-font', font_path, '-pointsize', font_size, '-weight', font_weight, '-fill',
             text_color, '-gravity', 'center', '-draw', f"text 0,0 '{text}'", localized_frame])


def create_gif_from_frames(frame_base_name, output_gif):
    # Reassemble the frames into a GIF
    subprocess.run(['magick', '-delay', '10', '-loop', '0', f"localized_{frame_base_name}*.png", output_gif])


def cleanup_frames(video_frames):
    # Optional: Clean up the intermediate frame files
    for frame in video_frames:
        frame.unlink()
    for frame in Path('.').glob("localized_*.png"):
        frame.unlink()


if __name__ == "__main__":
    main()
