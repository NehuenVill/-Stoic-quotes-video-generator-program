import pyttsx3
import requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx import all

api = 'https://api.themotivate365.com/stoic-quote'

def get_quote(url:str) -> list:

    req = requests.get(url)

    api_res = req.json()

    quote = api_res['quote']

    author = api_res['author']

    return [quote, author]

def create_audio(quote:str = None) -> None:

    ts = pyttsx3.init()

    voices = ts.getProperty('voices')

    voices = [voice.id for voice in voices]

    ts.setProperty('voice', voices[2])

    ts.save_to_file(quote, 'voice_1.mp3')

    

def create_video(quote:str, author:str) -> None:

    clip = VideoFileClip("Videos/bg_videos/bg_1.mp4")

    clip = clip.volumex(0.8)

    full_text = f"""

{quote}

-{author}
                
                """

    clip = all.resize(clip, width=1080, height=1920)

    clip = clip.set_opacity(0.5)

    txt_clip = TextClip(full_text, fontsize=80, color='black', font='Vivaldi-Cursiva')

    txt_clip = txt_clip.set_pos('center').set_duration(10)

    video = CompositeVideoClip([clip, txt_clip])

    video.write_videofile("Videos/finished_videos/video_1.mp4")


if __name__ == '__main__':

    create_audio()