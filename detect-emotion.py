from moviepy.editor import *
import sys
import time
import json
import requests

filename = "C:\\Users\\jwang\\Desktop\\emotions\\hope.mp4"
 
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data
 
headers = {'authorization': "104f6cf196074ea683617d6dc512ab32"}
response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(filename))

uploadUrl = response.json()["upload_url"];

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
  "audio_url": uploadUrl
}

headers = {
    "authorization": "104f6cf196074ea683617d6dc512ab32",
    "content-type": "application/json"
}

response = requests.post(endpoint, json=json, headers=headers)

id = response.json()["id"]

endpoint = "https://api.assemblyai.com/v2/transcript/"+id

headers = {
    "authorization": "104f6cf196074ea683617d6dc512ab32",
}
while response.json()["status"] != "completed":
    response = requests.get(endpoint, headers=headers)
    time.sleep(2)
    print(response.json()["status"])

transcript = response.json()["text"]

clip = VideoFileClip(filename)
clip.save_frame("C:\\Users\\jwang\\Desktop\\emotions\\frame2.png", t = 2)

def detect_faces(path, text):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
 
    for face in faces:
        if(likelihood_name[face.anger_likelihood] == 'VERY_LIKELY'):
            text = text + '>:('
        elif(likelihood_name[face.joy_likelihood] == 'VERY_LIKELY'):
            text = text + ':)'
        elif(likelihood_name[face.surprise_likelihood] == 'VERY_LIKELY'):
            text = text + ':O'
        else:   
            text = text + '¯\_(ツ)_/¯'

    print(text)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_faces("C:\\Users\\jwang\\Desktop\\emotions\\frame2.png", transcript)