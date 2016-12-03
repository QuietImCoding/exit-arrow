from pprint import pprint
from clarifai.rest import ClarifaiApp
import json

app = ClarifaiApp()
url = raw_input("Pick a photo: ")
files = [url]
search = ["dinosaur"]
d = app.tag_urls(files)

for image in d["outputs"]:
    dinosaur = False
    tags = []
    for concept in image["data"]["concepts"]:
        if concept["name"].lower() in search:
            dinosaur = True
        else:
            tags.append(concept["name"].lower())
    if dinosaur:
        print "DINOSAUR!!"
    else:
        print "NOT A DINOSAUR"
        print tags


