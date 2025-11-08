# 🎥 YouTube Downloader

Ứng dụng tải video/audio từ YouTube với giao diện đồ họa đơn giản, dễ sử dụng.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Tính năng

- ✅ Tải video với nhiều chất lượng (Best, 4K, 2K, 1080p, 720p, 480p, 360p)
- 🎧 Tải audio và chuyển đổi sang MP3
- 📝 Hỗ trợ tải playlist
- 📊 Hiển thị tiến trình tải xuống real-time
- 💾 Lưu thư mục tải xuống cuối cùng
- 🎯 Giao diện thân thiện, dễ sử dụng
- ⚡ Hỗ trợ hủy tải xuống

## 📸 Giao diện

```
┌─────────────────────────────────────┐
│  🔗 Video URL:                      │
│  [________________] [📋 Paste]      │
│                                     │
│  📁 Save to:                        │
│  [________________] [...]           │
│                                     │
│  Quality: [Best ▼]  ☑ Playlist     │
│  ────────────────────────────────   │
│  [████████████░░░░] 75%            │
│  [🎥 Video]  [🎧 MP3]              │
│  [❌ Cancel] [📂 Open Folder]       │
│  ┌───────────────────────────────┐ │
│  │ Log output...                 │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 🚀 Cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- FFmpeg (để chuyển đổi audio sang MP3)

### Cài đặt từ source

1. Clone repository:
```bash
git clone https://github.com/duy/youtube-downloader.git
cd youtube-downloader
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Cài đặt FFmpeg:
   - **Windows**: Tải từ [ffmpeg.org](https://ffmpeg.org/download.html) và thêm vào PATH
   - **Linux**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`

4. Chạy ứng dụng:
```bash
python main.py
```

## 📦 Build file thực thi

Để tạo file `.exe` độc lập:

```bash
pyinstaller --onefile --noconsole --add-data "icon.ico;." --hidden-import=PyQt5 --hidden-import=yt_dlp --icon=icon.ico --name="YouTube_Downloader" main.py
```

File `.exe` sẽ được tạo trong thư mục `dist/`

## 📋 requirements.txt

```
PyQt5>=5.15.0
yt-dlp>=2023.0.0
```

## 🎮 Hướng dẫn sử dụng

1. **Nhập URL video**: Dán link YouTube vào ô "Video URL" (hoặc nhấn nút "Paste")
2. **Chọn thư mục lưu**: Click nút "..." để chọn nơi lưu file
3. **Chọn chất lượng**: Chọn độ phân giải mong muốn (mặc định: Best)
4. **Tải playlist** (tùy chọn): Tick vào "Playlist" nếu muốn tải cả playlist
5. **Tải xuống**:
   - Click "🎥 Video" để tải video
   - Click "🎧 MP3" để tải audio (định dạng MP3)
6. **Theo dõi tiến trình**: Xem thanh progress bar và log bên dưới
7. **Hủy tải** (nếu cần): Click "❌ Cancel"
8. **Mở thư mục**: Click "📂 Open Folder" để xem file đã tải

## 🏗️ Cấu trúc dự án

```
youtube-downloader/
├── main.py              # File chính, khởi động ứng dụng
├── ui_main.py           # Giao diện chính (PyQt5)
├── downloader.py        # Logic tải xuống (yt-dlp)
├── config.py            # Quản lý cấu hình
├── utils.py             # Các hàm tiện ích
├── icon.ico             # Icon ứng dụng
├── requirements.txt     # Danh sách thư viện
└── README.md           # File này
```

## 🔧 Các tính năng kỹ thuật

- **Multi-threading**: Sử dụng QThread để tải xuống không block UI
- **Signal/Slot**: Giao tiếp giữa worker thread và UI thread
- **Progress tracking**: Hiển thị tiến trình real-time với speed và ETA
- **Error handling**: Xử lý lỗi video riêng tư, không khả dụng, v.v.
- **Config persistence**: Lưu thư mục tải xuống cuối cùng vào file JSON

## ⚠️ Lưu ý

- Ứng dụng yêu cầu kết nối internet để tải video
- Tốc độ tải phụ thuộc vào kết nối mạng của bạn
- Một số video có thể bị hạn chế tải xuống do quyền sở hữu
- Tuân thủ điều khoản sử dụng của YouTube khi tải nội dung

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork dự án
2. Tạo branch mới (`git checkout -b feature/TinhNangMoi`)
3. Commit thay đổi (`git commit -m 'Thêm tính năng mới'`)
4. Push lên branch (`git push origin feature/TinhNangMoi`)
5. Tạo Pull Request

## 📝 Changelog

### v1.0.0 (2024)
- ✨ Phát hành phiên bản đầu tiên
- 🎥 Hỗ trợ tải video với nhiều chất lượng
- 🎧 Hỗ trợ tải audio MP3
- 📝 Hỗ trợ tải playlist
- 💾 Lưu cấu hình thư mục


## 📄 Giấy phép

Dự án này được phát hành dưới giấy phép [MIT License](LICENSE).


## 🙏 Cảm ơn

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Thư viện tải video mạnh mẽ
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Framework GUI
- [FFmpeg](https://ffmpeg.org/) - Công cụ xử lý media

## ⭐ Ủng hộ

Nếu bạn thấy dự án hữu ích, hãy cho một ⭐ trên GitHub!

---

Made with ❤️ in Vietnam
