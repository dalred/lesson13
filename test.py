from functions import read_json
POST_PATH = "posts.json"
tags = []
for i in read_json(POST_PATH):
    print(i['content'].lower())