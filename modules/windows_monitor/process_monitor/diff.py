import json

def diff_registry(old_file, new_file):
    with open(old_file) as f:
        old = json.load(f)
    with open(new_file) as f:
        new = json.load(f)

    changes = []

    for key in new:
        if key not in old:
            changes.append({"key": key, "change": "NEW KEY"})
        else:
            for val in new[key]:
                if val not in old[key]:
                    changes.append({"key": key, "value": val, "change": "ADDED"})

    return changes
