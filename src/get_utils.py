import re, html
import define
from utils import ankiconnect

def get_separator(model, deck):
    """
    aide :
        C2 : DECK_TAPER → "--"
        Z2 : DECK_TAPER → "--"
        R3 : DECK_PAPIER + MODEL_REPLACE → "---r"
        C3 : DECK_PAPIER → "---"
        Z3 : DECK_PAPIER → "---"
        R1 : MODEL_REPLACE → "-r"
        SONG : DECK_SONG → "-song"
        C1 → "-"
        Z1 → "-"
    """
    if deck == define.DECK_TAPER:
        return "--"

    if deck == define.DECK_PAPIER:
        if model == define.MODEL_REPLACE:
            return "---r"
        else:
            return "---"

    if model == define.MODEL_REPLACE:
        return "-r"

    if deck == define.DECK_SONG:
        return "-song"

    return "-"

def get_fields(card):
    # card["fields"] contient les champs de la note.
    # c'est un dictionnaire dont les clés sont les noms des champs.
    # une valeur de ce dictionnaire contient donc un champ.
    # cette valeur est elle-même un dictionnaire dont les clés sont "value" (c'est ce qu'on veut)
    # et "order" (qui donne la position du champ).
    # donc on trie card["fields"].values() par ordre croissant sur "order",
    # et on renvoie la liste des "value" dans cet ordre
    return [
        field["value"]
        for field in sorted(
            card["fields"].values(),
            key=lambda f: f["order"]
        )
    ]

def get_notes_data(card_ids):
    """renvoie une liste des notes :
        chaque note est un dictionnaire avec les clés :
            separator : le séparateur qu'il faudra écrire dans le .txt
            fields : la liste des champs de la note (qu'il faudra décoder)."""

    cards = ankiconnect(
        "cardsInfo",
        {"cards": card_ids}
    )

    note_ids = set() # pour aller de note en note
    result = []
    for card in cards:
        if card["note"] in note_ids:
            continue
        note_ids.add(card["note"])
        result.append({
            "separator": get_separator(card["modelName"], card["deckName"]),
            "fields": get_fields(card),
        })
    return result

def decode(s):
    """s : un champ récupéré d'anki.

    renvoie s décodé."""

    s = (
        s.replace("&nbsp;&nbsp;&nbsp;&nbsp;", "\t")
         .replace("&nbsp;", " ")
         .replace("<br>", "\n")
         .replace("<br />", "\n")
         .replace("<div>", "")
         .replace("</div>", "")
    )
    s = html.unescape(s) # par exemple, "&lt;" → "<"
    s = s.replace("@", r"\@") # après le unescape, si jamais unescape fait apparaître un "@"
    s = re.sub(define.FORMATS["decode_img"], r"<img h=10\n\1>", s)
    s = re.sub(define.FORMATS["decode_red"], r"<red>\1</red>", s)
    s = re.sub(define.FORMATS["decode_link"], r"<link:\1>", s)
    return s

def decode_notes(notes):
    for note in notes:
        note["fields"] = [decode(field) for field in note["fields"]]
    return notes
