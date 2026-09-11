from utils import check_anki, get_card_ids_by_query, move_cards_to_trash, open_input_in_vscode
import define
from get_utils import get_notes_data, decode_notes
from backup import backup_notes, backup_images
from reset import reset_anki_trash
import sys

check_anki()
if not define.INPUT_PATH.is_file():
    sys.exit(f"{define.RED}erreur : input.txt introuvable{define.RESET}\nINPUT_PATH : {define.INPUT_PATH}")

# le deck est lié aux cartes, pas aux notes.
# (perso, toutes les cartes d'une note sont dans le même deck.)
# donc pour tout ce qui est "récupérer le deck" et "changer de deck",
# on doit utiliser les fonctions liées aux cartes...

selected_card_ids = get_card_ids_by_query("is:buried OR tag:marked")

selected_notes = get_notes_data(selected_card_ids)
# c'est une liste de dictionnaires.
# un dictionnaire a les clés :
# separator : le séparateur à utiliser dans le .txt
# fields : la liste des champs

selected_notes = decode_notes(selected_notes)

backup_notes(selected_notes, define.INPUT_PATH)
backup_images(selected_notes, define.IMAGES_SRC_DIR)
# les notes cibles sont maintenant récupérées dans l'input
# et leurs images ont été copiées dans le dossier source des images

move_cards_to_trash(selected_card_ids)
# les cartes cibles ont été déplacées dans le deck poubelle

trashed_card_ids = get_card_ids_by_query(f'deck:"{define.DECK_POUBELLE}"')
trashed_notes = get_notes_data(trashed_card_ids)
trashed_notes = decode_notes(trashed_notes)
backup_path = define.BACKUPS_TRASH / f"{define.TIMESTAMP}.txt"
backup_notes(trashed_notes, backup_path)
backup_images(trashed_notes, define.BACKUPS_IMAGES)
# les notes du deck poubelle et leurs images ont été archivées

reset_anki_trash()
# les notes du deck poubelle ont été supprimées

print(f"{len(selected_notes)} notes récupérées")
print(f"{len(trashed_notes) - len(selected_notes)} notes supprimées")
if trashed_notes:
    print(f"archive : {backup_path}")

open_input_in_vscode()
