import os
import yt_dlp
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class DownloadSignals(QObject):
    """Signals for communicating download progress and status"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    error = pyqtSignal(str)


class DownloadWorker(QThread):
    """
    Worker thread for downloading videos/audio using yt-dlp.
    Inherits from QThread for proper thread management.
    """
    def __init__(self, url, mode, folder, signals, playlist, quality):
        super().__init__()
        self.url = url
        self.mode = mode
        self.folder = folder
        self.signals = signals
        self.playlist = playlist
        self.quality = quality
        self._is_cancelled = False

    def run(self):
        """Main execution method for the thread"""
        try:
            # Validate folder exists
            if not os.path.isdir(self.folder):
                os.makedirs(self.folder, exist_ok=True)
                self.signals.status.emit(f"📁 Đã tạo thư mục: {self.folder}")

            q_map = {
                "Tốt nhất": "bestvideo+bestaudio/best",
                "1080p": "bestvideo[height<=1080]+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best",
                "480p": "bestvideo[height<=480]+bestaudio/best",
                "360p": "bestvideo[height<=360]+bestaudio/best"
            }

            ydl_opts = {
                'outtmpl': os.path.join(self.folder, '%(title)s.%(ext)s'),
                'progress_hooks': [self.hook],
                'noplaylist': not self.playlist,
                'quiet': False,
                'no_warnings': False,
                'ignoreerrors': False,  # Stop on first error
                'nocheckcertificate': False,
            }

            if self.mode == "audio":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                ydl_opts['postprocessor_args'] = [
                    '-ar', '44100'  # Standard audio sample rate
                ]
            else:
                ydl_opts['format'] = q_map.get(self.quality, q_map["Tốt nhất"])
                ydl_opts['merge_output_format'] = 'mp4'

            self.signals.status.emit(f"🔍 Đang phân tích URL...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Check if cancelled before starting
                if self._is_cancelled:
                    self.signals.finished.emit(False, "❌ Đã hủy tải xuống")
                    return
                
                # Get video info first
                info = ydl.extract_info(self.url, download=False)
                if info:
                    if 'entries' in info:
                        # It's a playlist
                        count = len(info['entries'])
                        self.signals.status.emit(f"📑 Tìm thấy {count} video trong playlist")
                    else:
                        # Single video
                        title = info.get('title', 'Unknown')
                        duration = info.get('duration', 0)
                        duration_str = f"{duration//60}:{duration%60:02d}" if duration else "N/A"
                        self.signals.status.emit(f"🎬 {title} ({duration_str})")
                
                # Start download
                if not self._is_cancelled:
                    ydl.download([self.url])
                    self.signals.finished.emit(True, "✅ Hoàn tất tải xuống!")
                else:
                    self.signals.finished.emit(False, "❌ Đã hủy tải xuống")
                    
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if "Private video" in error_msg:
                self.signals.finished.emit(False, "❌ Video riêng tư hoặc bị hạn chế")
            elif "Video unavailable" in error_msg:
                self.signals.finished.emit(False, "❌ Video không khả dụng")
            else:
                self.signals.finished.emit(False, f"❌ Lỗi tải xuống: {error_msg}")
        except Exception as e:
            self.signals.finished.emit(False, f"❌ Lỗi: {str(e)}")

    def hook(self, d):
        """Progress hook called by yt-dlp during download"""
        if self._is_cancelled:
            raise Exception("Download cancelled by user")
            
        if d['status'] == 'downloading':
            # Extract progress information
            percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
            speed_str = d.get('_speed_str', 'N/A')
            eta_str = d.get('_eta_str', 'N/A')
            
            try:
                percent = int(float(percent_str))
                self.signals.progress.emit(percent)
            except (ValueError, TypeError):
                pass
            
            # Format status message
            filename = d.get('filename', '').split(os.sep)[-1]
            if len(filename) > 40:
                filename = filename[:37] + "..."
            
            self.signals.status.emit(
                f"⬇️ {percent_str}% | {speed_str} | ETA {eta_str} | {filename}"
            )
            
        elif d['status'] == 'finished':
            self.signals.progress.emit(100)
            filename = d.get('filename', '').split(os.sep)[-1]
            self.signals.status.emit(f"🔄 Đang xử lý: {filename}...")
            
        elif d['status'] == 'error':
            self.signals.status.emit(f"❌ Lỗi trong quá trình tải")

    def cancel(self):
        """Cancel the download operation"""
        self._is_cancelled = True
        self.signals.status.emit("⚠️ Đang hủy tải xuống...")