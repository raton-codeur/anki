import define
from check_input import check_top, check_angle_brackets, check_MS, check_Z, check_and_move_images, check_fields
from section_transform import first_split, trim_lines, split_fields
from encode import encode
from final_add import get_final_sections, check_can_add_to_anki, add_to_anki, mosalingua_output
from utils import update_input_trash, reset_input_file, reset_img_dir, print_sections, print_count_cards

def add():
    # ouvrir, retirer les white spaces de début et fin, split lines
    with open(define.INPUT_PATH, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()

    check_top(lines)
    sections_raw = first_split(lines)
    # sections_raw est un dictionnaire avec
        # clés : "C1", "C2", "C3", "Z1", "Z2", "Z3", "R1", "R3", "MS"
        # une valeur : la liste des sections brutes correspondantes
    # les sections ne sont pas encore divisées en champs.

    check_angle_brackets(sections_raw)
    check_MS(sections_raw["MS"])
    check_Z(sections_raw)
    check_and_move_images(sections_raw)

    sections_raw_trim = trim_lines(sections_raw)
    # les lignes de sections_raw_trim sont soft-trimées à gauche et hard-trimées à droite
        # soft trimer → strip(" ")
        # hard trimer → strip(" \t")
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
        # → [{'modelName': 'card', 'deckName': 'base', 'fields': {'front': 'a', 'back': 'b'}},
        # {'modelName': 'card', 'deckName': 'base', 'fields': {'front': 'c', 'back': ''}}]
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
