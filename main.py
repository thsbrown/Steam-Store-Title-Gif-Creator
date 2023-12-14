import os
import subprocess
from pathlib import Path

# Prompt for the path to the input MP4 file
input_video = input('Input the path to your video file: ')
# The base name for the output frames
frame_base_name = 'frame_'
# The output GIF file name is the same as the input video path but with a .gif extension
output_gif = Path(input_video).with_suffix('.gif')
# Prompt for the localized text to overlay on the GIF
localized_text = input('Input your localized text: ')
# Font settings for ImageMagick
font = 'C:\\Users\\Thomas\\AppData\\Local\\Microsoft\\Windows\\Fonts\\CourierPrime-Bold.ttf'
font_size = '34'
font_weight = 'bold'
text_color = '#00ff9b'
# Position for the text
position = '10,20'

# Extract frames from the MP4 file
subprocess.run(['ffmpeg', '-i', input_video, '-vf', 'fps=10', f"{frame_base_name}%04d.png"])

# Get the list of extracted frames
frames = list(Path('.').glob(f"{frame_base_name}*.png"))

# Apply localized text to each frame with centered alignment
for frame in frames:
    localized_frame = f"localized_{frame.name}"
    subprocess.run(['magick', frame.name, '-font', font, '-pointsize', font_size, '-weight', font_weight, '-fill', text_color, '-gravity', 'center', '-draw', f"text 0,0 '{localized_text}'", localized_frame])

# Reassemble the frames into a GIF
subprocess.run(['magick', '-delay', '10', '-loop', '0', f"localized_{frame_base_name}*.png", output_gif])

# Optional: Clean up the intermediate frame files
for frame in frames:
    frame.unlink()
for frame in Path('.').glob("localized_*.png"):
    frame.unlink()
