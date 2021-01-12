import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import en_core_web_sm
import json
import spacy
import itertools

from mine_properties import mine_json_doc
from data.index import COPULAS

nlp = en_core_web_sm.load()

app = Flask(__name__)
CORS(app)


def flatten(arr):
    return list(itertools.chain(*arr))


@app.route("/mine-properties", methods=['POST'])
def upload_images():
    if not request.json:
        return jsonify(error="json array required")

    print(f"mining properties in {len(request.json)} passages...")

    result = []

    for passage in request.json:
        requires_tokenization = isinstance(passage, str)
        sentences = [s.text for s in list(nlp(passage).sents)] if requires_tokenization else passage
        properties = flatten([
            mine_json_doc(nlp((sentence)).to_json(), COPULAS) for sentence in sentences
        ])
        print(f"{len(properties)} properties found")
        result.append(properties)

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', debug=False, port=port)
    print("running...")
