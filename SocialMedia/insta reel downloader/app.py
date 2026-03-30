import sys
import os
import re
import logging
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import yt_dlp


# -------------------------
# Logging Setup
# -------------------------
logging.basicConfig(
    filename="insta_downloader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -------------------------
# Worker Thread
# -------------------------
class DownloadWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and 'downloaded_bytes' in d:
                percent = int(
                    d['downloaded_bytes'] * 100 / d['total_bytes']
                )
                self.progress.emit(percent)

    def run(self):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.save_path, '%(title).50s.%(ext)s'),
                'format': 'best',
                'progress_hooks': [self.progress_hook],
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            logging.info(f"Downloaded: {self.url}")
            self.finished.emit(self.save_path)

        except Exception as e:
            logging.error(f"Error downloading {self.url} - {str(e)}")
            self.error.emit(str(e))


# -------------------------
# Main App
# -------------------------
class InstaDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instagram Reels Downloader - By Rehan")
        self.setFixedSize(500, 260)

        layout = QVBoxLayout()

        self.label = QLabel("Paste Instagram Reel URL:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.instagram.com/reel/...")
        layout.addWidget(self.url_input)

        self.download_button = QPushButton("Download Reel")
        self.download_button.clicked.connect(self.download_reel)
        layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def validate_url(self, url):
        pattern = r"https://(www\.)?instagram\.com/reel/.+"
        return re.match(pattern, url)

    def download_reel(self):
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.critical(self, "Error", "Please enter a URL.")
            return

        if not self.validate_url(url):
            QMessageBox.critical(self, "Invalid URL", "Enter a valid Instagram Reel URL.")
            return

        save_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if not save_path:
            return

        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)

        self.worker = DownloadWorker(url, save_path)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.download_success)
        self.worker.error.connect(self.download_error)
        self.worker.start()

    def download_success(self, path):
        self.download_button.setEnabled(True)
        QMessageBox.information(
            self,
            "Success",
            f"Reel Downloaded Successfully!\n\nSaved in:\n{path}"
        )

    def download_error(self, error_message):
        self.download_button.setEnabled(True)
        QMessageBox.critical(self, "Download Failed", error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstaDownloader()
    window.show()
    sys.exit(app.exec())