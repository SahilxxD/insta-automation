from instagrapi import Client
import datetime
import os
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag

SESSION_FILE = 'session.json'
username = 'money.grenadex'
password = 'dilip1973'


def login():
    print("   [green] Initializing login... [/green]")
    api = Client()
    api.delay_range = [1, 3]
    if os.path.exists(SESSION_FILE):
        print("   [green] Logging with previous session... [/green]")
        api.load_settings(SESSION_FILE)
        # this doesn't actually login using username/password but uses the session
        api.login(username, password)
        api.dump_settings(SESSION_FILE)
        api.get_timeline_feed()
        print("   [green] Logged in successfully. [/green]")
        return api

    else:
        print("   [green] Logging with username and password... [/green]")
        api.login(username, password)
        api.dump_settings(SESSION_FILE)
        api.get_timeline_feed()
        print("   [green] Logged in successfully. [/green]")
        return api


# Trim Video for story
def trim_video(file_path, output_path, max_duration=15):
    clip = VideoFileClip(file_path)
    trimmed_clip = clip.subclip(0, max_duration)
    trimmed_clip.write_videofile(output_path)
    return output_path

# Get Video Duration


def get_video_duration(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration
    return duration


def post_to_story(api, media, media_path):
    hashtag = api.hashtag_info('like')

    duration = get_video_duration(media_path)
    # if duration > 15:
    #     media_path = trim_video(media_path,config.DOWNLOAD_DIR+os.sep+media.code+".mp4")

    media_pk = api.media_pk_from_url(
        'https://www.instagram.com/p/'+media.code+'/')

    api.video_upload_to_story(
        media_path,
        "",
        links=[
            StoryLink(webUri='https://www.instagram.com/p/'+media.code+'/')],
        hashtags=[StoryHashtag(hashtag=hashtag, x=0.23,
                               y=0.32, width=0.5, height=0.22)],
        medias=[StoryMedia(media_pk=media_pk, x=0.5,
                           y=0.5, width=0.6, height=0.8)],
    )


def upload(video_path, caption):
    api = login()
    try:
        api.delay_range = [1, 3]
        reel = api.clip_upload(
            video_path,
            caption,
            extra_data={
                # "custom_accessibility_caption": "alt text example",
                "like_and_view_counts_disabled": True,
            }
        )
        print("Reel uploaded successfully!")

        # After the reel is uploaded, upload the story linked to it
        post_to_story(api, reel, '1.mp4')

    except Exception as e:
        print(f"Exception {type(e).__name__}: {str(e)}")
        pass


def main():
    # Path to the video directory (reels folder in the same repo)
    video_dir = './reels'

    # Get the current day of the month (1-31)
    day_of_month = datetime.datetime.now().day
    print(f"Day of the month: {day_of_month}")
    # List the video files in the 'reels' directory
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

    if day_of_month <= len(video_files):
        video_path = os.path.join(video_dir, video_files[day_of_month - 1])
        caption = f"Uploading reel for day {day_of_month}."
        upload(video_path, caption)
    else:
        print("No video to upload today.")


main()
