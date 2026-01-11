# def split_fields(sections) :
# 	# on veut séparer les champs des sections
# 	# et soft trimer les champs

# 	# si on a plus de champs que prévu, tant pis.
# 	# si on a moins de champs que prévu, on complète avec des champs vides.

# 	result = {"C1" : [], "C2" : [], "C3" : [], "Z1" : [], "Z2" : [], "Z3" : [], "MS" : []}

# 	def get_split_fields(sections, type, nb_fields) :
# 		""" renvoie le split de "sections" en champs soft-trimés """
# 		result = []
# 		for i in range(len(sections)) :
# 			new = [s.strip(" \n\r") for s in re.split(r"(?<!\\)@", sections[i])]
# 			if nb_fields == 4 and len(new) == 2 : # pour mosalingua, quand 2 champs seulement sont donnés
# 				new.insert(1, "")
# 				new.append("")
# 			if (len(new) < nb_fields) :
# 				new.extend([""] * (nb_fields - len(new)))
# 			result.append(new)
# 		return result

# 	for type in "C1", "C3", "Z1", "Z2", "Z3" : # les sections qui ont 2 champs
# 		result[type] = get_split_fields(sections[type], type, 2)
# 	result["C2"] = get_split_fields(sections["C2"], "C2", 3)
# 	result["MS"] = get_split_fields(sections["MS"], "MS", 4)

# 	# une section de sections est maintenant appairée dans result avec la liste de ses champs soft trimés.
# 	# par exemple :
# 	# sections["C1"] = [" a@b ", "blabla", ...]
# 	# result["C1"] = [["a", "b"], ["blabla", ""], ...]

# 	return result
