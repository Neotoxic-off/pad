import yt_dlp
import requests
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 🔹 REPLACE WITH YOUR SPOTIFY API CREDENTIALS
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""

class SpotifyPlaylistFetcher:
    """Fetches albums from a Spotify playlist and saves them to a JSON file."""
    
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
        ))

    def find_playlist_id(self, playlist_name):
        """Search for a playlist by name and return its ID."""
        results = self.sp.search(q=playlist_name, type="playlist", limit=1)
        if results["playlists"]["items"]:
            return results["playlists"]["items"][0]["id"]
        print(f"❌ Playlist '{playlist_name}' not found.")
        return None

    def get_albums_from_playlist(self, playlist_id):
        """Extract all albums from a given Spotify playlist (handles pagination)."""
        albums = []
        results = self.sp.playlist_tracks(playlist_id)
        
        while results:
            for item in results["items"]:
                track = item["track"]
                if not track:  # Sometimes Spotify returns None tracks
                    continue
                
                album_name = track["album"]["name"]
                artist_name = track["artists"][0]["name"]
                album_entry = {"artist": artist_name, "album": album_name}

                if album_entry not in albums:  # Avoid duplicates
                    albums.append(album_entry)

            # Fetch next page
            results = self.sp.next(results) if results["next"] else None

        return albums

    def save_albums_to_json(self, albums, json_file="albums.json"):
        """Saves album data to a JSON file."""
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(albums, file, indent=4, ensure_ascii=False)
        print(f"✅ Saved {len(albums)} albums to {json_file}.")

    def run(self, playlist_name):
        """Main function to fetch albums from a playlist."""
        playlist_id = self.find_playlist_id(playlist_name)
        if playlist_id:
            albums = self.get_albums_from_playlist(playlist_id)
            self.save_albums_to_json(albums)


class AlbumDownloader:
    """Fetches album tracklist from MusicBrainz and downloads each song from YouTube."""

    def __init__(self, artist, album, output_folder="Downloads"):
        self.artist = artist
        self.album = album
        self.output_folder = output_folder
        self.base_url = "https://musicbrainz.org/ws/2/release/"
        self.tracks = []

    def fetch_album_tracks(self):
        """Fetch album tracklist from MusicBrainz API."""
        print(f"🔎 Fetching tracklist for: {self.artist} - {self.album}...")
        params = {"query": f'artist:"{self.artist}" AND release:"{self.album}"', "fmt": "json"}
        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            print("❌ Error fetching album data.")
            return False

        data = response.json()
        if "releases" not in data or not data["releases"]:
            print("❌ Album not found!")
            return False

        release_id = data["releases"][0]["id"]
        tracklist_url = f"https://musicbrainz.org/ws/2/release/{release_id}?inc=recordings&fmt=json"

        response = requests.get(tracklist_url)
        if response.status_code != 200:
            print("❌ Error fetching tracklist.")
            return False

        release_data = response.json()
        self.tracks = [track["title"] for track in release_data["media"][0]["tracks"]]
        return True

    def search_youtube(self, track):
        """Search for a track on YouTube and return the best video URL."""
        ydl_opts = {"quiet": True, "extract_flat": True, "force_generic_extractor": True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch1:{self.artist} - {track} audio", download=False)

        if "entries" in search_results and search_results["entries"]:
            return search_results["entries"][0]["url"]
        return None

    def download_song(self, url, track):
        """Download a single track from YouTube."""
        artist_folder = os.path.join(self.output_folder, self.artist)
        album_folder = os.path.join(artist_folder, self.album)
        os.makedirs(album_folder, exist_ok=True)  # Ensure directory exists

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(album_folder, f"{track}.%(ext)s"),
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def run(self):
        """Main function to fetch, search, and download all songs in the album."""
        if not self.fetch_album_tracks():
            return

        for track in self.tracks:
            print(f"🎵 Searching YouTube for: {self.artist} - {track}...")
            video_url = self.search_youtube(track)

            if video_url:
                print(f"⬇️ Downloading: {track} from {video_url}")
                self.download_song(video_url, track)
            else:
                print(f"❌ No results found for {track}")


class AlbumManager:
    """Handles loading albums from JSON and triggering downloads."""

    def __init__(self, json_file="albums.json"):
        self.json_file = json_file
        self.albums = self.load_albums()

    def load_albums(self):
        """Load album list from a JSON file."""
        with open(self.json_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def download_all_albums(self):
        """Trigger downloads for all albums in the JSON file."""
        for album in self.albums:
            downloader = AlbumDownloader(album["artist"], album["album"])
            downloader.run()


if __name__ == "__main__":
    print("🎵 Welcome to the Spotify Playlist to MP3 Downloader!")

    # Step 1: Fetch albums from a Spotify playlist
    fetch_spotify = input("Do you want to fetch albums from a Spotify playlist? (yes/no): ").strip().lower()
    if fetch_spotify == "yes":
        playlist_name = input("Enter the Spotify playlist name: ").strip()
        SpotifyPlaylistFetcher().run(playlist_name)

    # Step 2: Download albums
    download_now = input("Do you want to start downloading albums? (yes/no): ").strip().lower()
    if download_now == "yes":
        AlbumManager().download_all_albums()
