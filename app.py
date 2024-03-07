from flask import Flask, render_template, request, abort, jsonify
import magic

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
    if "file" not in request.files:
        return jsonify({"error": "No file found"}, 400)

    file = request.files("file")

    # type check file to ensure is audio
    mime_type = magic.from_buffer(file.read(1024), mime=True)
    if not mime_type.startswith("audio/"):
        return jsonify({"error": "File is not a valid audio type"}), 400

    # Process audio file
    result = process(file)
    return result


def process(**args):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=8888)
