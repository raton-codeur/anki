import define
import shutil, re
from send2trash import send2trash

def backup_input():
    # on veut maintenir une archive de (maximum) 10 inputs.
    # si le dossier existe pas, il est créé.
    # si on dépasse 10, on veut mettre à la corbeille le plus ancien.

    define.BACKUPS_INPUT.mkdir(parents=True, exist_ok=True)
    backup_path = define.BACKUPS_INPUT / f"{define.TIMESTAMP}.txt"
    shutil.copy2(define.INPUT_PATH, backup_path)
    print(f"archive créée : {backup_path}")

    files = sorted(define.BACKUPS_INPUT.iterdir())
    if (len(files) > 10):
        send2trash(files[0])

def backup_notes(notes, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [] # ce qu'on va écrire dans le fichier
    for note in notes :
        data.append(note["separator"])
        fields = note["fields"]
        while fields and not fields[-1]:
            fields.pop()
        data.append("\n@\n".join(fields))
    with open(path, "a") as f:
        f.write("\n".join(data))

def backup_images(notes, path_dir):
    path_dir.mkdir(parents=True, exist_ok=True)
    for note in notes:
        for field in note["fields"]:
            for _, name in re.findall(define.FORMATS["img"], field) :
                src = define.IMAGES_DST_DIR / name
                dst = path_dir / name
                if src.is_file():
                    shutil.copy2(src, dst)
                else:
                    print(
                        f'backup_images: {define.RED}image manquante'
                        f'{define.RESET}: "{name}"'
                    )
