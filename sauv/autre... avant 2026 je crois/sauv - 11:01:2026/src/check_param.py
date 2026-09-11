import os, requests
import define
from ankiconnect import ankiconnect

def check_param() :
	if not os.path.isfile(define.INPUT_PATH) :
			exit(f"{define.RED}erreur : input.txt introuvable{define.RESET}\nINPUT_PATH : {define.INPUT_PATH}")
	if not os.path.isdir(define.IMAGES_SRC_DIR) :
			exit(f"{define.RED}erreur : dossier source des images introuvable{define.RESET}\nIMAGES_SRC_DIR : {define.IMAGES_SRC_DIR}")
	if not os.path.isdir(define.IMAGES_DST_DIR) :
			exit(f"{define.RED}erreur : dossier de destination des images introuvable{define.RESET}\nIMAGES_DST_DIR : {define.IMAGES_DST_DIR}")
	if not os.path.isdir(define.LOG_DIR) :
			exit(f"{define.RED}erreur : dossier des logs introuvable{define.RESET}\nLOG_DIR : {define.LOG_DIR}")

	try :
		a = ankiconnect("version")
		if a != define.ANKI_CONNECT_VERSION :
			exit(f"{define.RED}erreur : mauvaise valeur pour la version d'AnkiConnect{define.RESET}\nversion du add-on : {a}\nANKI_CONNECT_VERSION : {define.ANKI_CONNECT_VERSION}")
	except Exception as e :
		exit(f"{define.RED}erreur : connexion à Anki impossible{define.RESET}\n{e}")

	decks = ankiconnect("deckNames")
	for deck in define.DECK_1, define.DECK_2, define.DECK_3 :
		if deck not in decks :
			print(f"{define.RED}erreur : {deck} : mauvais nom de paquet{define.RESET}\ndecks existants :")
			for d in decks :
				print(f" - {d}")
			exit()

	myModels = define.TYPE_1, define.TYPE_2, define.TYPE_3, define.TYPE_4
	myFieldss = define.FIELDS_TYPE_1, define.FIELDS_TYPE_2, define.FIELDS_TYPE_3, define.FIELDS_TYPE_4
	modelsAnki = ankiconnect("modelNames")
	for myModel, myFields in zip(myModels, myFieldss) :
		if myModel not in modelsAnki :
			print(f"{define.RED}erreur : {myModel} : mauvais nom de type de note{define.RESET}\ntypes de notes existants :")
			for m in modelsAnki :
				print(f" - {m}")
			exit()
		fieldsAnki = ankiconnect("modelFieldNames", {"modelName": myModel})
		for field in myFields :
			if field not in fieldsAnki :
				print(f"{define.RED}erreur : {field} : mauvais nom de champ dans le type de note \'{myModel}\'{define.RESET}\nchamps existants :")
				for f in fieldsAnki :
					print(f" - {f}")
				exit()
