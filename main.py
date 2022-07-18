"""
This is the main loop file for our AutoTube Bot!

Quick notes!
- Currently it's set to try and post a video then sleep for a day.
- You can change the size of the video currently it's set to post shorts.
    * Do this by adding a parameter of scale to the image_save function.
    * scale=(width,height)
"""

from datetime import date
import time  
from utils.CreateMovie import CreateMovie, GetDaySuffix
from utils.RedditBot import RedditBot
from utils.upload_video import upload_video

#Create Reddit Data Bot
redditbot = RedditBot()

part_counter = 1

# Leave if you want to run it 24/7
while True:
    # Gets our new posts pass if image related subs. Default is memes
    posts = redditbot.get_posts("Animemes") + redditbot.get_posts("AnimeFunny") + redditbot.get_posts("animememes")

    # Create folder if it doesn't exist
    redditbot.create_data_folder()

    # Go through posts and find 5 that will work for us.
    for post in posts:
        redditbot.save_image(post)

    # Wanted a date in my titles so added this helper
    DAY = date.today().strftime("%d")
    DAY = str(int(DAY)) + GetDaySuffix(int(DAY))
    dt_string = date.today().strftime("%A %B") + f" {DAY}"

    # Create the movie itself!
    CreateMovie.CreateMP4(redditbot.post_data)

    # Video info for YouTube.
    # This example uses the first post title.
    video_data = {
            "file": "video.mp4",
            "title": f"Posting Anime memes cuz I'm bored - part #{part_counter}!",
            "description": "#shorts #anime #animememes #animemes #memes #meme\n\nGiving you the hottest anime memes of the day with funny comments!",
            "keywords":"meme,memems,anime,funny",
            "privacyStatus":"public"
    }

    print(video_data["title"])
    print("Posting Video in 5 minutes...")
    time.sleep(60)
    upload_video(video_data)

    # Update counter
    part_counter = part_counter + 1

    # Sleep until ready to post another video!
    time.sleep(60 * 60 * 3 - 1)
