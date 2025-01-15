from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, LoginRequired
import datetime
import os
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
import random
import time

SESSION_FILE = 'session.json'

# Access environment variables for Instagram credentials
username = os.getenv('INSTAGRAM_USERNAME', 'your_default_username')
password = os.getenv('INSTAGRAM_PASSWORD', 'your_default_password')


def random_delay(min_seconds=2, max_seconds=60):
    """Introduce a random delay to mimic human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def delete_session_file():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("Session file deleted due to automated activity detection.")

def login():
    """Log in to Instagram, either using a saved session or username/password."""
    print("   [green] Initializing login... [/green]")
    api = Client()
    api.delay_range = [1, 3]

    try:
        if os.path.exists(SESSION_FILE):
            print("   [green] Logging with previous session... [/green]")
            api.load_settings(SESSION_FILE)
            api.login(username, password)
            api.dump_settings(SESSION_FILE)
            api.get_timeline_feed()
            print("   [green] Logged in successfully. [/green]")
        else:
            print("   [green] Logging with username and password... [/green]")
            api.login(username, password)
            api.dump_settings(SESSION_FILE)
            api.get_timeline_feed()
            print("   [green] Logged in successfully. [/green]")

        return api
    
    except ChallengeRequired:
        print("Challenge required. Automated activity detected.")
        delete_session_file()
        raise

    except LoginRequired:
        print("Login required.")
        delete_session_file()
        raise

    except Exception as e:
        if 'challenge_required' in str(e).lower():
            print("Challenge required by Instagram. Please resolve manually in your app or web.")
        else:
            print(f"Exception during login: {type(e).__name__}: {str(e)}")
        delete_session_file()
        return None


def post_to_story(api, media, media_path):
    """Post the uploaded reel to the story with additional elements."""
    hashtag = api.hashtag_info('like')

    media_pk = api.media_pk_from_url(f'https://www.instagram.com/p/{media.code}/')

    api.video_upload_to_story(
        media_path,
        "",
        links=[StoryLink(webUri=f'https://www.instagram.com/p/{media.code}/')],
        hashtags=[StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)],
        medias=[StoryMedia(media_pk=media_pk, x=0.5, y=0.5, width=0.6, height=0.8)],
    )


def upload(video_path, hashtags):
    """Upload a video to Instagram as a reel with random captions and hashtags."""
    random_delay(2,2*60)
    api = login()
    
    if not api:
        print("Login failed. Skipping upload.")
        return

    captions = [
        "🐾 Love animals? Follow for daily heartwarming pet videos that will make your day! 🐶🐱",
        "😊 Want to smile every day? Follow us for the cutest animal moments on Instagram! 🐕🐈",
        "🐾 Get your daily dose of adorable pets! Follow now and join our animal-loving community! 🐾💖",
        # Add more captions as needed
    ]

    random_caption = random.choice(captions)
    try:
        selected_hashtags = random.sample(hashtags, 10)
        hashtags_str = ' '.join(selected_hashtags)

        caption_with_hashtags = f"{random_caption} {hashtags_str}"
        random_delay(2,60)
        api.delay_range = [1, 3]
        reel = api.clip_upload(
            video_path,
            caption_with_hashtags,
            extra_data={
                "like_and_view_counts_disabled": True,
            }
        )
        print("Reel uploaded successfully!")

        post_to_story(api, reel, video_path)

    except Exception as e:
        print(f"Exception during upload: {type(e).__name__}: {str(e)}")


def main():
    """Main function to upload a video based on the day of the month."""
    video_dir = './reels'

    hashtags = [
        "#CuteAnimals", "#FunnyAnimals", "#AnimalVideos", "#PetLovers", "#PetsofIG",
        "#AdorablePets", "#PetPhotography", "#FurBabies", "#FurryLove", "#AnimalMagic",
        "#AnimalsOfInstagram", "#InstaAnimal", "#PetAddict", "#PetsofInstagram",
        "#WildlifePhotographer", "#FurryFriends", "#NatureLovers", "#WildlifeLover"
    ]

    day_of_month = datetime.datetime.now().day
    print(f"Day of the month: {day_of_month}")

    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

    if day_of_month <= len(video_files):
        video_path = os.path.join(video_dir, video_files[day_of_month - 1])
        upload(video_path, hashtags)
    else:
        print("No video to upload today.")


if __name__ == "__main__":
    main()
