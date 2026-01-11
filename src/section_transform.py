import define
import re, pyperclip

def first_split(lines) :
	# on veut une liste des sections
	# une section c'est un tuple (séparateur, texte)

	sections = []
	current_sep = None
	current_lines = []

	for line in lines :
		if line.strip() in define.SEPARATORS :
			if current_sep is not None :
				# on avait une section en cours
				sections.append((current_sep, "\n".join(current_lines)))
			current_sep = line.strip()
			current_lines = []
		else :
			current_lines.append(line)

	sections.append((current_sep, "\n".join(current_lines)))

	# sections est maintenant une liste de tuples (séparateur, texte)

	# on veut séparer les sections selon le séparateur

	# séparateur -> nouveau nom de section
	get_new_key = {
			"-": "1",
			"--": "2",
			"---": "3",
			"-)": "MS"
	}

	sections_tmp = {"1": [], "2": [], "3": [], "MS": []}
	for sep, section in sections :
		sections_tmp[get_new_key[sep]].append(section)
	sections = sections_tmp

	# sections est maintenant un dictionnaire avec
		#	clés : "1", "2", "3", "MS"
		# valeur : la liste des sections correspondantes

	# on veut séparer les sections avec trou

	sections_tmp = {"C1": [], "C2": [], "C3": [], "Z1": [], "Z2": [], "Z3": [], "MS": sections["MS"]}
	for i in "1", "2", "3" :
		for section in sections[i] :
			if re.search(define.FORMATS["cloze"], section) :
				key = "Z" + i
			else :
				key = "C" + i
			sections_tmp[key].append(section)
	sections = sections_tmp

	# sections est maintenant un dictionnaire avec [ clés : "C1", "C2", "C3", "Z1", "Z2", "Z3", "MS" ]
	# et [ valeur : la liste des sections correspondantes ]

	return sections

def trim_lines(sections) :
	# on veut trimer toutes les lignes
	# soft à gauche, hard à droite

	result = {}
	for type, sections_ in sections.items() :
		result[type] = []
		for section in sections_ :
			result[type].append("\n".join([line.rstrip(" \t").lstrip(" ") for line in section.splitlines()]))

	return result


def split_fields(sections) :
	# on veut séparer les champs des sections
	# et soft trimer les champs

	# si on a plus de champs que prévu, tant pis.
	# si on a moins de champs que prévu, on complète avec des champs vides.

	result = {}
	for type, sections_ in sections.items() :
		result[type] = []
		nb_fields = define.NB_FIELDS[type]
		for section in sections_ :
			new = [field.strip(" \n\r") for field in re.split(r"(?<!\\)@", section)]
			if type == "MS" and len(new) == 2 :
				new.insert(1, "")
				new.append("")
			if (len(new) < nb_fields) :
				new.extend([""] * (nb_fields - len(new)))
			result[type].append(new)

	# une section de sections est maintenant appairée dans result avec la liste de ses champs soft trimés.
	# par exemple :
	# sections["C1"] = [" a@b ", "blabla", ...]
	# result["C1"] = [["a", "b"], ["blabla", ""], ...]

	return result

def remove_empty_sections(sections_fields) :
	result = {}
	for type, sections in sections_fields.items() :
		sections = [section for section in sections if any(section)]
		result[type] = sections
	return result
