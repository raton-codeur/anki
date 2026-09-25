import define
from send2trash import send2trash
from utils import ankiconnect

def reset_input():
    with open(define.INPUT_PATH, "w") as f:
        f.write("-\n")

def remove_img_dir():
    if define.IMAGES_SRC_DIR.is_dir():
        for f in define.IMAGES_SRC_DIR.iterdir():
            print(f"image non utilisée envoyée à la corbeille : {f.name}")
        send2trash(define.IMAGES_SRC_DIR)

def reset_anki_trash():
    note_ids = ankiconnect(
        "findNotes",
        {"query": f'deck:"{define.DECK_POUBELLE}"'}
    )
    ankiconnect("deleteNotes", {"notes": note_ids})
