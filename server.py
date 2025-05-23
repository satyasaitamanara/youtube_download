import os
import yt_dlp
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")
    download_type = data.get("type", "video")

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'www.youtube.com.cookies.json', 
    }

    if download_type == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'cookiefile': 'www.youtube.com.cookies.json', 
        })
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return {"download_url": f"/{filename}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Use PORT from environment
    uvicorn.run(app, host="0.0.0.0", port=port)
