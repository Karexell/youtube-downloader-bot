"""
Handlers for Telegram bot commands and messages
"""
import os
import asyncio
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from downloader import YouTubeDownloader
from keyboards import (
    get_main_menu_keyboard,
    get_video_quality_keyboard,
    get_audio_quality_keyboard,
    get_confirmation_keyboard,
    get_back_keyboard,
)
from config import TELEGRAM_BOT_TOKEN

download_manager = YouTubeDownloader()

WAITING_FOR_URL = 1
WAITING_FOR_QUALITY = 2

user_sessions = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_text = """
🎬 **بوت تنزيل يوتيوب**

أهلاً بك! أنا بوت لتنزيل فيديوهات يوتيوب بكل سهولة.

**الميزات:**
📹 تنزيل الفيديو بأي جودة
🎵 تنزيل الصوت MP3
⚡ سريع ومجاني

**ابدأ الآن:**
أرسل رابط يوتيوب أو اختر من الأزرار أدناه
    """
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📖 **مساعدة**

**كيفية الاستخدام:**
1. أرسل رابط يوتيوب
2. اختر الجودة المطلوبة
3. انتظر حتى يكتمل التنزيل

**الأوامر:**
/start - بدء البوت
/help - المساعدة
/cancel - إلغاء العملية

**ملاحظات:**
- الحد الأقصى لحجم الملف 50MB
- يدعم الفيديو حتى 1080p
- يدعم صوت MP3 بجودات متعددة
    """
    await update.message.reply_text(
        help_text,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    await update.message.reply_text(
        "❌ تم إلغاء العملية",
        reply_markup=get_main_menu_keyboard()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages (YouTube URLs)"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if not download_manager.is_youtube_url(text):
        await update.message.reply_text(
            "⚠️ يرجى إرسال رابط يوتيوب صالح",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    await update.message.reply_text("🔍 جاري التحقق من الفيديو...")
    
    video_info = download_manager.extract_video_info(text)
    
    if not video_info:
        await update.message.reply_text(
            "❌ تعذر الوصول للفيديو. تأكد من صحة الرابط",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    duration_min = video_info['duration'] // 60
    duration_sec = video_info['duration'] % 60
    
    info_text = f"""
📹 **{video_info['title']}**

⏱️ المدة: {duration_min}:{duration_sec:02d}
👤 القناة: {video_info['uploader']}
👁️ المشاهدات: {video_info['views']:,}

اختر الجودة:
    """
    
    keyboard = get_video_quality_keyboard(video_info['formats'])
    
    user_sessions[user_id] = {
        'url': text,
        'title': video_info['title'],
        'formats': video_info['formats'],
    }
    
    await update.message.reply_text(
        info_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "mode_video":
        await query.edit_message_text(
            "📹 أرسل رابط يوتيوب لتنزيل الفيديو"
        )
    
    elif data == "mode_audio":
        await query.edit_message_text(
            "🎵 أرسل رابط يوتيوب لتنزيل الصوت",
            reply_markup=get_audio_quality_keyboard()
        )
    
    elif data == "help":
        await help_command(update, context)
    
    elif data == "back_main":
        await query.edit_message_text(
            "✅ عدت للقائمة الرئيسية",
            reply_markup=get_main_menu_keyboard()
        )
    
    elif data == "cancel":
        if user_id in user_sessions:
            del user_sessions[user_id]
        await query.edit_message_text(
            "❌ تم إلغاء العملية",
            reply_markup=get_main_menu_keyboard()
        )
    
    elif data.startswith("video_"):
        format_id = data.replace("video_", "")
        await process_video_download(query, user_id, format_id)
    
    elif data.startswith("audio_"):
        quality = data.replace("audio_", "")
        await process_audio_download(query, user_id, quality)


async def process_video_download(query, user_id: int, format_id: str):
    """Process video download request"""
    if user_id not in user_sessions:
        await query.edit_message_text(
            "❌ انتهت الجلسة. أرسل الرابط مجدداً",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    session = user_sessions[user_id]
    url = session['url']
    title = session['title']
    
    await query.edit_message_text(f"📥 جاري تنزيل: {title}\n\nقد يستغرق ذلك بعض الوقت...")
    
    filepath = await download_manager.download_video(url, format_id)
    
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as f:
                await query.message.reply_video(
                    video=f,
                    caption=f"✅ {title}",
                    read_timeout=60,
                )
            download_manager.cleanup_file(filepath)
            await query.edit_message_text(
                "✅ تم إرسال الفيديو بنجاح!",
                reply_markup=get_main_menu_keyboard()
            )
        except Exception as e:
            await query.edit_message_text(
                f"❌ خطأ في الإرسال: {str(e)}",
                reply_markup=get_main_menu_keyboard()
            )
            download_manager.cleanup_file(filepath)
    else:
        await query.edit_message_text(
            "❌ فشل التنزيل. جرب جودة أقل",
            reply_markup=get_main_menu_keyboard()
        )
    
    if user_id in user_sessions:
        del user_sessions[user_id]


async def process_audio_download(query, user_id: int, quality: str):
    """Process audio download request"""
    if user_id not in user_sessions:
        await query.edit_message_text(
            "❌ انتهت الجلسة. أرسل الرابط مجدداً",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    session = user_sessions[user_id]
    url = session['url']
    title = session['title']
    
    await query.edit_message_text(f"🎵 جاري تنزيل الصوت: {title}\n\nقد يستغرق ذلك بعض الوقت...")
    
    filepath = await download_manager.download_audio(url, quality)
    
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as f:
                await query.message.reply_audio(
                    audio=f,
                    title=title,
                    performer="YouTube Downloader",
                    read_timeout=60,
                )
            download_manager.cleanup_file(filepath)
            await query.edit_message_text(
                "✅ تم إرسال الصوت بنجاح!",
                reply_markup=get_main_menu_keyboard()
            )
        except Exception as e:
            await query.edit_message_text(
                f"❌ خطأ في الإرسال: {str(e)}",
                reply_markup=get_main_menu_keyboard()
            )
            download_manager.cleanup_file(filepath)
    else:
        await query.edit_message_text(
            "❌ فشل التنزيل. حاول مجدداً",
            reply_markup=get_main_menu_keyboard()
        )
    
    if user_id in user_sessions:
        del user_sessions[user_id]


def get_handlers():
    """Get all handlers"""
    return [
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CommandHandler("cancel", cancel_command),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
        CallbackQueryHandler(handle_callback),
    ]