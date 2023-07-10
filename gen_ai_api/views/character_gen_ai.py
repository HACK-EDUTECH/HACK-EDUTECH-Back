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
    data: Dict = {"prompt": request.POST}
    try:
        character_b64 = requests.post(url=url, json=data)
        character_image = base64.b64decode(character_b64)

        # save
        with open("temp.jpg", "wb") as f:
            f.write(character_image)

        image_path: str = f"images/{uuid}/character-{datetime.timestamp(datetime.now())}.jpg"
        storage.child(image_path).put("temp.jpg")

        db.child("USER_TABLE").child(uuid).update({"character_url": image_path})
    except Exception as e:
        return Response(
            "Generating character fail", status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response("Generating character success")
