# 🎬 YouTube Downloader Telegram Bot

بوت تيليجرام لتنزيل فيديوهات يوتيوب بكل سهولة!

## ✨ الميزات

- 📹 تنزيل الفيديو بأي جودة (360p - 1080p)
- 🎵 تنزيل الصوت MP3 (128/256/320 kbps)
- ⚡ سريع ومجاني
- 🌐 يدعم يوتيوب وروابط قصيرة

## 🚀 التثبيت

### 1. استنساخ المشروع

```bash
git clone https://github.com/yourusername/youtube-downloader-bot.git
cd youtube-downloader-bot
```

### 2. إنشاء بوت تيليجرام

1. افتح BotFather: `t.me/BotFather`
2. أنشئ بوت جديد: `/newbot`
3. احصل على TOKEN

### 3. إعداد البيئة

```bash
cp .env.example .env
nano .env
```

أضف التوكن:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

### 4. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 5. تشغيل البوت

```bash
python bot.py
```

## 🖥️ النشر على السيرفر

### Render (مجاني)

1. ارفع الكود على GitHub
2. سجل في render.com
3. أضف `PYTHON_VERSION = 3.11`
4. أمر التشغيل: `python bot.py`

### Railway

1. ارفع الكود على GitHub
2. أضف متغير `TELEGRAM_BOT_TOKEN`
3. deploy تلقائي

### VPS/Linux

```bash
screen -S bot
python bot.py
Ctrl+A+D للخروج
```

## 📁 هيكل المشروع

```
youtube-downloader-bot/
├── bot.py           # الملف الرئيسي
├── config.py        # الإعدادات
├── downloader.py    # محرك التنزيل
├── handlers.py      # معالجة الأوامر
├── keyboards.py     # أزرار التحكم
├── requirements.txt # المتطلبات
├── .env.example    # نموذج المتغيرات
└── temp/           # الملفات المؤقتة
```

## 🔐 حل مشكلة "Please sign in"

إذا واجهت خطأ "يرجى تسجيل الدخول"، اتبع الخطوات:

### 1. تصدير الكوكيز من المتصفح

1. ثبت إضافة **[Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookies-txt-locally/ccleldfahkkkleeddjhbimepncpfndmk)** في كروم
2. سجّل دخولك في يوتيوب على المتصفح
3. اذهب لـ `youtube.com`
4. اضغط على الإضافة → Export Cookies
5. احفظ الملف باسم `cookies.txt`

### 2. رفع الكوكيز على السيرفر

**للاستضافة المحلية:**
```bash
cp cookies.txt .env
```

**لـ Render/Railway:**
- أضف الملف `cookies.txt` إلى المستودع
- أو أضف Secret File في إعدادات الاستضافة

### 3. ملاحظة مهمة

- الكوكيز تنتهي بعد فترة،，你需要 تجديدها
- لا تشارك الكوكيز مع أحد

---

## ⚠️ ملاحظات

- الحد الأقصى لحجم الملف: 50MB
- يوتيوب قد يحظر بعض الطلبات (استخدم VPN إذا لزم)
- الملف يُحذف بعد الإرسال لتوفير المساحة

## 📜 الرخصة

MIT License