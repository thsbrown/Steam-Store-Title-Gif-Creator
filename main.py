import os
import subprocess
from pathlib import Path


def main():
    # Prompt for the path to the input MP4 file
    video_path = input('Input the path to your video file (no quotes): ')
    # Prompt for the  text to overlay on the GIF
    input_text = input('Input the text to overlay on the GIF (no quotes): ')

    # The output GIF file name is the same as the input video path but with a .gif extension
    output_gif_path = Path(video_path).with_suffix('.gif')
    # The base name for the output frames
    frame_base_name = 'frame_'
    # The prefix for the output frames
    output_frame_prefix = 'output'

    # Font settings for ImageMagick
    font_path = "C:/Users/Thomas/AppData/Local/Microsoft/Windows/Fonts/CourierPrime-Bold.ttf"
    font_size = '34'
    font_weight = 'bold'
    text_color = '#00ff9b'

    video_frames = convert_video_to_frames(frame_base_name, video_path)
    overlay_text_on_video_frames(video_frames, output_frame_prefix, font_path, font_size, font_weight, text_color, input_text)
    create_gif_from_frames(frame_base_name, output_frame_prefix, output_gif_path)
    cleanup_frames(video_frames, output_frame_prefix)


def convert_video_to_frames(frame_base_name, video_path):
    # Extract frames from the MP4 file
    subprocess.run(['ffmpeg', '-i', video_path, '-vf', 'fps=10', f"{frame_base_name}%04d.png"])

    # Get the list of extracted frames
    return list(Path('.').glob(f"{frame_base_name}*.png"))


def overlay_text_on_video_frames(video_frames, output_frame_prefix,
                                 font_path, font_size, font_weight, text_color, input_text):
    # Apply localized text to each frame with centered alignment
    for frame in video_frames:
        output_frame = f"{output_frame_prefix}_{frame.name}"
        subprocess.run(
            ['magick', frame.name, '-font', font_path, '-pointsize', font_size, '-weight', font_weight, '-fill',
             text_color, '-gravity', 'center', '-draw', f"text 0,0 '{input_text}'", output_frame])


def create_gif_from_frames(frame_base_name, output_frame_prefix, output_gif):
    # Reassemble the frames into a GIF
    subprocess.run(['magick', '-delay', '10', '-loop', '0', f"{output_frame_prefix}_{frame_base_name}*.png", output_gif])


def cleanup_frames(video_frames, output_frame_prefix):
    # Optional: Clean up the intermediate frame files
    for frame in video_frames:
        frame.unlink()
    for frame in Path('.').glob(f"{output_frame_prefix}_*.png"):
        frame.unlink()


if __name__ == "__main__":
    main()
