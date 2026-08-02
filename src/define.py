dev = 1

if dev:
    INPUT_PATH = '/Users/quentinhauuy/code/anki/input.txt'
    IMAGES_SRC_DIR = '/Users/quentinhauuy/code/anki/images'
    TRASH_DIR = "/Users/quentinhauuy/code/anki/trash"
else:
    INPUT_PATH = '/Users/quentinhauuy/Documents/anki/input.txt'
    IMAGES_SRC_DIR = '/Users/quentinhauuy/Documents/anki/images'
    TRASH_DIR = "/Users/quentinhauuy/Documents/anki/poubelle/poubelle_du_script"

IMAGES_DST_DIR = "/Users/quentinhauuy/Library/Application Support/Anki2/Quentin/collection.media"

SPOTIFY_CLIENT_ID = "efe7eb169b7d4e40a9d22123ea9e3912"
SPOTIFY_CLIENT_SECRET = "713431dadce14f2a972e35a713caf19c"

SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SPOTIFY_SCOPE = "playlist-read-private playlist-modify-private"
SPOTIFY_TOKEN_FILE = "/Users/quentinhauuy/code/anki/spotify_token.json"

RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

LINE_HEIGHT = 36 # line-height en pixels dans le CSS des cartes

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
ANKI_CONNECT_VERSION = 6

DECK_BASE = "base"
DECK_TAPER = "taper"
DECK_PAPIER = "papier"
DECK_SONG = "extern::song"
DECK_POUBELLE = "poubelle"

MODEL_CARD = "card"
MODEL_CARD_FIELDS = "front", "back"

MODEL_REPLACE = "replace"
MODEL_REPLACE_FIELDS = "front", "back"

MODEL_CLOZE = "cloze"
MODEL_CLOZE_FIELDS = "text", "extra"

MODEL_TAPE = "tapé"
MODEL_TAPE_FIELDS = "front", "back", "extra"

MODEL_CLOZE_TAPE = "cloze tapé"
MODEL_CLOZE_TAPE_FIELDS = "text", "extra"

NB_FIELDS = {
    "C1": 2,
    "C2": 3,
    "C3": 2,
    "R1": 2,
    "R3": 2,
    "Z1": 2,
    "Z2": 2,
    "Z3": 2,
    "MS": 4,
    "SONG": 2,
}

ANKI_CONNECT_MODELS = {
    "C1": {
        "modelName": MODEL_CARD,
        "deckName": DECK_BASE,
        "fields": dict.fromkeys(MODEL_CARD_FIELDS, "")
    },
    "C2": {
        "modelName": MODEL_TAPE,
        "deckName": DECK_TAPER,
        "fields": dict.fromkeys(MODEL_TAPE_FIELDS, "")
    },
    "C3": {
        "modelName": MODEL_CARD,
        "deckName": DECK_PAPIER,
        "fields": dict.fromkeys(MODEL_CARD_FIELDS, "")
    },
    "R1": {
        "modelName": MODEL_REPLACE,
        "deckName": DECK_BASE,
        "fields": dict.fromkeys(MODEL_REPLACE_FIELDS, "")
    },
    "R3": {
        "modelName": MODEL_REPLACE,
        "deckName": DECK_PAPIER,
        "fields": dict.fromkeys(MODEL_REPLACE_FIELDS, "")
    },
    "Z1": {
        "modelName": MODEL_CLOZE,
        "deckName": DECK_BASE,
        "fields": dict.fromkeys(MODEL_CLOZE_FIELDS, ""),
    },
    "Z2": {
        "modelName": MODEL_CLOZE_TAPE,
        "deckName": DECK_TAPER,
        "fields": dict.fromkeys(MODEL_CLOZE_TAPE_FIELDS, "")
    },
    "Z3": {
        "modelName": MODEL_CLOZE,
        "deckName": DECK_PAPIER,
        "fields": dict.fromkeys(MODEL_CLOZE_FIELDS, "")
    },
    "SONG": {
        "modelName": MODEL_CARD,
        "deckName": DECK_SONG,
        "fields": dict.fromkeys(MODEL_CARD_FIELDS, "")
    }
}

SEPARATORS = '-', '--', '---', '-)', '-r', '---r', '-song'

GET_SEPARATOR = {
    (MODEL_CARD, DECK_BASE): "-", # C1
    (MODEL_TAPE, DECK_TAPER): "--", # C2
    (MODEL_CARD, DECK_PAPIER): "---", # C3
    (MODEL_REPLACE, DECK_BASE): "-r", # R1
    (MODEL_REPLACE, DECK_PAPIER): "---r", # R3
    (MODEL_CLOZE, DECK_BASE): "-", # Z1
    (MODEL_CLOZE_TAPE, DECK_TAPER): "--", # Z2
    (MODEL_CLOZE, DECK_PAPIER): "---", # Z3,
    (MODEL_CARD, DECK_SONG): "-song" # SONG
}

# nom d'un format -> regex
FORMATS = {
    "img": r'<img h=([^\n]*)\n([^>]*)>',
        # groupe 1 : hauteur
        # groupe 2 : nom du fichier
    "decode_img": r'<img src="([^"]+)"[^>]*>',
        # groupe 1 : nom du fichier
    "red": r'<red>([\s\S]*?)</red>',
        # groupe 1 : contenu de la balise
    "decode_red": r'<span style="color: red;">([\s\S]*?)</span>',
        # groupe 1 : contenu de la balise
    "sup": r"<sup>([\s\S]*?)</sup>",
        # groupe 1 : contenu de la balise
    "sub": r"<sub>([\s\S]*?)</sub>",
        # groupe 1 : contenu de la balise
    "b": r"<b>([\s\S]*?)</b>",
        # groupe 1 : contenu de la balise
    "cloze": r"\{\{c(\d+)::([\s\S]*?)(?:::([\s\S]*?))?\}\}",
        # groupe 1 : numéro de carte
        # groupe 2 : champ principal
        # groupe 3 : champ d'indice (ou None)
    "phonetics": r'(?<!\\)//([\s\S]*?)(?<!\\)//',
        # groupe 1 : texte entre "//"
    "link": r'<link:([^>]*)>',
        # groupe 1 : lien
    "decode_link": r'<a href="([^"]*)">link</a>'
        # groupe 1 : lien
}
