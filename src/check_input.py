from check_param import *
import pyperclip, re, shutil
from section_transform import *

def check_top(lines) :
	if not lines :
		exit(f"{define.RED}erreur : l'input est vide{define.RESET}")
	firstline = lines[0].strip()
	if firstline not in define.SEPARATORS :
		pyperclip.copy(lines[0])
		exit(f"{define.RED}erreur : l'input ne commence pas par un séparateur{define.RESET}")

def check_angle_brackets(sections) :
	"""pas de LEFT_ANGLE_BRACKET ni RIGHT_ANGLE_BRACKET dans les sections brutes"""
	for type, sections_ in sections.items() :
		for section in sections_ :
			if re.search(r"LEFT_ANGLE_BRACKET|RIGHT_ANGLE_BRACKET", section) :
				pyperclip.copy(section)
				exit(f"{define.RED}erreur : \"LEFT_ANGLE_BRACKET\" ou \"RIGHT_ANGLE_BRACKET\" trouvé dans une section{define.RESET}\n"
					f"section {type} copiée : {define.YELLOW}{section}{define.RESET}")

def check_MS(sections) :
	"""pas d'image ni trou ni tab dans les sections MS"""
	for section in sections :

		# check tabs
		if "\t" in section :
			pyperclip.copy(section)
			exit(f"{define.RED}erreur : tabulation dans une section MS{define.RESET}\n"
				f"section MS copiée : {define.YELLOW}{section}{define.RESET}")

		# check images
		if re.search(define.FORMATS["img"], section) :
			pyperclip.copy(section)
			exit(f"{define.RED}erreur : image dans une section MS{define.RESET}\n"
				f"section MS copiée : {define.YELLOW}{section}{define.RESET}")

		# check trou
		if re.search(define.FORMATS["cloze"], section) :
			pyperclip.copy(section)
			exit(f"{define.RED}erreur : trou dans une section MS{define.RESET}\n"
				f"section MS copiée : {define.YELLOW}{section}{define.RESET}")

def check_Z(sections) :
	""" pas de trou vide dans les sections Z1, Z2, Z3 """
	for type in "Z1", "Z2", "Z3" :
		for section in sections[type] :
			for m in re.finditer(define.FORMATS["extended_cloze"], section) :
				main = m.group(2)
				hint = m.group(4)
				if main.strip() == "" :
					pyperclip.copy(section)
					exit(f"{define.RED}erreur : trou vide{define.RESET}\n"
						f"section {type} copiée : {define.YELLOW}{section}{define.RESET}")
				if hint is not None and hint.strip() == "" :
					pyperclip.copy(section)
					exit(f"{define.RED}erreur : indice de trou vide{define.RESET}\n"
						f"section {type} copiée : {define.YELLOW}{section}{define.RESET}")

def check_and_move_images(sections) :
	for type, sections_tmp in sections.items() :
		if type == "MS" :
			continue
		for section in sections_tmp :
			names = re.findall(define.FORMATS["img"], section)
			for name in names :
				name = name.strip()
				name_src = os.path.join(define.IMAGES_SRC_DIR, name)
				name_dst = os.path.join(define.IMAGES_DST_DIR, name)
				if not name :
					pyperclip.copy(section)
					exit(f"{define.RED}erreur : image vide{define.RESET}\n"
							f"section {type} copiée : {define.YELLOW}{section}{define.RESET}")
				elif not re.fullmatch(r"^[\w \-\(\)\.]+$", name, flags=re.ASCII) :
					pyperclip.copy(section)
					exit(f"{define.RED}erreur : nom d'image invalide{define.RESET}\n"
							f"nom : \"{name}\"\nautorisés :\n"
							"- lettre (sans accent)\n"
							"- chiffre\n"
							"- espace\n"
							"- underscore\n"
							"- tiret\n"
							"- parenthèse\n"
							"- point\n"
							f"section {type} copiée : {define.YELLOW}{section}{define.RESET}")
				elif not os.path.exists(name_src) and not os.path.exists(name_dst) :
					pyperclip.copy(section)
					exit(f"{define.RED}erreur : \"{name}\" : image introuvable{define.RESET}\n"
							f"dossier source : {define.IMAGES_SRC_DIR}\n"
							f"dossier destination : {define.IMAGES_DST_DIR}\n"
							f"section {type} copiée : {define.YELLOW}{section}{define.RESET}")
				elif os.path.exists(name_src) :
					if os.path.exists(name_dst) :
						pyperclip.copy(section)
						exit(f"{define.RED}erreur : \"{name}\" : une image du même nom existe déjà dans le dossier de destination{define.RESET}\n"
					 	f"section {type} copiée : {define.YELLOW}{section}{define.RESET}")
					shutil.move(name_src, name_dst)

def check_fields(sections_fields, sections_raw) :

	# nombre de champs
	for type, sections in sections_fields.items() :
		for i in range(len(sections)) :
			if len(sections[i]) > define.NB_FIELDS[type] :
				pyperclip.copy(sections_raw[type][i])
				exit(f"{define.RED}erreur : trop de changements de champs{define.RESET}\n"
						f"section {type} ({define.NB_FIELDS[type]} champs) copiée : {define.YELLOW}{sections_raw[type][i]}{define.RESET}")

	# premiers champs
	for type, sections in sections_raw.items() :
		for i in range(len(sections)) :
			if any(sections_fields[type][i]) :
				if not sections_fields[type][i][0] :
					pyperclip.copy(sections_raw[type][i])
					exit(f"{define.RED}erreur : premier champ vide{define.RESET}\n"
							f"section {type} copiée : {define.YELLOW}{sections_raw[type][i]}{define.RESET}")

	# deuxièmes champs des types C2
	for i in range(len(sections_raw["C2"])) :
		if sections_fields["C2"][i][0] and not sections_fields["C2"][i][1] :
			pyperclip.copy(sections_raw["C2"][i])
			exit(f"{define.RED}erreur : deuxième champ vide{define.RESET}\n"
					f"section C2 copiée : {define.YELLOW}{sections_raw['C2'][i]}{define.RESET}")

	# troisième champ des types MS
	for i in range(len(sections_raw["MS"])) :
		if sections_fields["MS"][i][0] and not sections_fields["MS"][i][2] :
			pyperclip.copy(sections_raw["MS"][i])
			exit(f"{define.RED}erreur : troisième champ (\"français\") vide{define.RESET}\n"
					f"section MS copiée : {define.YELLOW}{sections_raw['MS'][i]}{define.RESET}")

	# trou dans les deuxièmes champs des types Z1, Z2, Z3
	for type in "Z1", "Z2", "Z3" :
		for i in range(len(sections_raw[type])) :
			if sections_fields[type][i][0] and re.search(define.FORMATS["cloze"], sections_fields[type][i][1]) :
				pyperclip.copy(sections_raw[type][i])
				exit(f"{define.RED}erreur : trou dans le deuxième champ{define.RESET}\n"
						f"section {type} copiée : {define.YELLOW}{sections_raw[type][i]}{define.RESET}")