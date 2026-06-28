import define
import re, requests, send2trash, shutil, os

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

def print_sections(sections) :
    for type, sections_ in sections.items() :
        if sections_ :
            print(f"  {type} : {sections_}")

def print_count_cards(sections) :
    result = {"1" : 0, "2" : 0, "3" : 0, "MS" : 0}
    result["1"] += len(sections["C1"])
    result["1"] += len(sections["R1"])
    result["2"] += len(sections["C2"])
    result["3"] += len(sections["C3"])
    result["3"] += len(sections["R3"])
    result["MS"] += len(sections["MS"])
    for type, deck in (("Z1", "1"), ("Z2", "2"), ("Z3", "3")) :
        for section in sections[type] :
            result[deck] += len({m.group(1) for m in re.finditer(define.FORMATS["cloze"], section[0])})

    for type in "1", "2", "3" :
        print(f"  {type} : {result[type]}")
    if result["MS"] > 0 :
        print(f"  MS : {result['MS']}")

def update_logs() :
    log_9_path = os.path.join(define.LOG_DIR, "9.txt")
    if os.path.exists(log_9_path) :
            send2trash.send2trash(log_9_path)
    for i in range(8, -1, -1) :
            a = os.path.join(define.LOG_DIR, f"{i}.txt")
            b = os.path.join(define.LOG_DIR, f"{i + 1}.txt")
            if os.path.exists(a) :
                    os.rename(a, b)
    shutil.copy(define.INPUT_PATH, os.path.join(define.LOG_DIR, "0.txt"))

def reset_input_file() :
    with open(define.INPUT_PATH, "w") as f :
        f.write("-" + "\n" * 20)

def format_for_ankiconnect(section, type) :
    # section : une liste de champs encodés.
    # on veut renvoyer une section formatée pour ankiconnect.

    result = define.ANKI_CONNECT_MODELS[type].copy()
    result["fields"] = result["fields"].copy()
    for field_name, value in zip(result["fields"].keys(), section) :
        result["fields"][field_name] = value
    return result
