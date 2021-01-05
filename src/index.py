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


@app.route("/mine-properties", methods=['GET'])
def upload_images():
    query = request.args.get('q')
    if not query:
        return jsonify(error="q parameter required")

    json_doc = nlp((query)).to_json()
    predictions = mine_json_doc(json_doc, COPULAS)
    return jsonify(query=query, predictions=predictions)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', debug=False, port=port)
    print("running...")
