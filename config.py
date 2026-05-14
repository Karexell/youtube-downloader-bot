"""
Configuration file for YouTube Downloader Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
YOUTUBE_COOKIES_FILE = os.getenv("YOUTUBE_COOKIES_FILE", "cookies.txt")

MAX_FILE_SIZE = 50 * 1024 * 1024

DOWNLOAD_TIMEOUT = 600

TEMP_DIR = "temp"

VIDEO_QUALITY_OPTIONS = {
    "best": "الأفضل (1080p+)",
    "720p": "720p HD",
    "480p": "480p",
    "360p": "360p (صغير)",
}

AUDIO_QUALITY_OPTIONS = {
    "320": "320 kbps (الأفضل)",
    "256": "256 kbps",
    "128": "128 kbps (افتراضي)",
}

DOWNLOAD_PROGRESS_UPDATE = 5

MESSAGE_TIMEOUT = 30