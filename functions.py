import json, os
from pathlib import Path


def read_json(name):
    with open(name, "r", encoding='utf-8') as file:
        return json.load(file)


def search_tag(tag_name, POST_PATH):
    tags = []
    tag = str("#") + tag_name
    for i in read_json(POST_PATH):
        if tag in i['content'].lower():
            tags.append(i)
    return tags

def view_tag(POST_PATH):
    tags = []
    for i in read_json(POST_PATH):
        for tag in i['content'].split(' '):
            if tag.startswith("#"):
                tags.append(tag.lstrip("#").lower())
    tags = set(tags)
    return tags

def jsondump(POST_PATH, file, data, UPLOAD_FOLDER, request):
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
    return add_post
