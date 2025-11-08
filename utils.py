import os, subprocess, platform
from PyQt5.QtWidgets import QMessageBox

def check_ffmpeg(parent):
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=3)
    except:
        QMessageBox.warning(parent, "Cảnh báo", "⚠️ Không tìm thấy FFmpeg!\nMột số tính năng có thể bị hạn chế.")

def open_folder(parent, path):
    if not os.path.isdir(path):
        QMessageBox.warning(parent, "Lỗi", "Không tìm thấy thư mục!")
        return
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.run(['open', path])
        else:
            subprocess.run(['xdg-open', path])
    except Exception as e:
        QMessageBox.warning(parent, "Lỗi", str(e))
