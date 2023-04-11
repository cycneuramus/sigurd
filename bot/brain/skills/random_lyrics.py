import random

import lyricsgenius


def cleanup_lyrics(lyrics: str, title: str) -> str:
    for r in (
        (f"{title} Lyrics", ""),
        ("Embed", ""),
        ("(Instrumental)\n", ""),
        ("(Solo)\n", ""),
        ("(solos)\n", ""),
        ("\n\n", "\n"),
        ("\n\n\n", "\n"),
    ):
        lyrics = lyrics.replace(*r)

    return lyrics


def get_random_phrase(lyrics: str, phrase_length: int) -> str:
    lyric_lines = lyrics.splitlines()
    lyrics_length = len(lyric_lines) - 1

    start_at = random.choice(range(0, lyrics_length - phrase_length))

    selection = ""
    for line in range(start_at, start_at + phrase_length):
        selection += lyric_lines[line] + "\n"

    return selection.rstrip()


def get_lyrics(artist: str):
    genius = lyricsgenius.Genius()

    genius.remove_section_headers = True
    genius.skip_non_songs = True
    genius.excluded_terms = ["(Remix)", "(Live)"]

    msg = None
    attempts = 0
    while attempts < 2:
        try:
            artist_data = genius.search_artists(artist, per_page=1)
            artist_id = artist_data["sections"][0]["hits"][0]["result"]["id"]

            songs_all = genius.artist_songs(artist_id)
            song_data = random.choice(songs_all["songs"])

            title = song_data["title"].replace(" (Live)", "")
            url = song_data["url"]

            lyrics_raw = genius.lyrics(
                song_url=url, remove_section_headers=True
            )
            lyrics_clean = cleanup_lyrics(lyrics_raw, title)

            lyrics_phrase = get_random_phrase(lyrics_clean, 5)

            msg = f'{lyrics_phrase}\n\n– "{title}"'
            break
        except Exception:
            attempts += 1
            continue

    if msg is None:
        return "I can't seem to find any lyrics. 😠"
    else:
        return msg
