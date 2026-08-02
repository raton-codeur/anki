import define
from utils import ankiconnect
import spotipy, re
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

def decode(s):
    s = s.replace("&nbsp;", ' ')
    s = s.replace("<br>", '\n')
    s = s.replace("&lt;", "<").replace("&gt;", ">")
    return s

def get_songs() :
    card_ids = ankiconnect(
        "findCards",
        {"query": f'deck:extern::song is:due'}
    )
    cards = ankiconnect(
        "cardsInfo",
        {"cards": card_ids}
    )

    # de la plus ancienne à la plus récente
    cards.sort(key=lambda card: card["cardId"])

    result = []
    for card in cards :
        content = decode(card["fields"]["front"]["value"])
        first_line = content.splitlines()[0]
        title, _, artist = first_line.partition(" - ")
        match = re.search(define.FORMATS["decode_link"], content)
        link = match.group(1) if match else None
        if "paroles" not in content:
            content = ""
        result.append((title, artist, link, content))
    return result

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=define.SPOTIFY_CLIENT_ID,
        client_secret=define.SPOTIFY_CLIENT_SECRET,
        redirect_uri=define.SPOTIFY_REDIRECT_URI,
        scope=define.SPOTIFY_SCOPE,
        cache_handler=CacheFileHandler(
            cache_path=define.SPOTIFY_TOKEN_FILE
        ),
    )
)

def search_to_uri(title: str, artist: str) -> str:
    tracks = spotify.search(
        q=f'track:"{title}" artist:"{artist}"',
        type="track",
        limit=1,
    )["tracks"]["items"]
    if not tracks:
        raise ValueError(f"introuvable : {title} — {artist}")
    return tracks[0]["uri"]

def get_or_create_playlist(name: str) -> dict:
    playlists = spotify.current_user_playlists(limit=20)
    while playlists:
        for playlist in playlists["items"]:
            if playlist["name"] == name:
                print(f"playlist '{name}' mise à jour")
                return playlist
        playlists = (
            spotify.next(playlists)
            if playlists["next"]
            else None
        )
    print(f"playlist '{name}' crée")
    return spotify.current_user_playlist_create(
        name=name,
        public=False,
    )

def replace_playlist(playlist_id: str, song_uris: list[str]):
    # on doit remplir la playlist par groupe de 100

    spotify.playlist_replace_items(
        playlist_id,
        song_uris[:100],
    )

    for start in range(100, len(song_uris), 100):
        spotify.playlist_add_items(
            playlist_id,
            song_uris[start:start + 100],
        )

def handle_spotify(songs):
    song_uris = []
    for title, artist, link, _ in songs:
        if link:
            song_uris.append(link)
        else:
            song_uris.append(search_to_uri(title, artist))

    playlist_name = datetime.now().strftime("%d/%m/%Y apprendre")
    playlist = get_or_create_playlist(playlist_name)
    replace_playlist(
        playlist["id"],
        song_uris,
    )

    print(f"nombre de titres : {len(song_uris)}")

def copy_songs_to_input(songs) :
    data = []
    for _, _, _, content in songs :
        if content:
            data.append(f"-\n{content}")
    data = "\n".join(data)
    with open(define.INPUT_PATH, "a") as f:
        f.write(data)
