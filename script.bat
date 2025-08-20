@echo off
REM Create output folder if it doesn't exist
if not exist output mkdir output

REM LinkedIn Landscape
ffmpeg -i v1.mp4 -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:a copy output/v1_linkedin.mp4

REM LinkedIn Square
ffmpeg -i v1.mp4 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" -c:a copy output/v1_linkedin_square.mp4

REM Twitter Landscape (Full HD)
ffmpeg -i v1.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:a copy output/v1_twitterland.mp4

REM Instagram Portrait
ffmpeg -i v1.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:a copy output/v1_instagram.mp4

REM YouTube (Full HD Landscape)
ffmpeg -i v1.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:a copy output/v1_youtube.mp4

echo.
echo ✅ All videos converted and saved in the "output" folder.
pause
