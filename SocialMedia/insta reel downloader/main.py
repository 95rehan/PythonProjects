import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import yt_dlp


class InstaDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instagram Reels Downloader By Rehan")
        self.setFixedSize(500, 220)

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

        self.setLayout(layout)

    def download_reel(self):
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.critical(self, "Error", "Please enter an Instagram Reel URL.")
            return

        save_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if not save_path:
            return

        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'best',
            'quiet': False
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            QMessageBox.information(
                self,
                "Success",
                f"Reel Downloaded Successfully!\n\nSaved in:\n{save_path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Download Failed", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstaDownloader()
    window.show()
    sys.exit(app.exec())