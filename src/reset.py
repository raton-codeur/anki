import define
from send2trash import send2trash
from utils import ankiconnect

def reset_input():
    with open(define.INPUT_PATH, "w") as f:
        f.write("-\n")

def reset_img_dir():
    if not define.IMAGES_SRC_DIR.exists():
        return
    for f in define.IMAGES_SRC_DIR.iterdir():
        send2trash(f)
    print(f"{define.IMAGES_SRC_DIR} a été vidé")

def reset_anki_trash():
    note_ids = ankiconnect(
        "findNotes",
        {"query": f'deck:"{define.DECK_POUBELLE}"'}
    )
    ankiconnect("deleteNotes", {"notes": note_ids})
