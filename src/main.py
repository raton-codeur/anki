import define
from check_param import check_param
from check_input import check_top, check_angle_brackets, check_MS, check_Z, check_and_move_images, check_fields
from section_transform import first_split, trim_lines, split_fields
from encode import encode
from final_add import get_final_sections, check_can_add_to_anki, add_to_anki, mosalingua_output
from utils import (
    print_sections,
    print_count_cards,
    update_input_trash,
    reset_input_file,
    reset_img_dir,
    get_trashed_cards,
    update_anki_trash,
    open_input_in_vscode
)
from handle_marked import get_marked_cards, decode_notes, get_back_images, backfill_input, move_marked_cards

check_param()

# ouvrir, retirer les white spaces de début et fin, split lines
with open(define.INPUT_PATH, "r", encoding="utf-8") as f:
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

sections_anki, sections_anki_raw, sections_mosalingua, sections = get_final_sections(sections_encoded, sections_raw)
# sections_anki : les sections formatées pour anki connect.
    # exemple avec C1 = [['a', 'b'], ['c', '']]
    # → [{'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'a', 'back': 'b'}},
    # {'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'c', 'back': ''}}]
# sections_anki_raw : les sections brutes correspondantes.
# sections_mosalingua : les sections encodées pour mosalingua.
# sections : toutes les sections, sauf les sections vides.

check_can_add_to_anki(sections_anki, sections_anki_raw)
add_to_anki(sections_anki)
# les notes sont maintenant ajoutées à anki.

update_input_trash()
reset_input_file()
reset_img_dir()
# l'input a été archivée dans la corbeille et remise à 0.
# le dossier des images a été vidé.

mosalingua_output(sections_mosalingua)
# les sections MS sont maintenant formatées dans l'input.

if (any(sections.values())):
    print("ajouté :")
    # print_sections(sections)
    print_count_cards(sections)

marked_card_ids, marked_note_ids, marked_notes = get_marked_cards()
# marked_notes est une liste de dictionnaires des cartes marquées sur Anki
# dont les clés sont : separator, fields
if marked_notes:
    print(f"{len(marked_notes)} notes récupérées")

    marked_notes = decode_notes(marked_notes)
    # les notes marquées sont maintenant décodées.

    get_back_images(marked_notes)
    # on a récupéré les images des cartes marquées.

    backfill_input(marked_notes)
    # on a récupéré les cartes marquées dans l'input.

    move_marked_cards(marked_card_ids)

trashed_note_ids = get_trashed_cards()
if trashed_note_ids:
    print(f"{len(trashed_note_ids)} notes retirées d'Anki")

    update_anki_trash(trashed_note_ids)
    # la poubelle d'Anki a été vidée.

open_input_in_vscode()
