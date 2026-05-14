"""
Inline keyboards for the bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import VIDEO_QUALITY_OPTIONS, AUDIO_QUALITY_OPTIONS


def get_main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("📹 تنزيل فيديو", callback_data="mode_video")],
        [InlineKeyboardButton("🎵 تنزيل صوت (MP3)", callback_data="mode_audio")],
        [InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_video_quality_keyboard(formats: list):
    """Video quality selection keyboard with reliable selectors"""
    quality_options = [
        ("best", "🎬 أفضل جودة (أوتوماتيكي)"),
        ("bestvideo[height<=1080]+bestaudio/best[height<=1080]", "📹 1080p HD"),
        ("bestvideo[height<=720]+bestaudio/best[height<=720]", "📹 720p HD"),
        ("bestvideo[height<=480]+bestaudio/best[height<=480]", "📱 480p"),
        ("bestvideo[height<=360]+bestaudio/best[height<=360]", "📵 360p"),
    ]
    
    keyboard = []
    for selector, label in quality_options:
        keyboard.append([
            InlineKeyboardButton(label, callback_data=f"video_{selector}")
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)


def get_audio_quality_keyboard():
    """Audio quality selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("320 kbps ⭐", callback_data="audio_320"),
            InlineKeyboardButton("256 kbps", callback_data="audio_256"),
        ],
        [InlineKeyboardButton("128 kbps (افتراضي)", callback_data="audio_128")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard(url: str, format_id: str, is_audio: bool = False):
    """Download confirmation keyboard"""
    data_prefix = "audio" if is_audio else "video"
    keyboard = [
        [
            InlineKeyboardButton("✅ نعم", callback_data=f"confirm_{data_prefix}_{format_id}_{url}"),
            InlineKeyboardButton("❌ لا", callback_data="cancel"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard():
    """Back to main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard():
    """Cancel operation keyboard"""
    keyboard = [
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)