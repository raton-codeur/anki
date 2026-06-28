import define
import re

def encode(sections) :
    # sections : le dictionnaire des sections à encoder
    # renvoie le dictionnaire des sections encodées

    for sections_ in sections.values() :
        for section in sections_ :
            for i in range(len(section)) :

                # trimer les textes phonétiques et encoder les "//"
                section[i] = re.sub(
                    define.FORMATS["phonetics"],
                    lambda m: f"/{m.group(1).strip()}/",
                    section[i]
                )

                # trimer les trous
                section[i] = re.sub(
                    define.FORMATS["cloze"],
                    lambda m: (
                        f"{{{{c{m.group(1)}::{m.group(2).strip()}}}}}"
                        if (m.group(3) is None or m.group(3).strip() == "")
                        else f"{{{{c{m.group(1)}::{m.group(2).strip()}::{m.group(3).strip()}}}}}"
                    ),
                    section[i]
                )

                # encoder les balises : trimer le texte, mettre le bon code HTML...
                # pour les images, on encode aussi la hauteur.
                # on remplace temporairement les "<" et ">" des balises.
                section[i] = re.sub(
                    define.FORMATS["img"],
                    lambda m: f'LEFT_ANGLE_BRACKETimg src="{m.group(2).strip()}" style="height: {int(m.group(1) or define.DEFAULT_IMG_HEIGHT) * define.LINE_HEIGHT}px;"RIGHT_ANGLE_BRACKET',
                    section[i]
                )
                section[i] = re.sub(
                    define.FORMATS["red"],
                    lambda m: f'LEFT_ANGLE_BRACKETspan style="color: red;"RIGHT_ANGLE_BRACKET{m.group(1).strip()}LEFT_ANGLE_BRACKET/spanRIGHT_ANGLE_BRACKET',
                    section[i]
                )
                section[i] = re.sub(
                    define.FORMATS["sup"],
                    lambda m: f"LEFT_ANGLE_BRACKETsupRIGHT_ANGLE_BRACKET{m.group(1).strip()}LEFT_ANGLE_BRACKET/supRIGHT_ANGLE_BRACKET",
                    section[i]
                )
                section[i] = re.sub(
                    define.FORMATS["sub"],
                    lambda m: f"LEFT_ANGLE_BRACKETsubRIGHT_ANGLE_BRACKET{m.group(1).strip()}LEFT_ANGLE_BRACKET/subRIGHT_ANGLE_BRACKET",
                    section[i]
                )
                section[i] = re.sub(
                    define.FORMATS["b"],
                    lambda m: f"LEFT_ANGLE_BRACKETbRIGHT_ANGLE_BRACKET{m.group(1).strip()}LEFT_ANGLE_BRACKET/bRIGHT_ANGLE_BRACKET",
                    section[i]
                )
                section[i] = re.sub(
                    define.FORMATS["shade"],
                    lambda m: f'LEFT_ANGLE_BRACKETdiv style="background-color: rgba(0, 0, 0, 0.1);"RIGHT_ANGLE_BRACKET{m.group(1).strip()}LEFT_ANGLE_BRACKET/divRIGHT_ANGLE_BRACKET',
                    section[i]
                )

                # encoder les "<" et ">"
                # et rétablir ceux des balises
                section[i] = section[i].replace("<", "&lt;").replace(">", "&gt;")
                section[i] = section[i].replace("LEFT_ANGLE_BRACKET", "<").replace("RIGHT_ANGLE_BRACKET", ">")

                # encoder les tabulations
                section[i] = section[i].replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

                # encoder les \n
                section[i] = section[i].replace("\n", "<br>")

                # supprimer les "\" devant "@", "//", "-"
                section[i] = section[i].replace("\\@", "@").replace("\\//", "//").replace("\\-", "-")

    return sections