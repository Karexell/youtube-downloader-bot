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
    """Video quality selection keyboard"""
    keyboard = []
    
    for fmt in formats:
        height = fmt['height']
        label = f"{height}p"
        
        if height >= 1080:
            label = "🎬 1080p HD"
        elif height >= 720:
            label = "📹 720p HD"
        elif height >= 480:
            label = "📱 480p"
        else:
            label = "📵 360p"
        
        keyboard.append([
            InlineKeyboardButton(label, callback_data=f"video_{fmt['format_id']}")
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