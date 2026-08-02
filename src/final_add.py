import sys, pyperclip
import define
from utils import ankiconnect

def format_for_ankiconnect(section, type):
    # section : une liste de champs encodés.
    # on veut renvoyer une section formatée pour ankiconnect.

    result = define.ANKI_CONNECT_MODELS[type].copy()
    result["fields"] = result["fields"].copy()
    for field_name, value in zip(result["fields"].keys(), section):
        result["fields"][field_name] = value
    return result

def get_final_sections(sections_encoded, sections_raw):
    sections_anki = [] # les sections formatées pour anki connect.
        # exemple avec C1 = [['a', 'b'], ['c', '']]
        # → [{'modelName': 'card', 'deckName': 'base', 'fields': {'front': 'a', 'back': 'b'}},
        # {'modelName': 'card', 'deckName': 'base', 'fields': {'front': 'c', 'back': ''}}]
    sections_anki_raw = [] # les sections brutes correspondantes.
    sections_mosalingua = [] # les sections encodées pour mosalingua.
    sections = {} # toutes les sections, sauf les sections vides.

    for type, sections_ in sections_encoded.items():
        # sections_encoded[type] est une liste de sections du même type.
        # une section est une liste de champs.
        # chaque section de sections_encoded[type] est associée à une section brute dans sections_raw[type].

        sections[type] = []
        for section, section_raw in zip(sections_, sections_raw[type]):
            if all(field == "" for field in section):
                continue
            if type == "MS":
                sections_mosalingua.append(section)
            else:
                sections_anki.append(format_for_ankiconnect(section, type))
                sections_anki_raw.append(section_raw)
            sections[type].append(section)

    return sections_anki, sections_anki_raw, sections_mosalingua, sections

def check_can_add_to_anki(sections_anki, sections_anki_raw):
    can_add = ankiconnect("canAddNotes", {"notes": sections_anki})
    # pour chaque note de sections_anki, on a un booléen indiquant si elle peut être ajoutée.

    for can_add_, section, section_raw in zip(can_add, sections_anki, sections_anki_raw):
        if not can_add_:
            pyperclip.copy(section_raw)
            sys.exit(f"{define.RED}erreur : impossible d'ajouter via anki connect{define.RESET}\n"
                    f"vérifier les doublons ?\nnote : {section}\n"
                    f"section copiée : {define.YELLOW}{section_raw}{define.RESET}")

def add_to_anki(sections) :
    # sections : les sections formatées pour ankiconnect.
    notes_id = ankiconnect("addNotes", {"notes": sections})
    for note_id, section in zip(notes_id, sections):
        if note_id is None:
            print(f"{define.RED}impossible d'ajouter cette note :{define.RESET}\n"
                f"\tnote de type \"{section['modelName']}\", deck \"{section['deckName']}\"\n"
                f"\t{define.YELLOW}{section['fields']}{define.RESET}\n"
                f"à retrouver dans le dernier input traité : {define.TRASH_DIR}/0.txt")

def mosalingua_output(sections):
    # sections : les sections MosaLingua
    with open(define.INPUT_PATH, "a", encoding="utf-8") as f:
        for section in sections:
            for champ in section:
                if champ == "":
                    f.write("<p></p>\n")
                else:
                    f.write(champ + "\n")
            f.write("-\n")
