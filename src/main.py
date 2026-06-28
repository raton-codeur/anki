import define
from check_param import check_param
from check_input import check_top, check_angle_brackets, check_MS, check_Z, check_and_move_images, check_fields, check_can_add_to_anki
from section_transform import first_split, trim_lines, split_fields
from encode import encode
from utils import print_sections, print_count_cards, update_logs, reset_input_file, format_for_ankiconnect
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

# il faut :
#   - vérifier que les sections_encoded peuvent être ajoutées à anki sans erreur (notamment : pas de problème de doublon).
#   - garder une correspondance entre les sections pour anki et les sections brutes.
#   - séparer les sections pour mosalingua et les sections pour anki.

sections_anki = [] # les sections formatées pour anki connect.
    # exemple avec C1 = [['a', 'b'], ['c', '']]
    # → [{'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'a', 'back': 'b'}},
    # {'modelName': 'card', 'deckName': '1 - basic', 'fields': {'front': 'c', 'back': ''}}]
sections_anki_raw = [] # les sections brutes correspondantes.
sections_mosalingua = [] # les sections encodées pour mosalingua.
sections = {} # toutes les sections, sauf les sections vides.

for type, sections_ in sections_encoded.items() :
    # sections = sections_encoded[type], c'est une liste de sections du même type.
    # une section est une liste de champs.
    # chaque section de sections_encoded[type] est associée à une section brute dans sections_raw[type].

    sections[type] = [] # à remplir
    for section, section_raw in zip(sections_, sections_raw[type]) :
        if all(field == "" for field in section):
            continue
        if type == "MS" :
            sections_mosalingua.append(section_raw)
        else :
            sections_anki.append(format_for_ankiconnect(section, type))
            sections_anki_raw.append(section_raw)
        sections[type].append(section)

# sections_anki, sections_anki_raw, sections_mosalingua et sections sont prêts.

check_can_add_to_anki(sections_anki, sections_anki_raw)

# add_to_anki(sections_anki)
# if sections_mosalingua :
#     mosalingua_output(sections_mosalingua)
# les notes sont maintenant ajoutées à anki et les sections MS sont formatées dans un fichier.

print("sections :")
print_sections(sections)
print("count :")
print_count_cards(sections)

# update_logs()

# reset_input_file()

# # ouverture de l'output de mosalingua
# if ms_sections :
#     subprocess.run(["code", define.MS_OUTPUT_PATH])
