import define
import requests

ankiNotes = []
msNotes = []

def ankiconnect(action, params = None) :
	payload = {
	"action": action,
	"version": define.ANKI_CONNECT_VERSION,
	"params": params or {}
	}
	r = requests.post(define.ANKI_CONNECT_URL, json=payload, timeout=5)
	data = r.json()
	if data["error"] is not None :
		raise RuntimeError(data["error"])
	return data["result"]

def newNote(sectionType) :
	if sectionType == define.MS :
		result = dict.fromkeys(define.MS, "<p></p>")
		msNotes.append(result)
		return result
	else :
		result = {
			"deckName": sectionType["deckName"],
			"modelName": sectionType["modelName"],
			"fields": dict.fromkeys(sectionType["fieldsName"], "")
		}
		ankiNotes.append(result)
		return result["fields"]

def addNotes(notes) :
	if all(ankiconnect("canAddNotes", {"notes": notes})) :
		print("pas de doublon")
	else :
		print("doublon detecté")
	notes_id = ankiconnect("addNotes", {"notes": notes})
	print(f"{len(notes_id)} notes added")

def deleteNotesByQuery(query) :
		notes_id = ankiconnect("findNotes", {"query": query})
		if notes_id :
				ankiconnect("deleteNotes", {"notes": notes_id})
		print(f"{len(notes_id)} notes deleted")
