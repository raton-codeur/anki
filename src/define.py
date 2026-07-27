RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# INPUT_PATH = '/Users/quentinhauuy/Documents/anki/input.txt'
INPUT_PATH = 'input.txt'

# IMAGES_SRC_DIR = "/Users/quentinhauuy/Downloads"
IMAGES_SRC_DIR = 'images'
IMAGES_DST_DIR = "/Users/quentinhauuy/Library/Application Support/Anki2/Quentin/collection.media"

# LOG_DIR = "/Users/quentinhauuy/Documents/anki/logs"
TRASH_DIR = "/Users/quentinhauuy/code/anki/trash"

# MS_OUTPUT_PATH = "/tmp/mosalingua_output.txt"
MS_OUTPUT_PATH = "mosalingua_output.txt"

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
ANKI_CONNECT_VERSION = 6

DECK_1 = "1 - basique"
DECK_2 = "2 - taper"
DECK_3 = "3 - écrire"
TRASH_DECK = "poubelle"

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
    "MS": 4
}

ANKI_CONNECT_MODELS = {
    "C1": {
        "modelName": MODEL_CARD,
        "deckName": DECK_1,
        "fields": dict.fromkeys(MODEL_CARD_FIELDS, "")
    },
    "C2": {
        "modelName": MODEL_TAPE,
        "deckName": DECK_2,
        "fields": dict.fromkeys(MODEL_TAPE_FIELDS, "")
    },
    "C3": {
        "modelName": MODEL_CARD,
        "deckName": DECK_3,
        "fields": dict.fromkeys(MODEL_CARD_FIELDS, "")
    },
    "R1": {
        "modelName": MODEL_REPLACE,
        "deckName": DECK_1,
        "fields": dict.fromkeys(MODEL_REPLACE_FIELDS, "")
    },
    "R3": {
        "modelName": MODEL_REPLACE,
        "deckName": DECK_3,
        "fields": dict.fromkeys(MODEL_REPLACE_FIELDS, "")
    },
    "Z1": {
        "modelName": MODEL_CLOZE,
        "deckName": DECK_1,
        "fields": dict.fromkeys(MODEL_CLOZE_FIELDS, ""),
    },
    "Z2": {
        "modelName": MODEL_CLOZE_TAPE,
        "deckName": DECK_2,
        "fields": dict.fromkeys(MODEL_CLOZE_TAPE_FIELDS, "")
    },
    "Z3": {
        "modelName": MODEL_CLOZE,
        "deckName": DECK_3,
        "fields": dict.fromkeys(MODEL_CLOZE_FIELDS, "")
    }
}

SEPARATORS = '-', '--', '---', '-)', '-r', '---r'

GET_SEPARATOR = {
    (MODEL_CARD, DECK_1): "-", # C1
    (MODEL_TAPE, DECK_2): "--", # C2
    (MODEL_CARD, DECK_3): "---", # C3
    (MODEL_REPLACE, DECK_1): "-r", # R1
    (MODEL_REPLACE, DECK_3): "---r", # R3
    (MODEL_CLOZE, DECK_1): "-", # Z1
    (MODEL_CLOZE_TAPE, DECK_2): "--", # Z2
    (MODEL_CLOZE, DECK_3): "---" # Z3
}

# nom d'un format -> regex
FORMATS = {
    "img": r'<img(\d*)>([\s\S]*?)</img>', # ["valeur pour height" (ou ""), "nom de fichier"]
    "decode_img": r'<img src="([\s\S]*?)"[\s\S]*?>',
    "red": r'<red>([\s\S]*?)</red>',
    "decode_red": r'<span style="color: red;">([\s\S]*?)</span>',
    "sup": r"<sup>([\s\S]*?)</sup>",
    "sub": r"<sub>([\s\S]*?)</sub>",
    "b": r"<b>([\s\S]*?)</b>",
    "cloze": r"\{\{c(\d+)::([\s\S]*?)(?:::([\s\S]*?))?\}\}", # ["numéro", "champ principal", "champ d'indice" (ou None)]
    "phonetics": r'(?<!\\)//([\s\S]*?)(?<!\\)//'
}

LINE_HEIGHT = 36 # line-height en pixels dans le CSS des cartes
DEFAULT_IMG_HEIGHT = 10 # 10 lignes par défaut donc 10 * 36px
MAX_HEIGHT = 22 # hauteur max d'une carte
