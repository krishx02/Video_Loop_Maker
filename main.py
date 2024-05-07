import yt_dlp
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.fx import fadein, fadeout

def download_audio_from_youtube(url, output_filename):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': "C:\\ProgramData\\chocolatey\\lib\\ffmpeg-full\\tools\\ffmpeg\\bin",  # Specify the path to ffmpeg
        'outtmpl': output_filename,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
        ydl.download([url])

def loop_audio(audio, duration, fade_duration):
    looped_audio = AudioSegment.empty()
    total_duration = 0
    while total_duration < duration:
        looped_audio += audio.fade_in(fade_duration).fade_out(fade_duration)
        total_duration += len(audio)
    return looped_audio[:duration]

# Example usage:
url = 'https://www.youtube.com/watch?v=f8mL0_4GeV0'
output_filename = 'song'
download_audio_from_youtube(url, output_filename)

# Example usage:
audio_file = "song.mp3"
output_filename = "looped_audio.mp3"
audio = AudioSegment.from_mp3(audio_file)
looped_audio = loop_audio(audio, duration=100000, fade_duration=1)  # Loop for one hour (3600000 milliseconds) with 2-second fade
looped_audio.export(output_filename, format="mp3")

# Load the existing video
existing_video = VideoFileClip("existing_video.mkv")  # Replace with your existing video file

# Load the audio you created
audio_clip = AudioFileClip("looped_audio.mp3")  # Replace with the audio you created

# Set the duration of the video to be one hour
desired_duration = 20  # Duration in seconds (one hour)
existing_video_duration = existing_video.duration
existing_video = existing_video.set_duration(desired_duration)

# Overlay the existing video with the audio
final_video = existing_video.set_audio(audio_clip)

# Add fade-in and fade-out effects
fade_duration = 3  # Duration of the fade effect in seconds

if existing_video_duration < desired_duration:
    # Calculate the number of times the video needs to be looped
    num_loops = int(desired_duration / existing_video_duration)
    
    # Loop the video using the loop method
    final_video = final_video.loop(n=num_loops)

# Export the final video file
final_video.write_videofile("output.mp4", codec="libx264", fps=existing_video.fps)  # Use the same codec and fps as the existing video