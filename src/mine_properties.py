from data.index import VALID_PREDICATE_K_V_PAIRS, VERB_TAGS

VERBOSE = False


def LOG(msg):
    if VERBOSE:
        print(msg)


def first_or_none(lst):
    return None if len(lst) == 0 else lst[0]


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def children_for(json_doc, head_id, recursive=False):
    """Recursively find the children and the children's children for a word in a dependency tree."""
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


def filter_tokens_by_attr(tokens, attr, value):
    return [t for t in tokens if t[attr] != value]


def filter_tokens_by_attrs(tokens, k_v_pairs):
    for key, value in k_v_pairs:
        tokens = filter_tokens_by_attr(tokens, key, value)
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


def select_tokens_by_attr(tokens, attr, value):
    return [t for t in tokens if t[attr] == value]


def select_tokens_by_attrs(tokens, k_v_pairs):
    result = []
    for key, value in k_v_pairs:
        result += select_tokens_by_attr(tokens, key, value)
    return result


def sorted_values(tokens):
    return [t for t in sorted(tokens, key=lambda w: w["id"])]


def value_for_token(token, json_doc):
    return json_doc["text"][token["start"]:token["end"]].lower()

# point of entry


def mine_json_doc(json_doc, verbs):
    try:
        results = []

        for verb in get_verbs(json_doc, verbs):
            children = children_for(json_doc, verb["id"])
            LOG(f"parsing verb {value_for_token(verb, json_doc)}...")
            subject = find_token_by_attr(children, "dep", "nsubj")
            if subject is None:
                continue

            LOG(f"\n\tsubject is: {value_for_token(subject, json_doc)}")
            LOG(subject)
            predicates = select_tokens_by_attrs(children, VALID_PREDICATE_K_V_PAIRS)
            subject_deps = children_for(json_doc, subject["id"])
            subject_deps = filter_tokens_by_attrs(subject_deps, [("pos", "DET"), ("pos", "PUNCT")])
            LOG(f"\t\tdependencies are: {', '.join([value_for_token(o, json_doc) for o in subject_deps])}")
            word = [subject] + subject_deps
            properties = []
            LOG(f"\n\tpredicates are: {', '.join([value_for_token(o, json_doc) for o in predicates])}")

            for o in predicates:
                LOG(f"\n\tparsing predicate {value_for_token(o, json_doc)}...")
                properties.append(o)
                other_deps = children_for(json_doc, o["id"], True)
                filtered = filter_tokens_by_attrs(other_deps, [("pos", "DET")])
                LOG(f"\t\tdependencies are: {', '.join([value_for_token(o, json_doc) for o in filtered])}")
                properties += filtered

            word = sorted_values(word)
            properties = sorted_values(properties)
            if len(properties) == 0:
                continue

            joined = (
                " ".join([value_for_token(t,json_doc) for t in word]),
                " ".join([value_for_token(t,json_doc) for t in properties])
            )

            results.append({"subject":word, "properties":properties,"joined":joined})

        return results
    except Exception as error:
        LOG(f"ERROR: {error}")
        return error
