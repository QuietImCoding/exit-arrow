from pprint import pprint
from clarifai.rest import ClarifaiApp
import json

app = ClarifaiApp()
url = raw_input("Pick a photo: ")
files = [url]
tags = ["dinosaur"]
d = app.tag_urls(files)

for image in d["outputs"]:
    dinosaur = False
    for concept in image["data"]["concepts"]:
        if concept["name"].lower() in tags:
            dinosaur = True
    if dinosaur:
        print "DINOSAUR!!"
    else:
        print "NOT A DINOSAUR"


