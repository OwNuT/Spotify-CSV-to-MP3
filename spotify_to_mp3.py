#!/usr/bin/env python3
"""
Spotify CSV to MP3 Downloader
Simple and clean downloader using YouTube search and tracking history.
"""

import argparse
import csv
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# Colorama handling for Windows/Linux colored output
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

try:
    import yt_dlp
except ImportError:
    print("Error: 'yt-dlp' library is not installed. Install it with: pip install yt-dlp")
    sys.exit(1)


def get_color(color_name):
    if not HAS_COLORAMA:
        return ""
    colors = {
        "cyan": Fore.CYAN + Style.BRIGHT,
        "green": Fore.GREEN + Style.BRIGHT,
        "yellow": Fore.YELLOW + Style.BRIGHT,
        "red": Fore.RED + Style.BRIGHT,
        "gray": Fore.BLACK + Style.BRIGHT,
        "reset": Style.RESET_ALL,
    }
    return colors.get(color_name, "")


def print_banner():
    c_cyan = get_color("cyan")
    c_reset = get_color("reset")
    banner = f"""{c_cyan}
====================================================
  Spotify CSV to MP3 (Simple Downloader)
===================================================={c_reset}"""
    print(banner)


def setup_logging():
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"spotify_to_mp3_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
        ]
    )
    return log_file


def parse_csv(csv_path):
    tracks = []
    try:
        with open(csv_path, mode="r", encoding="utf-8-sig", errors="replace") as f:
            sample = f.read(4096)
            f.seek(0)
            delimiter = ";" if sample.count(";") > sample.count(",") else ","
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader, None)

            if not header:
                return tracks

            header_lower = [h.strip().lower() for h in header]
            title_idx = -1
            artist_idx = -1

            for cand in ["track name", "title", "name", "song", "titre"]:
                if cand in header_lower:
                    title_idx = header_lower.index(cand)
                    break

            for cand in ["artist name(s)", "artist name", "artist", "artiste", "artists"]:
                if cand in header_lower:
                    artist_idx = header_lower.index(cand)
                    break

            if title_idx == -1 or artist_idx == -1:
                title_idx, artist_idx = 0, 1 if len(header) > 1 else 0

            for row in reader:
                if not row:
                    continue
                title = row[title_idx].strip() if len(row) > title_idx else ""
                artist = row[artist_idx].strip() if len(row) > artist_idx else ""
                if title:
                    track_str = f"{title} - {artist}" if artist else title
                    tracks.append(track_str)
    except Exception as e:
        logging.error(f"Failed to parse CSV file: {e}")
        print(f"{get_color('red')}Error parsing CSV file: {e}{get_color('reset')}")
        sys.exit(1)

    return tracks


def load_history(history_file):
    if not os.path.isfile(history_file):
        return set()
    with open(history_file, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def save_to_history(history_file, track):
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"{track}\n")


def clean_string_for_matching(text):
    return re.sub(r"[^a-zA-Z0-9]", "", text).lower()


def file_exists_locally(output_dir, track):
    clean_track = clean_string_for_matching(track[:15])
    for entry in os.scandir(output_dir):
        if entry.is_file() and entry.name.endswith(".mp3"):
            clean_filename = clean_string_for_matching(entry.name)
            if clean_track in clean_filename:
                return entry.name
    return None


def download_track(track, output_dir, sleep_range=(2, 5), verbose=False):
    output_template = str(Path(output_dir) / "%(title)s.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'overwrites': False,
        'quiet': not verbose,
        'no_warnings': not verbose,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    query = f"{track} audio"
    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([query])
            return True, None
        except Exception as e:
            err_msg = str(e)
            if "HTTP Error 429" in err_msg or "Too Many Requests" in err_msg or "Sign in to confirm" in err_msg:
                log_msg = f"RATE LIMIT DETECTED on attempt {attempt}/{max_retries}. Pausing 60s..."
                logging.warning(log_msg)
                print(f"{get_color('yellow')}⚠️  {log_msg}{get_color('reset')}")
                time.sleep(60)
            else:
                log_msg = f"Attempt {attempt}/{max_retries} failed: {err_msg}"
                logging.warning(log_msg)
                if attempt < max_retries:
                    time.sleep(5)
    
    return False, "Failed after max retries."


def main():
    parser = argparse.ArgumentParser(description="Download Spotify CSV track list as MP3 files.")
    parser.add_argument("csv_file", help="Path to Spotify CSV export file")
    parser.add_argument("output_dir", nargs="?", default="./musiques", help="Output directory for MP3s (Default: ./musiques)")
    parser.add_argument("--sleep-min", type=int, default=2, help="Minimum sleep between requests")
    parser.add_argument("--sleep-max", type=int, default=5, help="Maximum sleep between requests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose yt-dlp logs")
    
    args = parser.parse_args()

    print_banner()
    log_file = setup_logging()

    if not os.path.isfile(args.csv_file):
        print(f"{get_color('red')}Error: CSV file '{args.csv_file}' not found.{get_color('reset')}")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    history_file = os.path.join(args.output_dir, "downloaded_history.txt")
    history = load_history(history_file)

    tracks = parse_csv(args.csv_file)
    total = len(tracks)

    if total == 0:
        print(f"{get_color('red')}No tracks found in CSV.{get_color('reset')}")
        sys.exit(1)

    print(f"{get_color('cyan')}ℹ Source file:{get_color('reset')} {args.csv_file}")
    print(f"{get_color('cyan')}ℹ Output directory:{get_color('reset')} {args.output_dir}")
    print(f"{get_color('green')}✔ Total tracks loaded: {total}{get_color('reset')}")
    print(get_color('gray') + "-" * 52 + get_color('reset'))

    skipped, success, failed = 0, 0, 0
    failed_tracks = []

    for idx, track in enumerate(tracks, start=1):
        print(f"\n{get_color('cyan')}[{idx}/{total}]{get_color('reset')} Processing: {track}")
        logging.info(f"Processing track {idx}/{total}: {track}")

        # 1. Vérification via l'historique CSV (fiabilité 100%)
        if track in history:
            msg = "Already downloaded in history (Skipped)"
            print(f"{get_color('cyan')}ℹ {msg}{get_color('reset')}")
            logging.info(f"{track}: {msg}")
            skipped += 1
            continue

        # 2. Vérification secondaire par nom de fichier partiel
        existing_file = file_exists_locally(args.output_dir, track)
        if existing_file:
            msg = f"Already exists locally: {existing_file}"
            print(f"{get_color('cyan')}ℹ {msg}{get_color('reset')}")
            logging.info(msg)
            save_to_history(history_file, track)  # Synchronise l'historique
            skipped += 1
            continue

        # Processus de téléchargement
        ok, err = download_track(
            track,
            args.output_dir,
            sleep_range=(args.sleep_min, args.sleep_max),
            verbose=args.verbose
        )

        if ok:
            print(f"{get_color('green')}✔ Successfully downloaded.{get_color('reset')}")
            logging.info(f"Successfully downloaded: {track}")
            save_to_history(history_file, track)
            success += 1
        else:
            print(f"{get_color('red')}✖ Download failed: {track}{get_color('reset')}")
            logging.error(f"Download failed for {track}: {err}")
            failed += 1
            failed_tracks.append(track)

        # Pause entre les requêtes
        sleep_time = max(args.sleep_min, args.sleep_max)
        time.sleep(sleep_time)

    # Summary
    print(f"\n{get_color('cyan')}===================================================={get_color('reset')}")
    print("                  SUMMARY                           ")
    print(f"{get_color('cyan')}===================================================={get_color('reset')}")
    print(f"Total processed     : {total}")
    print(f"Skipped (Existing)  : {skipped}")
    print(f"Successful downloads: {success}")
    if failed > 0:
        print(f"{get_color('red')}Failed downloads    : {failed}{get_color('reset')}")
        for ft in failed_tracks:
            print(f"  - {ft}")

    print(f"\nLog file saved to: {log_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{get_color('red')}Execution cancelled by user.{get_color('reset')}")
        sys.exit(130)