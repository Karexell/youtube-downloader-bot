"""
YouTube Downloader using yt-dlp
"""
import os
import asyncio
from typing import Optional, Dict, List, Callable
import yt_dlp
from config import (
    TEMP_DIR,
    MAX_FILE_SIZE,
    DOWNLOAD_TIMEOUT,
    DOWNLOAD_PROGRESS_UPDATE,
    YOUTUBE_COOKIES_FILE
)


class YouTubeDownloader:
    def __init__(self):
        self.temp_dir = TEMP_DIR
        os.makedirs(self.temp_dir, exist_ok=True)
        self.cookies_file = YOUTUBE_COOKIES_FILE if os.path.exists(YOUTUBE_COOKIES_FILE) else None
    
    def _get_cookies_opts(self) -> dict:
        """Get cookies options if file exists"""
        if self.cookies_file:
            return {'cookiefile': self.cookies_file}
        return {}

    def extract_video_info(self, url: str) -> Optional[Dict]:
        """Extract video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            **self._get_cookies_opts(),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'thumbnail': info.get('thumbnail'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'views': info.get('view_count', 0),
                    'formats': self._get_formats_list(info.get('formats', [])),
                }
        except Exception as e:
            print(f"Error extracting info: {e}")
            return None

    def _get_formats_list(self, formats: List[Dict]) -> List[Dict]:
        """Get list of available formats"""
        seen = set()
        result = []
        
        for f in formats:
            height = f.get('height', 0)
            if height and height not in seen and height <= 1080:
                seen.add(height)
                result.append({
                    'format_id': f['format_id'],
                    'height': height,
                    'ext': f.get('ext', 'unknown'),
                    'filesize': f.get('filesize', 0),
                })
        
        result.sort(key=lambda x: x['height'], reverse=True)
        return result[:6]

    async def download_video(
        self,
        url: str,
        format_id: str,
        progress_callback: Optional[Callable] = None
    ) -> Optional[str]:
        """Download video with progress callback"""
        output_template = os.path.join(self.temp_dir, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': output_template,
            'maxfilesize': MAX_FILE_SIZE,
            'timeout': DOWNLOAD_TIMEOUT,
            'progress_hooks': [],
            **self._get_cookies_opts(),
        }
        
        if progress_callback:
            ydl_opts['progress_hooks'] = [
                lambda d: asyncio.create_task(
                    progress_callback(d)
                )
            ]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if os.path.exists(filename):
                    return filename
                return None
        except Exception as e:
            print(f"Download error: {e}")
            return None

    async def download_audio(
        self,
        url: str,
        quality: str = "320",
        progress_callback: Optional[Callable] = None
    ) -> Optional[str]:
        """Download audio only (MP3)"""
        output_template = os.path.join(self.temp_dir, '%(title)s.mp3')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'maxfilesize': MAX_FILE_SIZE,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            **self._get_cookies_opts(),
        }
        
        if progress_callback:
            ydl_opts['progress_hooks'] = [
                lambda d: asyncio.create_task(
                    progress_callback(d)
                )
            ]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                filename = os.path.splitext(filename)[0] + '.mp3'
                
                if os.path.exists(filename):
                    return filename
                return None
        except Exception as e:
            print(f"Audio download error: {e}")
            return None

    def get_progress_text(self, d: Dict) -> str:
        """Get progress text from download status"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', '0')
            eta = d.get('_eta_str', '0')
            return f"📥 جاري التنزيل...\n{percent}\nالسرعة: {speed}\nالمتبقي: {eta}"
        elif d['status'] == 'finished':
            return "✅ اكتمل التنزيل!"
        return ""

    def cleanup_file(self, filepath: str) -> bool:
        """Delete downloaded file"""
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Cleanup error: {e}")
            return False

    def is_youtube_url(self, url: str) -> bool:
        """Check if URL is from YouTube"""
        youtube_domains = [
            'youtube.com',
            'youtu.be',
            'youtube-nocookie.com',
        ]
        return any(domain in url.lower() for domain in youtube_domains)