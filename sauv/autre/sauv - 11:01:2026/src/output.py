import define
from ankiconnect import ankiconnect

def mosalingua_output(sections) :
	# sections : les sections mosalingua

	if not sections :
		return

	with open(define.MS_OUTPUT_PATH, "w", encoding="utf-8") as f :
		f.write("-\n")
		for section in sections :
			for champ in section :
				if champ == "" :
					f.write("<p></p>\n")
				else :
					f.write(champ + "\n")
			f.write("-\n")

def ankiconnect_format(sections) :
	result = []
	for type, sections_ in sections.items() :
		for section in sections_ :
			new_section = define.ANKI_CONNECT_MODELS[type].copy()
			new_section["fields"] = new_section["fields"].copy()
			for field_name, value in zip(new_section["fields"].keys(), section) :
				new_section["fields"][field_name] = value
			result.append(new_section)
	return result

def add_anki_notes(sections) :
	note_ids = ankiconnect("addNotes", {"notes": sections})
	for i, note_id in enumerate(note_ids) :
		if note_id is None :
			print(f"{define.RED}impossible d'ajouter cette note :{define.RESET}\n"
				f"\tnote de type \"{sections[i]['modelName']}\", deck \"{sections[i]['deckName']}\"\n"
				f"\t{define.YELLOW}{sections[i]['fields']}{define.RESET}")
	print(f"{len(note_ids) - note_ids.count(None)} notes ajoutées avec anki connect")
