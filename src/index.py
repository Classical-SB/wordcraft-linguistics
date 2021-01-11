import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import en_core_web_sm
import json
import spacy

from mine_properties import mine_json_doc
from data.index import COPULAS

nlp = en_core_web_sm.load()

app = Flask(__name__)
CORS(app)


@app.route("/mine-properties", methods=['POST'])
def upload_images():
    if not request.json:
        return jsonify(error="json array required")

    result = []

    for passage in request.json:
        predictions = [
            [sentence, mine_json_doc(nlp((sentence)).to_json(), COPULAS)] for sentence in passage
        ]
        propositions_found = any([len(p[1]) > 0 for p in predictions])
        result.append({"predictions": predictions, "propositions_found": propositions_found})

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', debug=False, port=port)
    print("running...")
