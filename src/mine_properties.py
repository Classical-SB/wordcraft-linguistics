from data.index import VERB_TAGS


def first_or_none(lst):
    return None if len(lst) == 0 else lst[0]


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def children_for(json_doc, head_id, recursive=False):
    """Recursively find the children and the children's children for a word in a dependency tree.


    """
    results = []

    for x in json_doc["tokens"]:
        if x["head"] == head_id and x["id"] != head_id:
            results.append(x)

    if recursive and len(results) > 0:
        return results + flatten([children_for(json_doc, r["id"], True) for r in results])
    else:
        return results


def find_token_by_attr(tokens, attr, value):
    results = [t for t in tokens if t[attr] == value]
    return first_or_none(results)


def filter_token_by_attr(tokens, attr, value):
    return [t for t in tokens if t[attr] != value]


def filter_token_by_attrs(tokens, k_v_pairs):
    for key, value in k_v_pairs:
        tokens = filter_token_by_attr(tokens, key, value)
    return tokens


def get_verbs(json_doc, only=None):
    results = []
    for x in json_doc["tokens"]:
        value = value_for_token(x, json_doc)
        is_verb = x["pos"] in VERB_TAGS
        include = only is None or value in only
        if is_verb and include:
            results.append(x)
    return results


def sorted_values(tokens, json_doc):
    return [value_for_token(t, json_doc) for t in sorted(tokens, key=lambda w: w["id"])]


def value_for_token(token, json_doc):
    return json_doc["text"][token["start"]:token["end"]].lower()


def mine_properties(json_doc, verbs):
    results = []

    for verb in get_verbs(json_doc, verbs):
        children = children_for(json_doc, verb["id"])
        subject = find_token_by_attr(children, "dep", "nsubj")
        other = filter_token_by_attrs(children, [("dep", "nsubj"), ("pos", "PUNCT")])

        if subject is None:
            continue

        subject_deps = children_for(json_doc, subject["id"])
        subject_deps = filter_token_by_attrs(subject_deps, [("pos", "DET"), ("pos", "PUNCT")])
        word = [subject] + subject_deps

        properties = []

        for o in other:
            properties.append(o)
            other_deps = children_for(json_doc, o["id"], True)
            properties += filter_token_by_attrs(other_deps, [("pos", "DET")])

        word = sorted_values(word, json_doc)
        properties = sorted_values(properties, json_doc)

        results.append((" ".join(word), " ".join(properties)))

    return results
