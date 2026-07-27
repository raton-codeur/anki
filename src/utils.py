import define
import re, requests, send2trash, shutil, os, subprocess

def ankiconnect(action, params = None):
    payload = {
    "action": action,
    "version": define.ANKI_CONNECT_VERSION,
    "params": params or {}
    }
    r = requests.post(define.ANKI_CONNECT_URL, json=payload, timeout=5)
    data = r.json()
    if data["error"] is not None:
        raise RuntimeError(data["error"])
    return data["result"]

def print_sections(sections):
    for type, sections_ in sections.items():
        if sections_:
            print(f"  {type} : {sections_}")

def print_count_cards(sections):
    result = {"1": 0, "2": 0, "3": 0, "MS": 0}
    result["1"] += len(sections["C1"])
    result["1"] += len(sections["R1"])
    result["2"] += len(sections["C2"])
    result["3"] += len(sections["C3"])
    result["3"] += len(sections["R3"])
    result["MS"] += len(sections["MS"])
    for type, deck in (("Z1", "1"), ("Z2", "2"), ("Z3", "3")):
        for section in sections[type]:
            result[deck] += len({m.group(1) for m in re.finditer(define.FORMATS["cloze"], section[0])})

    for type in "1", "2", "3":
        print(f"  {type} : {result[type]}")
    if result["MS"] > 0:
        print(f"  MS : {result['MS']}")

def update_input_trash():
    # on veut maintenir une archive des 10 derniers inputs traités.
    # le dernier input traité porte le numéro 0, puis 1,
    # ainsi de suite jusqu'à 9.

    # on veut mettre à la corbeille (la vraie)
    # l'ancien numéro 9.

    trash_9_path = os.path.join(define.TRASH_DIR, "9.txt")
    if os.path.exists(trash_9_path):
        send2trash.send2trash(trash_9_path)
    for i in range(8, -1, -1):
        a = os.path.join(define.TRASH_DIR, f"{i}.txt")
        b = os.path.join(define.TRASH_DIR, f"{i + 1}.txt")
        if os.path.exists(a):
            os.rename(a, b)
    shutil.copy(define.INPUT_PATH, os.path.join(define.TRASH_DIR, "0.txt"))

def reset_input_file():
    with open(define.INPUT_PATH, "w") as f:
        f.write("-\n")

def reset_img_dir():
    # tous les fichiers non utilisés du dossier des images
    # sont envoyés à la corbeille (la vraie).
    for f in os.listdir(define.IMAGES_SRC_DIR):
        send2trash.send2trash(os.path.join(define.IMAGES_SRC_DIR, f))

def get_trashed_cards():
    return ankiconnect("findNotes",
        {"query": f'deck:"{define.TRASH_DECK}"'}
    )

def update_anki_trash(note_ids):
    # on veut vider la corbeille d'anki
    # et maintenir une archive des 10 dernières corbeilles vidées.
    # la dernière corbeille vidée porte le numéro 0, puis 1,
    # ainsi de suite jusqu'à 9.

    # on veut mettre à la corbeille (la vraie)
    # l'ancien numéro 9.

    trash_9_path = os.path.join(define.TRASH_DIR, "9.apkg")
    if os.path.exists(trash_9_path):
        send2trash.send2trash(trash_9_path)
    for i in range(8, -1, -1):
        a = os.path.join(define.TRASH_DIR, f"{i}.apkg")
        b = os.path.join(define.TRASH_DIR, f"{i + 1}.apkg")
        if os.path.exists(a):
            os.rename(a, b)

    ankiconnect("exportPackage", {
        "deck": define.TRASH_DECK,
        "path": os.path.join(define.TRASH_DIR, "0.apkg")
    })

    ankiconnect("deleteNotes",
        {"notes": note_ids}
    )

def open_input_in_vscode():
    subprocess.run(["code", "-g", f"{define.INPUT_PATH}:2"])
