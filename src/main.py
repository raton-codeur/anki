from utils import ankiconnect
import define
from check_param import check_param
from check_input import check_top, check_angle_brackets, check_MS, check_Z, check_and_move_images, check_fields
from section_transform import first_split, trim_lines, split_fields
from encode import encode
from final import get_final, check_can_add_to_anki
from utils import print_sections, print_count_cards, update_input_trash, reset_input_file, update_anki_trash
from add_notes import add_to_anki, mosalingua_output
import subprocess

check_param()

# ouvrir, retirer les white spaces de début et fin, split lines
with open(define.INPUT_PATH, "r", encoding="utf-8") as f :
    lines = f.read().strip().splitlines()

check_top(lines)
sections_raw = first_split(lines)
# sections_raw est un dictionnaire avec
    # clés : "C1", "C2", "C3", "Z1", "Z2", "Z3", "R1", "R3", "MS"
    # une valeur : la liste des sections brutes correspondantes

# les sections ne sont pas divisées en champs

check_angle_brackets(sections_raw)
check_MS(sections_raw["MS"])
check_Z(sections_raw)
check_and_move_images(sections_raw)

sections_raw_trim = trim_lines(sections_raw)
# les lignes de sections_raw_trim sont soft-trimées à gauche et hard-trimées à droite
sections_fields = split_fields(sections_raw_trim)
# une section de sections_raw est maintenant appairée dans sections_fields
# avec la liste de ses champs bien trimés
# par exemple :
#     # sections_raw["C1"] = [" a@\n\tb\t ", "\n\n blabla ", ...]
#     # sections_fields["C1"] = [["a", "\tb"], ["blabla", ""], ...]

check_fields(sections_fields, sections_raw)

sections_encoded = encode(sections_fields)
# les sections sont maintenant encodées et toujours appairées avec sections_raw.

sections_anki, sections_anki_raw, sections_mosalingua, sections = get_final(sections_encoded, sections_raw)
# sections_anki : les sections formatées pour anki connect.
    # exemple avec C1 = [['a', 'b'], ['c', '']]
    # → [{'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'a', 'back': 'b'}},
    # {'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'c', 'back': ''}}]
# sections_anki_raw : les sections brutes correspondantes.
# sections_mosalingua : les sections encodées pour mosalingua.
# sections : toutes les sections, sauf les sections vides.

# check_can_add_to_anki(sections_anki, sections_anki_raw)

update_input_trash()
reset_input_file()

add_to_anki(sections_anki)
mosalingua_output(sections_mosalingua)
# les notes sont maintenant ajoutées à anki et les sections MS sont formatées dans un fichier.

print("ajouté :")
# print_sections(sections)
print_count_cards(sections)

marked_cards_ids = ankiconnect(
    "findCards",
    {"query": "tag:marked"}
)

def get_separator(model, deck):
    if deck in (define.DECK_1, define.DECK_2, define.DECK_3):
        return define.GET_SEPARATOR[(model, deck)]
    elif model == define.MODEL_TAPE or model == define.MODEL_CLOZE_TAPE:
        return "--"
    else:
        return define.GET_SEPARATOR[(model, define.DECK_1)]

def get_marked(marked_cards_ids):
    cards = ankiconnect(
        "cardsInfo",
        {"cards": marked_cards_ids}
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
    return list(note_ids), notes
marked_notes_ids, marked_notes = get_marked(marked_cards_ids)
# marked_notes est une liste de dictionnaires
# dont les clés sont : separator, fields

import re
def decode(s):
    s = s.replace("&nbsp;&nbsp;&nbsp;&nbsp;", '\t')
    s = s.replace("&nbsp;", ' ')
    s = s.replace("<br>", '\n')
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("@", r"\@")
    s = re.sub(define.FORMATS["decode_img"], r"<img>\1</img>", s)
    s = re.sub(define.FORMATS["decode_red"], r"<red>\1</red>", s)
    return s

def decode_notes(notes):
    for note in notes:
        note["fields"] = [decode(field) for field in note["fields"]]
    return notes

marked_notes = decode_notes(marked_notes)

import shutil, os
def move_imgs(notes):
    for note in notes:
        for field in note["fields"]:
            images = re.findall(define.FORMATS["img"], field)
            for height, name in images :
                name_dst = os.path.join(define.IMAGES_DST_DIR, name)
                name_src = os.path.join(define.IMAGES_SRC_DIR, name)
                shutil.move(name_dst, name_src)

move_imgs(marked_notes)

output = []
for note in marked_notes :
    output.append(note["separator"])
    output.append("\n@\n".join(note["fields"]))

with open(define.INPUT_PATH, "a") as f:
    f.write("\n".join(output))

if marked_notes:
    ankiconnect("changeDeck", {
            "cards": marked_cards_ids,
            "deck": define.TRASH_DECK
        }
    )
    print(f"{len(marked_notes)} notes récupérées")

update_anki_trash()

subprocess.run(["code", "-g", f"{define.INPUT_PATH}:2"])
