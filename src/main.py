import define
from check_param import check_param
from check_input import check_top, check_angle_brackets, check_MS, check_Z, check_and_move_images, check_fields
from section_transform import first_split, trim_lines, split_fields, remove_empty_sections
from encode import encode
from utils import print_sections, print_count_cards, delete_notes_by_query, update_logs, reset_input_file
from output import mosalingua_output, ankiconnect_format, add_anki_notes
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

# fin des vérifications.
# on a plus besoin de sections_raw

sections = remove_empty_sections(sections_fields)

sections = encode(sections)

print("sections :")
print_sections(sections)
print("count :")
print_count_cards(sections)

ms_sections = sections.pop("MS")
if ms_sections :
    mosalingua_output(ms_sections)

anki_sections = ankiconnect_format(sections)
# les cartes sont maintenant formattées pour anki connect.
# exemple avec C1 = [['a', 'b'], ['c', '']]
# → [{'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'a', 'back': 'b'}},
# {'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'c', 'back': ''}}]
add_anki_notes(anki_sections)

# update_logs()

# reset_input_file()

# # ouverture de l'output de mosalingua
# if ms_sections :
#     subprocess.run(["code", define.MS_OUTPUT_PATH])


# # from zipfile import ZipFile

# # with ZipFile("test.apkg") as z:
# #     z.extractall("deck")

# # import sqlite3

# # conn = sqlite3.connect("deck/collection.anki2")
# # cursor = conn.cursor()

# # cursor.execute("SELECT mid, flds FROM notes")

# # for (mid, fields) in cursor.fetchall():
# #     fields = fields.split("\x1f")
# #     print(f"Model ID: {mid}")
# #     print(f"Fields: {fields}")
# #     print()