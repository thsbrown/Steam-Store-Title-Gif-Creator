# Overview
This is a simple script that allows you to create a gif from a video file with text overlayed on top of it. It uses [ImageMagick](https://www.imagemagick.org/script/index.php) to create the gif and [ffmpeg](https://www.ffmpeg.org/) to extract the frames from the video file. The main purpose for writing this script was to create text header gifs that can easily localized for the steam About this section of a game.

# Quick Start
1. Run `python main.py`.
2. Enter path to font file you want to use.
3. Enter font settings (font size, font weight, font color, etc.).
4. Enter video file path to create gif from.
5. Enter text to overlay.

# Output
## Run Demo
https://github.com/thsbrown/Steam-Store-Title-Gif-Creator/assets/2967721/0d313191-3afd-4b53-a565-14548c8fb4b9
## Before
https://github.com/thsbrown/Steam-Store-Title-Gif-Creator/assets/2967721/9117c689-8453-43a5-b63f-285ee5d5e121
## After
![Header Background Meteors Loop 3](https://github.com/thsbrown/Steam-Store-Title-Gif-Creator/assets/2967721/2ed2dbc0-9fff-4355-830f-ec220a5e2225)

# TODO
- [ ] font weight doesn't work when specifying font path.
- [ ] allow specifying custom fps, right now defaults to 30.
- [ ] allow specifying custom optimization percentage level (fuzz defaults to 7%).
- [ ] allow custom output path.
- [ ] allow for custom text position, (always defaults to center vertically and horizontally).
- [ ] allow for specifying csv file with video input and text to overlay. ("video.mp4", "text" \n "video2.mp4", "text2")
