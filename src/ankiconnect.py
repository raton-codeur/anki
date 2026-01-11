import define
import requests

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

def delete_notes_by_query(query) :
		notes_id = ankiconnect("findNotes", {"query": query})
		if notes_id :
				ankiconnect("deleteNotes", {"notes": notes_id})
		print(f"{len(notes_id)} notes supprimées avec anki connect")
