# Pad - Spotify Playlist Album Downloader

## 🎵 Overview
**Pad** is an automated tool that downloads entire albums from a Spotify playlist using a combination of **Spotify API**, **MusicBrainz API**, and **YouTube-DL**. The tool extracts all albums from a given playlist, fetches their tracklists, and downloads each song, organizing them neatly into folders.

## 🚀 Features
- ✅ **Fetch albums from a Spotify playlist**
- ✅ **Retrieve tracklists from MusicBrainz**
- ✅ **Fallback to YouTube search if missing**
- ✅ **Download songs using YouTube-DL**
- ✅ **Organized output: `Downloads/Artist/Album/Song.mp3`**

## 📂 Folder Structure
```
Pad/
├── pad.py               # Main script
├── albums.json          # Cached album data
├── README.md            # Project documentation
├── requirements.txt     # Dependencies
└── Downloads/           # Output folder
    ├── Artist 1/
    │   ├── Album 1/
    │   │   ├── Song1.mp3
    │   │   ├── Song2.mp3
    ├── Artist 2/
    │   ├── Album 2/
```

## 🛠 Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Pad.git
   cd Pad
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up Spotify API:**
   - Create a Spotify Developer Account
   - Get your `CLIENT_ID` and `CLIENT_SECRET`
   - Add them to `pad.py`

## 🎵 Usage
### **1️⃣ Fetch albums from a Spotify playlist**
```bash
python pad.py
```
It will prompt you to enter the playlist name. It will then fetch all albums and save them to `albums.json`.

### **2️⃣ Download albums from JSON**
```bash
python pad.py
```
It will read `albums.json`, fetch tracklists, and start downloading each song.

## 🔹 Example Output
```
🎵 Welcome to the Spotify Playlist to MP3 Downloader!
Do you want to fetch albums from a Spotify playlist? (yes/no): yes
Enter the Spotify playlist name: My Favorite Albums
✅ Saved 15 albums to albums.json.
Do you want to start downloading albums? (yes/no): yes
⬇️ Downloading: Artist - Song from YouTube...
✅ Download complete: Downloads/Artist/Album/Song.mp3
```

## 🛠 Dependencies
- `yt_dlp`
- `requests`
- `spotipy`
- `json`
- `os`

---
🎵 Happy Downloading! 🚀

