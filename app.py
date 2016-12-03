from pprint import pprint
from clarifai.rest import ClarifaiApp
import json


app = ClarifaiApp()
files = ['https://samples.clarifai.com/metro-north.jpg']
d = app.tag_urls(files)

pprint(d['outputs'])
