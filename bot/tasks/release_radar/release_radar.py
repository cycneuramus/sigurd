import datetime
import logging
import os
from typing import Optional

import tekore as tk
from tinydb import Query, TinyDB
from utils import utils
from utils.spotify_data import monitored_artists

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - line %(lineno)d: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("log", "w"), logging.StreamHandler()],
)


class LatestAlbumDatabase:
    """
    Database entries follow the pattern:
        "artist": "<artist name>", "album": "<latest album> (<year>)"

    Example:
        "artist": "The Beatles", "album": "Let It Be (1970)"
    """

    db = TinyDB("db")
    entry = Query()

    def __init__(self):
        logging.debug(f"{__class__.__name__}: instantiating class")

    def query(self, artist: str) -> Optional[str]:
        logging.debug(f"{__class__.__name__}: querying {artist}")

        entry = self.db.get(self.entry.artist == artist)
        if entry is not None:
            return entry.get("album")

    def insert(self, artist: str, album: str) -> None:
        logging.debug(f"{__class__.__name__}: inserting {artist} with {album}")

        self.db.insert(
            {
                "artist": artist,
                "album": album,
            }
        )

    def update(self, artist: str, album: str) -> None:
        logging.debug(f"{__class__.__name__}: updating {artist} with {album}")

        self.db.update(
            {"album": album},
            self.entry.artist == artist,
        )


class LatestAlbum:
    @staticmethod
    def create_spotify_client() -> tk.Spotify:
        logging.debug("Creating Spotify client")

        token = tk.request_client_token(
            os.environ["SPOTIFY_CLIENT_ID"], os.environ["SPOTIFY_CLIENT_SECRET"]
        )

        return tk.Spotify(
            token,
            tk.CachingSender(
                max_size=256, sender=tk.RetryingSender(retries=2)
            ),
        )

    spotify = create_spotify_client()

    def __init__(self, artist: str, artist_id: str):
        logging.debug(f"{__class__.__name__}: instantiating class")

        self.artist = artist
        self.artist_id = artist_id
        self.name: str
        self.year: str
        self.url: str
        self.id: str
        self.type: str
        self.summary: str

        self.get_album_data()

    @utils.retry(times=2)
    def get_album_data(self) -> None:
        logging.info(f"{self.artist}: getting latest album")

        try:
            album = self.spotify.artist_albums(
                self.artist_id,
                include_groups=["album", "single"],
                limit=1,
            ).items[0]

            self.name = album.name
            self.year = datetime.datetime.strptime(
                album.release_date, "%Y-%m-%d"
            ).strftime("%Y")
            self.url = album.external_urls["spotify"]
            self.id = album.id
            self.type = album.type
            self.summary = f"{self.name} ({self.year})"
        except IndexError:
            logging.error("No album found for {self.artist}")

    @utils.retry(times=2)
    def get_tracks_data(self) -> tk.model.SimpleTrackPaging:
        logging.debug("Getting tracks")
        return self.spotify.album_tracks(self.id)

    @utils.retry(times=2)
    def get_audio_features(self) -> dict:
        logging.debug("Getting audio features for tracks")

        tracks = self.get_tracks_data()
        ids = [track.id for track in tracks.items]
        tracks_analysis = self.spotify.tracks_audio_features(track_ids=ids)

        audio_features = {}
        for track in tracks_analysis:
            if track is None:
                continue

            # get track title from earlier API request by matching track ID
            title = ""
            for data in tracks.items:
                if data.id == track.id:
                    title = data.name
                    break

            audio_features.update(
                {
                    title: [
                        round(track.energy * 100),
                        round(track.valence * 100),
                        track.mode,
                    ]
                }
            )

        return audio_features

    @utils.retry(times=2)
    def get_power_analysis(self) -> str:
        logging.debug("Getting power analysis")

        tracks_features = self.get_audio_features()

        # get track with highest combined sum of list values
        # https://redd.it/37iaj4
        track_title = max(
            tracks_features, key=lambda k: sum(tracks_features.get(k))
        )

        track_energy = tracks_features[track_title][0]
        track_valence = tracks_features[track_title][1]

        if tracks_features[track_title][2] == 0:
            track_mode = "minor"
        else:
            track_mode = "major"

        return (
            f"Based on energy ({track_energy}%) and"
            f" valence ({track_valence}%) levels, the song"
            f' "{track_title}" seems to be the most powerful.'
            f" It sounds to be mostly in the {track_mode} key."
        )


class NewAlbumMessage:
    def __init__(self, album: LatestAlbum):
        logging.debug(f"{__class__.__name__}: instantiating class")

        self.album = album
        self.power_analysis = self.album.get_power_analysis()
        self.message = self.craft_message()

    def craft_message(self) -> str:
        logging.debug(
            f"Crafting message for {self.album.artist}: {self.album.summary}. Album type: {self.album.type}"
        )

        if self.album.type == "album":
            release_info = f"New album by {self.album.artist}"
            message = (
                f"{release_info}: {self.album.summary}."
                "\n\n"
                f"{self.album.url}"
                "\n\n"
                f"{self.power_analysis}"
            )
        else:
            release_info = f"New single by {self.album.artist}"
            message = (
                f"{release_info}: {self.album.summary}."
                "\n\n"
                f"{self.album.url}"
            )

        return message


def main():
    if not utils.internet():
        logging.error("No internet connectivity, exiting")
        exit()
    os.chdir(os.path.dirname(__file__))

    new_albums = 0
    db = LatestAlbumDatabase()
    logging.info("Checking for new albums")

    for artist, artist_id in monitored_artists.items():
        latest_album = LatestAlbum(artist, artist_id)
        if not latest_album:
            continue

        album_in_db = db.query(artist)
        if album_in_db is None:
            logging.info(
                f"{artist}: no entry in database, inserting {latest_album.summary}"
            )

            db.insert(artist, latest_album.summary)

        elif album_in_db != latest_album.summary:
            logging.info(f"New release by {artist}: {latest_album.summary}")

            msg = NewAlbumMessage(latest_album)
            utils.push(msg.message)
            new_albums += 1
            db.update(artist, latest_album.summary)

        else:
            logging.debug(f"{artist}: no new releases since {album_in_db}")

    logging.info(f"{new_albums} new albums")


if __name__ == "__main__":
    main()
