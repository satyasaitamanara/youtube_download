from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os
import base64

app = FastAPI()

# CORS middleware (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Decode cookies_base64.txt to cookies.txt (if needed)
if os.path.exists("cookies_base64.txt"):
    with open("cookies_base64.txt", "r") as f:
        encoded = f.read()
    with open("cookies.txt", "wb") as f:
        f.write(base64.b64decode(encoded))

# Create downloads folder if not exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")
    download_type = data.get("type", "video")  # "video" or "audio"

    # yt-dlp options
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt' if os.path.exists("cookies.txt") else None,
    }

    if download_type == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        })
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            cleaned_filename = filename.replace("\\", "/")  # for Windows paths
            return {
                "message": "Download completed",
                "download_url": f"http://localhost:5000/{cleaned_filename}"
            }
    except Exception as e:
        return {"error": str(e)}

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
