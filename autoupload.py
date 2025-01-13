from instagrapi import Client
import datetime
import os
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
import random

SESSION_FILE = 'session.json'
# Access environment variables for Instagram credentials
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


def post_to_story(api, media, media_path):
    hashtag = api.hashtag_info('like')

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


def upload(video_path, hashtags):
    api = login()
    captions = [
        "🐾 Love animals? Follow for daily heartwarming pet videos that will make your day! 🐶🐱",
        "😊 Want to smile every day? Follow us for the cutest animal moments on Instagram! 🐕🐈",
        "🐾 Get your daily dose of adorable pets! Follow now and join our animal-loving community! 🐾💖",
        "🐕 Can't get enough of cute animals? Follow for non-stop furry fun! 🐾🎉",
        "🐶 Join our tribe of animal lovers! Follow for daily paw-some videos! 🐾🐕",
        "🌟 Follow us and turn your feed into a haven of cuteness and joy! 🐾🐱",
        "📣 Missing out on these adorable moments? Follow now to stay updated! 🐕🐾",
        "🐾 Click that follow button for endless animal cuteness and fun! 🐶🐱",
        "😊 Need more joy in your life? Follow us for daily pet happiness! 🐾💖",
        "🐕 Follow now to fill your feed with furry friends and adorable antics! 🐾🐈",
        "🐾 Be the first to see our cutest pet videos! Hit follow and never miss out! 🐕🎥",
        "😊 Your daily smile starts here! Follow for the cutest pets on Instagram! 🐾🐶",
        "🐾 Looking for daily cheer? Follow us and get a front-row seat to pet cuteness! 🐕🐱",
        "🌟 Brighten your day with adorable animal videos! Follow us for daily updates! 🐾🐈",
        "🐾 Ready for a cuteness overload? Follow now and let the fun begin! 🐶🎉"
    ]
    # Select one random caption
    random_caption = random.choice(captions)
    try:
        # Randomly select 10 hashtags
        selected_hashtags = random.sample(hashtags, 10)
        hashtags_str = ' '.join(selected_hashtags)

        # Add the hashtags to the caption
        caption_with_hashtags = f"{random_caption} {hashtags_str}"

        api.delay_range = [1, 3]
        reel = api.clip_upload(
            video_path,
            caption_with_hashtags,
            extra_data={
                # "custom_accessibility_caption": "alt text example",
                "like_and_view_counts_disabled": True,
            }
        )
        print("Reel uploaded successfully!")

        # After the reel is uploaded, upload the story linked to it
        post_to_story(api, reel, video_path)

    except Exception as e:
        print(f"Exception {type(e).__name__}: {str(e)}")
        pass


def main():
    # Path to the video directory (reels folder in the same repo)
    video_dir = './reels'

    hashtags = [
        "#CuteAnimals",
        "#FunnyAnimals",
        "#AnimalVideos",
        "#PetLovers",
        "#PetsofIG",
        "#AdorablePets",
        "#PetPhotography",
        "#FurBabies",
        "#FurryLove",
        "#AnimalMagic",
        "#AnimalsOfInstagram",
        "#InstaAnimal",
        "#PetAddict",
        "#PetsofInstagram",
        "#WildlifePhotographer",
        "#FurryFriends",
        "#NatureLovers",
        "#WildlifeLover"
    ]

    # Get the current day of the month (1-31)
    day_of_month = datetime.datetime.now().day
    print(f"Day of the month: {day_of_month}")
    # List the video files in the 'reels' directory
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

    if day_of_month <= len(video_files):
        video_path = os.path.join(video_dir, video_files[day_of_month - 1])
        upload(video_path, hashtags)
    else:
        print("No video to upload today.")


main()
