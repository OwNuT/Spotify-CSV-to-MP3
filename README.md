# 🎵 Spotify CSV to MP3 Downloader

An automated Bash script to download tracks from any Spotify playlist as high-quality MP3s via YouTube search, completely bypassing the restricted Spotify API endpoints.

![Bash](https://img.shields.io/badge/Language-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Licence](https://img.shields.io/badge/License-MIT-blue.style=for-the-badge)

---

## 🌟 Features

* **No Spotify API limits:** Works with public, private, or third-party playlists via simple CSV exports.
* **Automatic YouTube Match:** Searches and matches titles using `yt-dlp` (`ytsearch1:` engine).
* **Automatic CSV Parsing:** Python-powered header detection (compatible with Exportify, custom CSVs, separated by commas or semicolons).
* **High Quality Audio:** Extracts and converts streams directly into 320kbps VBR MP3s via `ffmpeg`.
* **Rich Terminal UI:** Color-coded console feedback, progress tracking, verbose mode, and graceful CTRL+C cleanup.
* **Robust Logging:** Built-in logging system keeping full trace of operations and failures under `./logs/`.

---

## 📋 Prerequisites & Dependencies

Ensure you have the following installed on your machine:

- **`yt-dlp`**: Powerful YouTube downloader.
- **`ffmpeg`**: Media encoder for audio processing.
- **`python3`**: Used strictly for native CSV parsing (pre-installed on most UNIX systems).

### Installation Commands

#### Fedora / RHEL
```bash
sudo dnf install -y ffmpeg python3
pip install --user yt-dlp
