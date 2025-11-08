import os
import sys
import re
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QComboBox, QCheckBox,
    QTextEdit, QFrame, QProgressBar, QApplication, QSizePolicy
)
from PyQt5.QtGui import QFont, QTextCursor, QIcon
from PyQt5.QtCore import Qt
from downloader import DownloadWorker, DownloadSignals
from config import load_config, save_config
from utils import check_ffmpeg, open_folder


def resource_path(relative_path):
    try:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        # Icon
        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
            QApplication.setWindowIcon(app_icon)

        # Signals
        self.signals = DownloadSignals()
        self.signals.progress.connect(self.update_progress)
        self.signals.status.connect(self.update_status)
        self.signals.finished.connect(self.download_finished)

        # Window
        self.setWindowTitle("Video Downloader")
        self.setGeometry(400, 200, 600, 500)
        self.setMinimumSize(500, 450)

        # Load config
        self.config_file, self.saved_folder = load_config()
        check_ffmpeg(self)

        self.current_worker = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # URL + Paste
        url_label = QLabel("🔗 Video URL:")
        url_label.setFont(QFont("Arial", 10))
        url_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        url_box = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://youtube.com/watch?v=...")
        self.url_input.setFont(QFont("Arial", 10))
        self.url_input.setFixedHeight(36)
        paste_btn = QPushButton("📋 Paste")
        paste_btn.setFont(QFont("Arial", 10))
        paste_btn.setFixedSize(90, 36)
        paste_btn.clicked.connect(self.paste_url)
        url_box.addWidget(self.url_input)
        url_box.addWidget(paste_btn)
        main_layout.addWidget(url_label)
        main_layout.addLayout(url_box)

        # Folder
        folder_label = QLabel("📁 Save to:")
        folder_label.setFont(QFont("Arial", 10))
        folder_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        folder_box = QHBoxLayout()
        self.folder_path = QLineEdit(self.saved_folder)
        self.folder_path.setFont(QFont("Arial", 10))
        self.folder_path.setFixedHeight(36)
        self.folder_path.textChanged.connect(lambda: save_config(self.folder_path.text()))
        choose_btn = QPushButton("...")
        choose_btn.setFont(QFont("Arial", 10))
        choose_btn.setFixedSize(36, 36)
        choose_btn.clicked.connect(self.choose_folder)
        folder_box.addWidget(self.folder_path)
        folder_box.addWidget(choose_btn)
        main_layout.addWidget(folder_label)
        main_layout.addLayout(folder_box)

        # Quality + Playlist
        opts_box = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setFont(QFont("Arial", 10))
        quality_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.quality_box = QComboBox()
        self.quality_box.addItems(["Best", "4K", "2K", "1080p", "720p", "480p", "360p"])
        self.quality_box.setFont(QFont("Arial", 10))
        self.quality_box.setFixedHeight(32)
        self.quality_box.setFixedWidth(120)
        self.playlist_check = QCheckBox("Playlist")
        self.playlist_check.setFont(QFont("Arial", 10))
        self.playlist_check.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        opts_box.addWidget(quality_label)
        opts_box.addWidget(self.quality_box)
        opts_box.addWidget(self.playlist_check)
        opts_box.addStretch()
        main_layout.addLayout(opts_box)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(24)
        main_layout.addWidget(self.progress_bar)

        # Download buttons
        dl_box = QHBoxLayout()
        self.video_btn = QPushButton("🎥 Video")
        self.audio_btn = QPushButton("🎧 MP3")
        for b in [self.video_btn, self.audio_btn]:
            b.setFont(QFont("Arial", 11, QFont.Bold))
            b.setFixedHeight(40)
        dl_box.addWidget(self.video_btn)
        dl_box.addWidget(self.audio_btn)
        main_layout.addLayout(dl_box)

        # Control buttons
        ctrl_box = QHBoxLayout()
        self.cancel_btn = QPushButton("❌ Cancel")
        self.open_btn = QPushButton("📂 Open Folder")
        for b in [self.cancel_btn, self.open_btn]:
            b.setFont(QFont("Arial", 10))
            b.setFixedHeight(40)
        self.cancel_btn.setEnabled(False)
        ctrl_box.addWidget(self.cancel_btn)
        ctrl_box.addWidget(self.open_btn)
        main_layout.addLayout(ctrl_box)

        # Log (white background, black text, font nhỏ, nằm dưới)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 8))
        self.log_output.setLineWrapMode(QTextEdit.NoWrap)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 4px;
                border-radius: 4px;
                margin-top:4px;
            }
        """)
        self.log_output.setMinimumHeight(150)
        self.log_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.log_output)

        # Signals
        self.video_btn.clicked.connect(lambda: self.start_download("video"))
        self.audio_btn.clicked.connect(lambda: self.start_download("audio"))
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.open_btn.clicked.connect(lambda: open_folder(self, self.folder_path.text()))

        self.log("✨ Ready!")

    # Paste button
    def paste_url(self):
        text = QApplication.clipboard().text().strip()
        if text:
            self.url_input.setText(text)
        else:
            QMessageBox.information(self, "Clipboard", "Clipboard is empty!")

    # Logging (chỉ hiển thị tiến trình)
    def log(self, text):
        now = time.strftime("%H:%M:%S")
        self.log_output.append(f"[[{now}]] {text}")
        self.log_output.moveCursor(QTextCursor.End)
        if self.log_output.document().blockCount() > 200:
            cursor = self.log_output.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

    # Folder selection
    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.folder_path.text())
        if folder:
            self.folder_path.setText(folder)
            save_config(folder)

    # Start download
    def start_download(self, mode):
        url = self.url_input.text().strip()
        folder = self.folder_path.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Enter a video URL!")
            return
        if not folder:
            QMessageBox.warning(self, "Error", "Select a save location!")
            return

        self.log_output.clear()
        self.progress_bar.setValue(0)
        self.log(f"🚀 {mode.upper()} download started")
        if self.playlist_check.isChecked():
            self.log("📝 Playlist mode ON")

        self.set_buttons_enabled(False)

        quality_map = {
            "Best": "bestvideo+bestaudio/best",
            "4K": "2160p",
            "2K": "1440p",
            "1080p": "1080p",
            "720p": "720p",
            "480p": "480p",
            "360p": "360p"
        }

        self.current_worker = DownloadWorker(
            url, mode, folder, self.signals,
            self.playlist_check.isChecked(),
            quality_map[self.quality_box.currentText()]
        )
        self.current_worker.start()

    def cancel_download(self):
        if self.current_worker and self.current_worker.isRunning():
            if QMessageBox.question(self, "Cancel", "Cancel download?") == QMessageBox.Yes:
                self.current_worker.cancel()
                self.log("⚠️ Cancelling...")

    # UI Update
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, text):
        try:
            clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
            # Chỉ log các dòng tiến trình (% | speed | ETA | ⬇️ | ✅)
            if "%" in clean_text or "ETA" in clean_text or "⬇️" in clean_text or "✅" in clean_text:
                parts = clean_text.split("|")[:3]  # giữ 3 cột đầu
                progress_line = " |".join(parts).strip()
                self.log(progress_line)
        except:
            pass

    def download_finished(self, success, msg):
        self.log(msg)
        self.progress_bar.setValue(100 if success else 0)
        self.set_buttons_enabled(True)
        if success:
            if QMessageBox.information(self, "Done", f"{msg}\n\nOpen folder?",
                                      QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                open_folder(self, self.folder_path.text())

    def set_buttons_enabled(self, enabled):
        self.video_btn.setEnabled(enabled)
        self.audio_btn.setEnabled(enabled)
        self.cancel_btn.setEnabled(not enabled)
        self.open_btn.setEnabled(enabled)
        self.url_input.setEnabled(enabled)
        self.folder_path.setEnabled(enabled)
        self.quality_box.setEnabled(enabled)
        self.playlist_check.setEnabled(enabled)