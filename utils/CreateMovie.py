from moviepy.editor import *
import random
import os
from os import walk

filenames = next(walk('./Music'), (None, None, []))[2]  # [] if no file

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def GetDaySuffix(day):
    if day == 1 or day == 21 or day == 31:
        return "st"
    elif day == 2 or day == 22:
        return "nd"
    elif day == 3 or day == 23:
        return "rd"
    else:
        return "th"

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
music_path = os.path.join(dir_path, "Music/")
assets_path = os.path.join(dir_path, "assets/")

def add_return_comment(comment):
    need_return = 30
    new_comment = ""
    return_added = 0
    return_added += comment.count('\n')
    for i, letter in enumerate(comment):
        if i > need_return and letter == " ":
            letter = "\n"
            need_return += 30
            return_added += 1
        new_comment += letter
    return new_comment, return_added
        

class CreateMovie():

    @classmethod
    def CreateMP4(cls, post_data):
        video = VideoFileClip(os.path.join(assets_path, "base.mp4"))
        print(post_data)
        clips = []
        for i, post in enumerate(post_data):
            if "gif" not in post['image_path']:
                clip = ImageClip(post['image_path']).set_duration(12).set_position(("center",261)).set_start((0, (i * 12)))
                clips.append(clip)
            else:
                clip = VideoFileClip(post['image_path'])
                clip_lengthener = [clip] * 60
                clip = concatenate_videoclips(clip_lengthener)
                clip = clip.subclip(0,12)
                clip = clip.set_start((0, (i * 12)))
                clip = clip.set_position(("center",261))
                clips.append(clip)
        
        # After we have out clip.

        # Hack to fix getting extra frame errors??
        # clip = clips.subclip(0,36)

        text_clips = []
        notification_sounds = []
        for i, post in enumerate(post_data):
            return_comment, return_count = add_return_comment(post['Best_comment'])
            txt = TextClip(return_comment, font='Arial-Bold', stroke_color='white', stroke_width=1,
                        fontsize=38, color="white")
            # txt = txt.on_color(col_opacity=0.1)
            txt = txt.set_position(("center",1586))
            txt = txt.set_start((0, 3 + (i * 12))) # (min, s)
            txt = txt.set_duration(7)
            txt = txt.crossfadein(0.5)
            txt = txt.crossfadeout(0.5)
            text_clips.append(txt)
            notification = AudioFileClip(os.path.join(assets_path, f"notification.mp3"))
            notification = notification.set_start((0, 3 + (i * 12)))
            notification_sounds.append(notification)
        
        music_file = os.path.join(music_path, random.choice(filenames))
        music = AudioFileClip(music_file)
        music = music.set_start((0,0))
        music = music.volumex(.4)
        music = music.set_duration(36)

        new_audioclip = CompositeAudioClip([music]+notification_sounds)
        # clip.write_videofile(f"video_clips.mp4", fps = 24)
        print(clips)
        # clip = VideoFileClip("video_clips.mp4", audio=False)
        clip = CompositeVideoClip([video] + clips + text_clips)
        clip.audio = new_audioclip
        clip.write_videofile("video.mp4", fps = 24)

        
        if os.path.exists(os.path.join(dir_path, "video_clips.mp4")):
            os.remove(os.path.join(dir_path, "video_clips.mp4"))
        else:
            print(os.path.join(dir_path, "video_clips.mp4"))

if __name__ == '__main__':
    print(TextClip.list('color'))