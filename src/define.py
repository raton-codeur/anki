RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

INPUT_PATH = '/Users/quentinhauuy/Documents/anki/input.txt'

IMAGES_SRC_DIR = "/Users/quentinhauuy/Downloads"
IMAGES_DST_DIR = "/Users/quentinhauuy/Library/Application Support/Anki2/Quentin/collection.media"

LOG_DIR = "/Users/quentinhauuy/Documents/anki/log"

MS_OUTPUT_PATH = "/Users/quentinhauuy/Documents/anki/mosalingua_output.txt"

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
ANKI_CONNECT_VERSION = 6

DECK_1 = "1 - basic"
DECK_2 = "2 - type-in"
DECK_3 = "3 - write-out"

TYPE_1 = "1 - card"
FIELDS_TYPE_1 = ["front", "back"]

TYPE_2 = "2 - type-in card"
FIELDS_TYPE_2 = ["front", "back", "extra"]

TYPE_3 = "3 - cloze"
FIELDS_TYPE_3 = ["text", "extra"]

TYPE_4 = "4 - type-in cloze"
FIELDS_TYPE_4 = ["text", "extra"]

FIELDS_MS = ["english", "extra english", "french", "extra french"]

NB_FIELDS = {
	"C1": 2,
	"C2": 3,
	"C3": 2,
	"Z1": 2,
	"Z2": 2,
	"Z3": 2,
	"MS": 4
}

ANKI_CONNECT_MODELS = {
	"C1" : {
		"modelName": TYPE_1,
		"deckName": DECK_1,
		"fields": dict.fromkeys(FIELDS_TYPE_1, "")
	},
	"C2" : {
		"modelName": TYPE_2,
		"deckName": DECK_2,
		"fields": dict.fromkeys(FIELDS_TYPE_2, "")
	},
	"C3" : {
		"modelName": TYPE_1,
		"deckName": DECK_3,
		"fields": dict.fromkeys(FIELDS_TYPE_1, "")
	},
	"Z1" : {
		"modelName": TYPE_3,
		"deckName": DECK_1,
		"fields": dict.fromkeys(FIELDS_TYPE_3, ""),
	},
	"Z2" : {
		"modelName": TYPE_4,
		"deckName": DECK_2,
		"fields": dict.fromkeys(FIELDS_TYPE_4, "")
	},
	"Z3" : {
		"modelName": TYPE_3,
		"deckName": DECK_3,
		"fields": dict.fromkeys(FIELDS_TYPE_3, "")
	}
}

SEPARATORS = '-', '--', '---', '-)'

# nom d'un format -> regex
FORMATS = {
    "img": r'<img src="([\s\S]*?)">',
    "red": r'<span style="color:red;">([\s\S]*?)</span>',
    "sup": r"<sup>([\s\S]*?)</sup>",
    "sub": r"<sub>([\s\S]*?)</sub>",
    "b": r"<b>([\s\S]*?)</b>",
    "cloze" : r"\{\{c\d+::([\s\S]*?)(?:::([\s\S]*?))?\}\}", # ["champ principal", "champ d'indice"]
    "extended_cloze" : r"\{\{c(\d+)::([\s\S]*?)(::([\s\S]*?))?\}\}", # ["numéro", "champ principal", "vide si pas d'indice", "champ d'indice"]
    "phonetics" : r'(?<!\\)//([\s\S]*?)(?<!\\)//'
}
