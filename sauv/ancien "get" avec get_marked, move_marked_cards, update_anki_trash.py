
marked_card_ids, marked_notes = get_marked()
# marked_notes : la liste des notes marquées :
    # chaque note est un dictionnaire avec les clés :
        # separator : le séparateur qu'il faudra écrire dans l'input
        # fields : la liste des champs de la note (qu'il faut décoder).

marked_notes = decode_notes(marked_notes)
# les notes marquées sont maintenant décodées.

get_notes_back(marked_notes)
print(f"{len(marked_notes)} notes récupérées dans l'input")

get_images_back(marked_notes)
# on a récupéré les images des cartes marquées.

move_marked_cards(marked_card_ids)
# les cartes marquées sont maintenant toutes dans le deck poubelle

trashed_note_ids = get_trashed_cards()
if trashed_note_ids:
    print(f"{len(trashed_note_ids)} notes retirées d'Anki")

    update_anki_trash(trashed_note_ids)
    # la poubelle d'Anki a été vidée.

def get_marked():
    """renvoie la liste des ids des cartes marquées
    et une liste des notes marquées :
        chaque note est un dictionnaire avec les clés :
            separator : le séparateur qu'il faudra écrire dans l'input
            fields : la liste des champs de la note (qu'il faudra décoder)."""

    card_ids = ankiconnect(
        "findCards",
        {"query": "tag:marked"}
    )

    cards = ankiconnect(
        "cardsInfo",
        {"cards": card_ids}
    )

    note_ids = set() # juste pour aller de note en note
    notes = []
    for card in cards:
        if card["note"] in note_ids:
            continue
        note_ids.add(card["note"])
        notes.append({
            "separator": define.GET_SEPARATOR.get((card["modelName"], card["deckName"]), "-"),
            "fields": [
                field["value"]
                for field in sorted(
                    card["fields"].values(),
                    key=lambda f: f["order"]
                )
            ]
        })
    return card_ids, notes

def decode(s):
    """s : un champ récupéré d'anki.

    renvoie s décodé."""
    s = s.replace("&nbsp;&nbsp;&nbsp;&nbsp;", '\t')
    s = s.replace("&nbsp;", ' ')
    s = s.replace("<br>", '\n')
    s = s.replace("<br />", '\n')
    s = s.replace("&lt;", "<").replace("&gt;", ">")
    s = s.replace("<div>", "").replace("</div>", "")
    s = s.replace("@", r"\@")
    s = re.sub(define.FORMATS["decode_img"], r"<img h=10\n\1>", s)
    s = re.sub(define.FORMATS["decode_red"], r"<red>\1</red>", s)
    s = re.sub(define.FORMATS["decode_link"], r"<link:\1>", s)
    return s

def decode_notes(notes):
    for note in notes:
        note["fields"] = [decode(field) for field in note["fields"]]
    return notes

def backup_notes(notes):
    data = [] # ce qu'on va écrire dans le fichier
    for note in notes :
        data.append(note["separator"])
        fields = list(note["fields"])
        while fields and not fields[-1]:
            fields.pop()
        data.append("\n@\n".join(fields))

    with open(define.INPUT_PATH, "a") as f:
        f.write("\n\n")
        f.write("\n".join(data))

def get_images_back(notes):
    """copier les images référencées dans les cartes marquées
    du dossier images d'Anki au dossier source des images du script."""
    for note in notes:
        for field in note["fields"]:
            for _, name in re.findall(define.FORMATS["img"], field) :
                path_dst = define.IMAGES_DST_DIR / name
                path_src = define.IMAGES_SRC_DIR / name
                if path_dst.exists():
                    path_src.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path_dst, path_src)
                else:
                    print(f"get_images_back: image à récupérer manquante: {path_dst}")

def move_marked_cards(card_ids):
    ankiconnect("changeDeck", {
            "cards": card_ids,
            "deck": define.DECK_POUBELLE
        }
    )


def get_trashed_cards():
    return ankiconnect("findNotes",
        {"query": f'deck:"{define.DECK_POUBELLE}"'}
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
        "deck": define.DECK_POUBELLE,
        "path": os.path.join(define.TRASH_DIR, "0.apkg")
    })

    ankiconnect("deleteNotes",
        {"notes": note_ids}
    )
