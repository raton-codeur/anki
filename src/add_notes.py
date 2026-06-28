import define
from utils import ankiconnect

def add_to_anki(sections) :
    # sections : les sections formatées pour ankiconnect.
    notes_id = ankiconnect("addNotes", {"notes": sections})
    for note_id, section in zip(notes_id, sections):
        if note_id is None :
            print(f"{define.RED}impossible d'ajouter cette note :{define.RESET}\n"
                f"\tnote de type \"{section['modelName']}\", deck \"{section['deckName']}\"\n"
                f"\t{define.YELLOW}{section['fields']}{define.RESET}\n"
                f"il faut ouvrir le dernier fichier de log.")

def mosalingua_output(sections) :
    # sections : les sections mosalingua
    with open(define.MS_OUTPUT_PATH, "w", encoding="utf-8") as f :
        for section in sections :
            for champ in section :
                if champ == "" :
                    f.write("<p></p>\n")
                else :
                    f.write(champ + "\n")
            f.write("-\n")
