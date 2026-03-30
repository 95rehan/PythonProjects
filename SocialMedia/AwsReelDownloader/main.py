import os
import uuid
import re
import yt_dlp

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.background import BackgroundTasks

app = FastAPI()

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# -----------------------------
# URL Validation
# -----------------------------
def validate_url(url: str):
    pattern = r"https://(www\.)?instagram\.com/.+"
    return re.match(pattern, url)


# -----------------------------
# Home Page (Simple UI)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Instagram Video Downloader By Rehan</title>
        </head>
        <body style="text-align:center; margin-top:100px; font-family:Arial;">
            <h2>Instagram Video Downloader By Rehan</h2>
            <form action="/download" method="post">
                <input 
                    type="text" 
                    name="url" 
                    placeholder="Paste Instagram URL"
                    style="width:300px; padding:8px;"
                    required
                />
                <br><br>
                <button type="submit" style="padding:8px 20px;">
                    Download
                </button>
            </form>
        </body>
    </html>
    """


# -----------------------------
# Download Route
# -----------------------------
@app.post("/download")
async def download_video(
    background_tasks: BackgroundTasks,
    url: str = Form(...)
):
    if not validate_url(url):
        return {"error": "Invalid Instagram URL"}

    unique_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, unique_id)

    ydl_opts = {
        "outtmpl": output_path + ".%(ext)s",
        "format": "best",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find downloaded file
        file_path = None
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(unique_id):
                file_path = os.path.join(DOWNLOAD_FOLDER, file)
                break

        if not file_path:
            return {"error": "Download failed"}

        # Schedule file deletion after response
        background_tasks.add_task(os.remove, file_path)

        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=os.path.basename(file_path)
        )

    except Exception as e:
        return {"error": str(e)}