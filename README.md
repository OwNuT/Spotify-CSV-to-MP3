# 🎵 Spotify CSV to MP3 Downloader

An automated Bash script to download tracks from any Spotify playlist as high-quality MP3s via YouTube search, completely bypassing restricted Spotify API endpoints.

![Bash](https://img.shields.io/badge/Language-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## 🌟 Features

* **No Spotify API limits:** Works with public, private, or third-party playlists via simple CSV exports.
* **Anti-Ban Protection:** Built-in sleep intervals, random User-Agents, and automated pause on YouTube rate limits (HTTP 429).
* **Automatic YouTube Match:** Searches and matches titles using `yt-dlp` (`ytsearch1:` engine).
* **Smart CSV Parsing:** Python-powered header detection (compatible with Exportify, custom CSVs, separated by commas or semicolons).
* **High Quality Audio:** Extracts and converts streams directly into high-quality MP3s via `ffmpeg`.
* **Rich Terminal UI:** Color-coded console feedback, progress tracking, verbose mode, proxy support, and graceful `CTRL+C` cleanup.
* **Robust Logging:** Built-in logging system keeping full trace of operations and failures under `./logs/`.

---

## 📋 Prerequisites & Dependencies

Ensure you have the following installed on your system:

* **`yt-dlp`**: Powerful YouTube downloader.
* **`ffmpeg`**: Media encoder for audio processing.
* **`python3`**: Used strictly for native CSV parsing (pre-installed on most UNIX systems).

### Installation Commands

#### Fedora / RHEL
```bash
sudo dnf install -y ffmpeg python3
pip install --user yt-dlp
```

#### Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y ffmpeg python3 python3-pip
pip install --user yt-dlp
```

#### Arch Linux
```bash
sudo pacman -S ffmpeg python3 yt-dlp
```

---

## 🚀 Quick Start Guide

### Step 1: Export your Spotify Playlist to CSV
1. Go to [Exportify](https://exportify.net) and log in with your Spotify Account.
2. Export your target playlist as a `.csv` file and place it in your working directory.

### Step 2: Clone & Make Executable
```bash
git clone [https://github.com/OwNuT/spotify-csv-to-mp3.git](https://github.com/OwNuT/spotify-csv-to-mp3.git)
cd spotify-csv-to-mp3
chmod +x spotify-csv-to-mp3.sh
```

### Step 3: Run the Script
```bash
./spotify-csv-to-mp3.sh ./my_playlist.csv ./music_output
```

---

## ⚙️ Options & Usage

```text
Usage: ./spotify-csv-to-mp3.sh [options] <fichier_playlist.csv> [dossier_de_sortie]

Options:
  -p, --proxy URL      Pass requests through a proxy (e.g. socks5://127.0.0.1:9050)
  --sleep-min SEC      Minimum sleep delay between requests (Default: 3)
  --sleep-max SEC      Maximum sleep delay between requests (Default: 8)
  -v, --verbose        Displays live detailed output from yt-dlp for debugging
  -q, --quiet          Hides non-critical standard informational messages
  -h, --help           Shows the command line help page
```

### Examples

**Standard Download:**
```bash
./spotify-csv-to-mp3.sh playlist.csv
```

**Using a Proxy (Anti-Ban / Tor):**
```bash
./spotify-csv-to-mp3.sh -p socks5://127.0.0.1:9050 playlist.csv ~/Music/Spotify
```

**Verbose Mode (Debugging):**
```bash
./spotify-csv-to-mp3.sh -v my_playlist.csv
```

---

## 📂 Project Structure

```text
.
├── spotify-csv-to-mp3.sh  # Main executable script
├── logs/                  # Detailed execution logs (created automatically)
├── README.md              # Project documentation
└── LICENSE                # License information
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
