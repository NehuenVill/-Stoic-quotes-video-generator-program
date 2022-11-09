import pyttsx3
import requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips
from moviepy.video.fx import all
from os import listdir
from os.path import isfile, join
from random import randint

api = 'https://api.themotivate365.com/stoic-quote'

def get_quote(url:str) -> list:

    req = requests.get(url)

    api_res = req.json()

    quote = api_res['quote']

    author = api_res['author']

    return [quote, author]

def create_audio(quote:str = None) -> str:

    ts = pyttsx3.init()

    voices = ts.getProperty('voices')

    voices = [voice.id for voice in voices]

    ts.setProperty('voice', voices[2])

    files = [f for f in listdir('Audios') if isfile(join('Audios', f))]

    if files:

        last_file_num = int(files[len(files)-1].replace('voice_', '').replace('.mp3', ''))

        audio_file = f'voice_{last_file_num + 1}.mp3'
    
    else:

        audio_file = 'voice_1.mp3'

    ts.save_to_file(quote, audio_file)

    return audio_file


def create_video(quote:str, author:str, audio:str) -> None:

    clip = VideoFileClip(f"Videos/bg_videos/bg_{randint(1, 6)}.mp4")

    clip = clip.volumex(0)

    full_text = f"""

{quote}

-{author}
                
                """

    duration = clip.duration

    if duration >= 10:

        random_start = randint(0, duration-10)

        end = random_start + 10

        clip = clip.subclip(random_start, end)

    else:

        print('Too short background video, better delete.')

    clip = all.resize(clip, width=1080, height=1920)

    clip = clip.set_opacity(0.5)

    txt_clip = TextClip(full_text, fontsize=80, color='black', font='Vivaldi-Cursiva')

    txt_clip = txt_clip.set_pos('center').set_duration(10)

    audioclip = AudioFileClip(f'Audios/{audio}')

    silence_clip = AudioFileClip('Audios/silence/silence.mp3')

    final_audio = concatenate_audioclips([silence_clip, audioclip])

    clip = clip.set_audio(final_audio)

    video = CompositeVideoClip([clip, txt_clip])

    video.write_videofile("Videos/finished_videos/video_1.mp4")


if __name__ == '__main__':

    create_audio()