from flask import Flask, render_template, request, abort, jsonify
import os
from dotenv import load_dotenv
# import magic
import requests
from waitress import serve

load_dotenv()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/assess", methods=["GET", "POST"])
def assess():
    # check request type
    if request.method != "POST":
        abort(403)

    # check for file
    if not request.files.get("file"):
        print("file not found")
        return jsonify({"error": "File not found"}), 400

    print(request.files.get("file"))

    file = request.files.get("file")

    # # type check file to ensure is audio --> not working as expected, moved to front end to retry for added security
    # mime_type = magic.from_buffer(file.read(1024), mime=True)
    # if not mime_type.startswith("audio/") or mime_type.startswith("video/"):
    #     print("file not audio", mime_type)
    #     return jsonify({"error": "File is not a valid audio type"}), 400

    # Process audio file
    result = process(file)
    return {"result": result}


def process(file):
    torchserve_url = os.getenv("torchserve_url")
    files = {"data": (file.filename,
                      file,)}
    response = requests.post(torchserve_url, files)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8888)
