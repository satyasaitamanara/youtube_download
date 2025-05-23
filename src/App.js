import { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [activeButton, setActiveButton] = useState(null);
  // const [downloadTime, setDownloadTime] = useState(null);

  const download = async (type) => {
    if (!url) {
      setError('Please enter a YouTube URL');
      return;
    }

    setLoading(true);
    setError('');
    setSuccessMsg('');
    setActiveButton(type);
    const startTime = performance.now(); // Start time

    try {
      const response = await axios.post('https://youtube-download-4yoo.onrender.com/download', {
        url,
        type,
      });

      const endTime = performance.now(); // End time
      const timeTaken = ((endTime - startTime) / 1000).toFixed(2); // seconds

      window.open(response.data.download_url, '_blank');
      setSuccessMsg(`Download completed in ${timeTaken} seconds.`);
      // setDownloadTime(timeTaken);
      setUrl(''); // Clear input field
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to download. Invalid URL or server error.');
    } finally {
      setLoading(false);
      setActiveButton(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex flex-col">
      

      <header className="p-6 text-center">
        <h1 className="text-4xl font-bold text-white animate-pulse md:text-5xl">
          YouTube Downloader
        </h1>
        <p className="text-white opacity-80 mt-2">Download videos and audio in high quality</p>
      </header>

      <main className="flex-grow flex items-center justify-center p-4">
        <div className="card">
          <input
            type="text"
            placeholder="Paste YouTube URL here..."
            className="input-field"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setError('');
              setSuccessMsg('');
            }}
            onKeyPress={(e) => e.key === 'Enter' && download('video')}
          />

          {error && <div className="error-message">{error}</div>}
          {successMsg && <div className="text-green-600 font-medium mt-2">{successMsg}</div>}

          <div className="flex flex-col sm:flex-row gap-4 mt-4">
            <button
              onClick={() => download('video')}
              disabled={loading}
              className={`btn btn-primary ${activeButton === 'video' ? 'animate-bounce' : ''}`}
            >
              {loading && activeButton === 'video' ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="loading-spinner"></span> Processing...
                </span>
              ) : 'Download Video'}
            </button>
            <button
              onClick={() => download('audio')}
              disabled={loading}
              className={`btn btn-secondary ${activeButton === 'audio' ? 'animate-bounce' : ''}`}
            >
              {loading && activeButton === 'audio' ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="loading-spinner"></span> Processing...
                </span>
              ) : 'Download MP3'}
            </button>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>© {new Date().getFullYear()} YouTube Downloader | Built with React & Python</p>
        <p className="mt-1 text-xs opacity-70">For educational purposes only</p>
      </footer>
    </div>
  );
}

export default App;
