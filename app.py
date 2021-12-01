import json, os
from pathlib import Path
from flask import Flask, request, render_template, send_from_directory
from functions import read_json
POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)

@app.route("/")
def page_index():
    tags = []
    for i in read_json(POST_PATH):
        for tag in i['content'].split(' '):
            if '#' in tag:
                tags.append(tag.lstrip("#"))
    tags = set(tags)
    return render_template('index.html', tags=tags)


@app.route("/tag/", methods=["GET"])
def page_tag():
    tags = []
    tag_name = request.args.get('tag')
    tag = str("#")+tag_name
    for i in read_json('posts.json'):
        if tag in i['content']:
            tags.append(i)
    return render_template('post_by_tag.html', tags=tags, tag_name=tag_name)


@app.route("/post", methods=["GET", "POST"])
def page_post_create():
    data = read_json(POST_PATH)
    if request.method == "GET":
        return render_template("post_form.html")
    else:
        file = request.files['picture']
        path = Path(os.path.abspath(__file__)).parent
        if not os.path.exists(path.joinpath("uploads", file.filename)):
            file.save(path.joinpath("uploads/images", file.filename))
        add_post = {
            "pic": f"../{UPLOAD_FOLDER}/{file.filename}",
            "content": request.form.get("content"),
        }
        data.append(add_post)
        with open(POST_PATH, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return render_template("post_uploaded.html", **add_post)


@app.route("/uploads/images/<path:path>")
def static_dir(path):
    return send_from_directory(UPLOAD_FOLDER, path)

if __name__ == "__main__":
    app.run('127.0.0.1', 8000)

