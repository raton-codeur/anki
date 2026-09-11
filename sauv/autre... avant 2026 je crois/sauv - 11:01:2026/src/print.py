import define
import re

def print_sections(sections) :
	for type, sections in sections.items() :
		print(f"{type} : {sections}")

def print_count_cards(sections) :
	result = {"1" : 0, "2" : 0, "3" : 0, "MS" : 0}
	result["1"] += len(sections["C1"])
	result["2"] += len(sections["C2"])
	result["3"] += len(sections["C3"])
	result["MS"] += len(sections["MS"])
	for type, deck in (("Z1", "1"), ("Z2", "2"), ("Z3", "3")) :
		for section in sections[type] :
			result[deck] += len({m.group(1) for m in re.finditer(define.FORMATS["extended_cloze"], section[0])})

	for type in "1", "2", "3" :
		print(f"{type} : {result[type]}")
	print()
	if result["MS"] > 0 :
		print(f"MS : {result['MS']}")
		print()

