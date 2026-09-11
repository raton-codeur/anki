import define
import re, requests, subprocess, sys
from datetime import datetime

def ankiconnect(action, params = None):
    payload = {
    "action": action,
    "version": define.ANKI_CONNECT_VERSION,
    "params": params or {}
    }
    r = requests.post(define.ANKI_CONNECT_URL, json=payload, timeout=5)
    data = r.json()
    if data["error"] is not None:
        raise RuntimeError(data["error"])
    return data["result"]

def check_anki():
    try:
        a = ankiconnect("version")
        if a != define.ANKI_CONNECT_VERSION :
            sys.exit(f"{define.RED}erreur : mauvaise valeur pour la version d'AnkiConnect{define.RESET}\nversion du add-on : {a}\nANKI_CONNECT_VERSION : {define.ANKI_CONNECT_VERSION}")
    except Exception as e:
        sys.exit(f"{define.RED}erreur : connexion à Anki impossible{define.RESET}\n{e}")

    decks = ankiconnect("deckNames")
    for deck in define.DECK_BASE, define.DECK_TAPER, define.DECK_PAPIER, define.DECK_SONG:
        if deck not in decks:
            print(f"{define.RED}erreur : {deck} : mauvais nom de paquet{define.RESET}\ndecks existants :")
            for d in decks:
                print(f" - {d}")
            sys.exit()

    myModels = define.MODEL_CARD, define.MODEL_REPLACE, define.MODEL_CLOZE, define.MODEL_TAPE, define.MODEL_CLOZE_TAPE
    myFieldss = define.MODEL_CARD_FIELDS, define.MODEL_REPLACE_FIELDS, define.MODEL_CLOZE_FIELDS, define.MODEL_TAPE_FIELDS, define.MODEL_CLOZE_TAPE_FIELDS
    modelsAnki = ankiconnect("modelNames")
    for myModel, myFields in zip(myModels, myFieldss):
        if myModel not in modelsAnki:
            print(f"{define.RED}erreur : {myModel} : mauvais nom de type de note{define.RESET}\ntypes de notes existants :")
            for m in modelsAnki:
                print(f" - {m}")
            sys.exit()
        fieldsAnki = ankiconnect("modelFieldNames", {"modelName": myModel})
        for field in myFields:
            if field not in fieldsAnki:
                print(f"{define.RED}erreur : {field} : mauvais nom de champ dans le type de note \'{myModel}\'{define.RESET}\nchamps existants :")
                for f in fieldsAnki:
                    print(f" - {f}")
                sys.exit()

def print_sections(sections):
    for type, sections_ in sections.items():
        if sections_:
            print(f"  {type} : {sections_}")

def print_count_cards(sections):
    result = {"base": 0, "taper": 0, "papier": 0, "song": 0, "MS": 0}
    result["base"] += len(sections["C1"])
    result["base"] += len(sections["R1"])
    result["taper"] += len(sections["C2"])
    result["papier"] += len(sections["C3"])
    result["papier"] += len(sections["R3"])
    result["song"] += len(sections["SONG"])
    result["MS"] += len(sections["MS"])
    for type, deck in (("Z1", "base"), ("Z2", "taper"), ("Z3", "papier")):
        for section in sections[type]:
            result[deck] += len({m.group(1) for m in re.finditer(define.FORMATS["cloze"], section[0])})

    for type in "base", "taper", "papier", "song", "MS":
        if result[type]:
            print(f"  {type} : {result[type]}")

def open_input_in_vscode():
    subprocess.run(["code", "-g", f"{define.INPUT_PATH}:2"])

def get_card_ids_by_query(query):
    return ankiconnect(
        "findCards",
        {"query": query}
    )

def move_cards_to_trash(card_ids):
    ankiconnect(
        "changeDeck", {
            "cards": card_ids,
            "deck": define.DECK_POUBELLE
        }
    )
