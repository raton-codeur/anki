import define
from anki_connect import *

note = newNote(define.C1)
note["front"] = "  \"mytests type C1"
note["back"] = "type C1 back"

note = newNote(define.C2)
note["front"] = "mytest type C2"
note["back"] = "type C2 back"
note["extra"] = "type C2 extra"

note = newNote(define.C3)
note["front"] = "mytest type C3"
note["back"] = "type C3 back"

note = newNote(define.Z1)
note["text"] = "mytest type Z1 {{c1::type Z1 réponse}}"
note["extra"] = "type Z1 extra"

note = newNote(define.Z2)
note["text"] = "mytest type Z2 {{c1::type Z2 réponse}}"
note["extra"] = "type Z2 extra"

note = newNote(define.Z3)
note["text"] = "mytest type Z3 {{c1::type Z3 réponse}}"
note["extra"] = "type Z3 extra"

note = newNote(define.MS)
note["english"] = "mytest MS English"
note["extra english"] = "mytest MS Extra English"
note["french"] = "mytest MS French"
note["extra french"] = "mytest MS Extra French"

# for note in ankiNotes :
# 	for clé, valeur in note.items() :
# 		print(f"{clé} : {valeur}")
# for note in msNotes :
# 	for clé, valeur in note.items() :
# 		print(f"{clé} : {valeur}")

# addNotes(ankiNotes)

# ankiconnect("guiBrowse", {"query": "mytest"})

# deleteNotesByQuery("mytest")
