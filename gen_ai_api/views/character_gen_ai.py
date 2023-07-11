from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

import requests
import os
import json
import base64
import pyrebase
from datetime import datetime
from typing import List, Dict


# Firebase
config = {
    "apiKey": os.environ["FIREBASE_API_KEY"],
    "authDomain": os.environ["FIREBASE_AUTO_DOMAIN"],
    "databaseURL": os.environ["FIREBASE_URL"],
    "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()


@api_view(["POST"])
def gen_character(request, uuid):
    url: str = os.environ["SD_AI_API"] + "/character/"
    data: Dict = {
        "left_prompt": request.POST["left_prompt"],
        "right_prompt": request.POST["right_prompt"],
    }
    result = requests.post(url=url, json=data)
    if result.status_code != 200:
        return Response(
            "Generating memoryroom fail", status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    print(result)
    b64_json = result.json()
    print(type(b64_json), b64_json.keys())
    image = base64.b64decode(b64_json["image"])

    # save
    with open("temp.jpg", "wb") as f:
        f.write(image)

    image_path: str = f"/image/{uuid}/character-{datetime.timestamp(datetime.now())}.jpg"
    storage.child(image_path).put("temp.jpg")

    db.child("USER_TABLE").child(uuid).update({"character_url": image_path})
    
    return Response("Generating character success")
