import re, shutil, os
import define
from utils import ankiconnect

def get_separator(model, deck):
    if deck in (define.DECK_BASE, define.DECK_TAPER, define.DECK_PAPIER, define.DECK_SONG):
        return define.GET_SEPARATOR[(model, deck)]
    elif model == define.MODEL_TAPE or model == define.MODEL_CLOZE_TAPE:
        return "--"
    else:
        return define.GET_SEPARATOR.get((model, define.DECK_BASE), "-")

def get_marked():
    card_ids = ankiconnect(
        "findCards",
        {"query": "tag:marked"}
    )

    cards = ankiconnect(
        "cardsInfo",
        {"cards": card_ids}
    )

    note_ids = set()
    notes = []
    for card in cards:
        if card["note"] in note_ids:
            continue
        note_ids.add(card["note"])
        notes.append({
            "separator": get_separator(card["modelName"], card["deckName"]),
            "fields": [
                field["value"]
                for field in sorted(
                    card["fields"].values(),
                    key=lambda f: f["order"]
                )
            ]
        })
    return card_ids, notes

def decode(s):
    """s : un champ récupéré d'anki.

    renvoie s décodé."""
    s = s.replace("&nbsp;&nbsp;&nbsp;&nbsp;", '\t')
    s = s.replace("&nbsp;", ' ')
    s = s.replace("<br>", '\n')
    s = s.replace("&lt;", "<").replace("&gt;", ">")
    s = s.replace("@", r"\@")
    s = re.sub(define.FORMATS["decode_img"], r"<img h=10\n\1>", s)
    s = re.sub(define.FORMATS["decode_red"], r"<red>\1</red>", s)
    s = re.sub(define.FORMATS["decode_link"], r"<link:\1>", s)
    return s

def decode_notes(notes):
    for note in notes:
        note["fields"] = [decode(field) for field in note["fields"]]
    return notes

def get_back_images(notes):
    """déplace les images référencées dans les cartes marquées
    du dossier images d'Anki au dossier source des images du script."""
    for note in notes:
        for field in note["fields"]:
            for _, name in re.findall(define.FORMATS["img"], field) :
                name_dst = os.path.join(define.IMAGES_DST_DIR, name)
                name_src = os.path.join(define.IMAGES_SRC_DIR, name)
                shutil.move(name_dst, name_src)

def backfill_input(notes):
    data = [] # ce qu'on va écrire dans le fichier
    for note in notes :
        data.append(note["separator"])
        data.append("\n@\n".join(note["fields"]))

    with open(define.INPUT_PATH, "a") as f:
        f.write("\n\n")
        f.write("\n".join(data))

def move_marked_cards(card_ids):
    ankiconnect("changeDeck", {
            "cards": card_ids,
            "deck": define.DECK_POUBELLE
        }
    )
