import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import en_core_web_sm
import itertools
import json

from mine_properties import mine_json_doc,value_for_token
from data.index import COPULAS
from data.wordcraft_words import WORDCRAFT_WORDS

nlp = en_core_web_sm.load()

app = Flask(__name__)
CORS(app)


def flatten(arr):
    return list(itertools.chain(*arr))

def get_lemmas(tokens):
    return [t["lemma"]for t in tokens]

def wordcraft_words_in(prop):
    lemmas = get_lemmas(prop["subject"]) + get_lemmas(prop["properties"])
    words = [w for w in WORDCRAFT_WORDS if w in lemmas]
    return {"words":words,"count":len(words)}

def has_wordcraft_word(prop):
    return wordcraft_words_in(prop)["count"] > 0

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]    

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        print(len(file_data),"articles")
        
        try:
            updated_data = file_data + new_data
            file.seek(0)
            json.dump(updated_data, file, indent = 4)
        except Exception as e:
            file.seek(0)
            json.dump(file_data, file, indent = 4)

@app.route("/save-passages", methods=['POST'])
def save_passages():
    write_json(request.json)
    return jsonify(success=1)

@app.route("/mine-properties", methods=['GET'])
def upload_images():
    text = request.args.get("text")
    title = request.args.get("title")
    print("text=",text)
    return jsonify(success=1)
    # doc = nlp(text)
    # json_doc = doc.to_json()
    # properties = mine_json_doc(json_doc, COPULAS)
    # properties = [p for p in properties if has_wordcraft_word(p)]

    # count = sum([wordcraft_words_in(p)["count"] for p in properties])
    # words = flatten([wordcraft_words_in(p)["words"] for p in properties])
    
    # ranges = sorted(flatten([p["subject"] + p["properties"] for p in properties]), key=lambda w: w["start"])
    # increment = 0
    # for r in ranges:
    #     start_str = '<span style="color:blue;">'
    #     text = insert_str(text, start_str, r["start"] + increment)
    #     increment += len(start_str)
    #     end_str = '</span>'
    #     text = insert_str(text, end_str, r["end"] + increment)
    #     increment += len(end_str)
    # tagged = "<p>" + text + "</p>"


    # if len(properties) > 0:
    #     print(properties)
    #     with open("Output.html", "a") as f:
    #         f.write(f"\n<h3>{title}</h3>\n")
    #         f.write(tagged)
    #         f.write(f"\n<h5>{' '.join(words)}</h5>")

    
    # return jsonify({
    #     "count":count,
    #     "words":words,
    #     "tagged":tagged,
    #     "joined": [p["joined"] for p in properties]
    # })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', debug=True, port=port)
    print("running...")
