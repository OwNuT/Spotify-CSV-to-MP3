# 🎵 Spotify CSV to MP3 Downloader (Python Edition)

A fully cross-platform Python application to convert exported Spotify playlists into high-quality `.mp3` files via YouTube matching. 

Works natively on **Windows**, **macOS**, and **Linux**.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgray?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## 🌟 Key Features

* **100% Cross-Platform:** Native execution on Windows, macOS, and Linux without Bash dependencies.
* **Instant Resume & Zero-Network Duplicate Skip:** Scans local directory before making network calls. Skipping local files takes 0ms and saves network quota.
* **Smart Anti-Rate-Limit & Auto-Cooldown:** Automatically catches HTTP 429 / Captcha errors from YouTube, pauses execution for 60 seconds, and attempts retry.
* **Browser Cookies Support (`--browser`):** Uses your native browser session (Chrome, Firefox, Edge, Brave, Opera) to authenticate searches and completely bypass IP rate limits.
* **Proxy Support (`--proxy`):** Full HTTP, HTTPS, and SOCKS5 proxy support natively integrated.
* **Auto-Delimiter CSV Parser:** Reads Exportify or custom CSVs (comma or semicolon separated) with UTF-8 BOM protection.

---

## 📦 Requirements & Installation

### 1. Prerequisites
* **Python 3.8+**
* **FFmpeg:** Required for audio extraction to MP3.

---

### Windows Setup

1. **Install Python:** Download and install Python from [python.org](https://www.python.org/). Ensure you check **"Add Python to PATH"** during installation.
2. **Install FFmpeg:**
   * Easiest method via **winget** (PowerShell):
     ```cmd
     winget install "FFmpeg (Essential Build)"
     ```
   * Or via **Chocolatey**:
     ```cmd
     choco install ffmpeg
     ```
3. **Install Python Libraries:**
   ```cmd
   pip install yt-dlp colorama
   ```

---

### Linux / macOS Setup

* **Ubuntu / Debian:**
  ```bash
  sudo apt update && sudo apt install -y python3 python3-pip ffmpeg
  pip install yt-dlp colorama
  ```

* **Fedora:**
  ```bash
  sudo dnf install -y python3 python3-pip ffmpeg
  pip install yt-dlp colorama
  ```

* **macOS (Homebrew):**
  ```bash
  brew install python ffmpeg
  pip3 install yt-dlp colorama
  ```

---

## 🚀 Usage

### 1. Export Spotify Playlist
Export your target playlist to CSV using [Exportify](https://exportify.net).

### 2. Run the Script

**Basic Usage:**
```bash
python spotify_to_mp3.py playlist.csv
```

**Bypass Rate Limits (Recommended for >50 songs):**
```bash
# Windows / Linux / macOS using Chrome session
python spotify_to_mp3.py -b chrome playlist.csv ./my_music

# Using Firefox session
python spotify_to_mp3.py -b firefox playlist.csv ./my_music
```

---

## ⚙️ Command Line Options

```text
positional arguments:
  csv_file              Path to Spotify CSV export file
  output_dir            Output directory for MP3s (Default: ./musiques)

options:
  -h, --help            Show this help message and exit
  -b, --browser NAME    Extract cookies from browser (chrome, firefox, brave, edge, opera)
  -p, --proxy URL       Proxy URL (e.g. [http://127.0.0.1:8080](http://127.0.0.1:8080) or socks5://127.0.0.1:9050)
  --sleep-min SEC       Minimum sleep delay between requests (Default: 2)
  --sleep-max SEC       Maximum sleep delay between requests (Default: 5)
  -v, --verbose         Enable verbose logging
```

---

## ⚡ Possibilities, Limitations & Windows Caveats

### 1. SOCKS5 Proxies on Windows
* **SOCKS5 Support:** If you use a SOCKS5 proxy (`socks5://...`), Python requires the `PySocks` package.
  * **Fix:** Install it via `pip install PySocks`.
* HTTP/HTTPS proxies (`http://127.0.0.1:8080`) work out-of-the-box on all operating systems without extra packages.

### 2. Browser Cookies Access (`-b` / `--browser`)
* **Windows Chrome / Edge Lock:** Windows locks browser database files while the browser is open. 
  * **Fix:** If `--browser chrome` or `--browser edge` fails on Windows, **close your browser entirely** before running the script.
* **Firefox:** Firefox handles file locking better and usually works even while open.

### 3. YouTube Search Quotas (HTTP 429)
* **Unauthenticated Requests:** YouTube limits consecutive search requests from a single IP to ~50–60 queries within a short window.
* **Auto-Cooldown Mechanism:** If blocked, the script will wait 60 seconds automatically before resuming. If left running, it will eventually complete the whole list.
* **Immediate Resume:** Stopping the script and restarting it is instant: existing `.mp3` files are recognized locally, skipping YouTube requests completely.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
