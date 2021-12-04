from flask import Flask, request, render_template, send_from_directory
from functions import read_json, search_tag, jsondump, view_tag

POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)


@app.route("/")
def page_index():
    tags = view_tag(POST_PATH)
    return "render_template('index.html', tags=tags)"


@app.route("/tag/", methods=["GET"])
def page_tag():
    tag_name = request.args.get('tag')
    if not tag_name:
        return "Record not found", 400
    tags = search_tag(tag_name, POST_PATH)
    return render_template('post_by_tag.html', tags=tags, tag_name=tag_name)


@app.route("/post", methods=["GET", "POST"])
def page_post_create():
    data = read_json(POST_PATH)
    if request.method == "GET":
        return render_template("post_form.html")
    if request.method == "POST":
        try:
            file = request.files['picture']
        except:
            return '', 400
        else:
            add_post = jsondump(POST_PATH, file, data, UPLOAD_FOLDER, request)
            return render_template("post_uploaded.html", **add_post)


@app.route("/uploads/images/<path:path>")
def static_dir(path):
    return send_from_directory(UPLOAD_FOLDER, path)


if __name__ == "__main__":
    app.run('127.0.0.1', 8000)
