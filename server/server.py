from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os
import base64

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Decode and save the cookies file from base64
if os.path.exists("cookies_base64.txt"):
    with open("cookies_base64.txt", "rb") as f:
        encoded = f.read()
    with open("cookies.txt", "wb") as f:
        f.write(base64.b64decode(encoded))

# Ensure downloads folder exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.get("/")
def root():
    return {"message": "YouTube Downloader is live."}

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")
    download_type = data.get("type", "video")

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'cookies': 'cookies.txt',  # must exist and be valid Netscape format
    }

    if download_type == "audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            filename = filename.replace("\\", "/")
            filename = os.path.basename(filename)
            return {
                "message": "Download successful",
                "file_name": filename,
                "download_url": f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/downloads/{filename}"
            }
    except Exception as e:
        return {"error": str(e)}

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
