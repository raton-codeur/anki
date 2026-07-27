from check_param import check_param
from check_input import *
import define
from section_transform import *
from encode import *
from print import *
from output import *
from ankiconnect import *
import subprocess
import send2trash

check_param()

# ouvrir, retirer les white spaces de début et fin, split lines
with open(define.INPUT_PATH, "r", encoding="utf-8") as f :
	lines = f.read().strip().splitlines()

check_top(lines)
sections_raw = first_split(lines)
# sections_raw est un dictionnaire avec
	# clés : "C1", "C2", "C3", "Z1", "Z2", "Z3", "MS"
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
# avec la liste de ses champs soft-trimés

# les lignes sont aussi soft-trimées à gauche et hard-trimées à droite dans sections_fields

	# par exemple :
		# sections_raw["C1"] = [" a@\n\tb ", "blabla", ...]
		# sections_fields["C1"] = [["a", "\tb"], ["blabla", ""], ...]

check_fields(sections_fields, sections_raw)

# fin des vérifications
	# on a plus besoin de sections_raw

sections = remove_empty_sections(sections_fields)

sections = encode(sections)

# print("sections :")
# print_sections(sections)
# print("count :")
print_count_cards(sections)

ms_sections = sections.pop("MS")
anki_sections = ankiconnect_format(sections)

mosalingua_output(ms_sections)
add_anki_notes(anki_sections)

# mise à jour des logs
log_9_path = os.path.join(define.LOG_DIR, "9.txt")
if os.path.exists(log_9_path) :
    send2trash.send2trash(log_9_path)
for i in range(8, -1, -1) :
    a = os.path.join(define.LOG_DIR, f"{i}.txt")
    b = os.path.join(define.LOG_DIR, f"{i + 1}.txt")
    if os.path.exists(a) :
        os.rename(a, b)
shutil.copy(define.INPUT_PATH, os.path.join(define.LOG_DIR, "0.txt"))

# mise à jour du sas
with open(define.INPUT_PATH, "w") as f :
  f.write("-" + "\n" * 20)

# ouverture de l'output de mosalingua
if ms_sections :
	subprocess.run(["code", "-r", define.MS_OUTPUT_PATH])

# delete_notes_by_query("ankitest")
