from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from .GeneratorAI.Senario import Senario

import openai
import os
import json
import base64
import pyrebase

config = {
    "apiKey": os.environ["FIREBASE_API_KEY"],
    "authDomain": os.environ["FIREBASE_AUTO_DOMAIN"],
    "databaseURL": os.environ["FIREBASE_URL"],
    "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

api_key = os.environ["OPENAI_API_KEY"]
organization = os.environ["OPENAI_ORGANIZATION"]
openai.organization = organization
openai.api_key = api_key


# Create your views here.
@api_view(["GET"])
def index(request):
    return Response("openai_api")


@api_view(["GET"])
def step3(request, uuid, chapter_no):
    sitation: str = (
        db.child("content")
        .child("CHAPTER" + chapter_no)
        .child("sitation")
        .child(request.GET.sitation)
        .get()
    )
    partner: str = request.GET.partner
    grammar: str = (
        db.child("content").child("CHAPTER" + chapter_no).child("grammar").get()
    )
    expression: str = (
        db.child("content")
        .child("CHAPTER" + chapter_no)
        .child("expression")
        .child(request.GET.sitation)
        .get()
    )
    word: str = db.child(uuid).child("word").get()

    senario = Senario(
        sitation=sitation,
        partner=partner,
        grammar=grammar,
        expression=expression,
        word=word,
    )

    try_n = 2

    for i in range(try_n):
        # 예문 생성
        try:
            completion = create_ChatCompletion(
                senario.get_system_content(),
                senario.get_user_content(),
            )
        except Exception as e:
            print(e)
            if i == 1:
                return Response(
                    "openai connect fail", status=HTTP_500_INTERNAL_SERVER_ERROR
                )
            continue

        # json 문자열 -> json 객체
        try:
            senario_result = json.loads(completion.choices[0].message.content)
        except Exception as e:
            print("Not json")
            if i == 1:
                return Response("convert fail", status=HTTP_500_INTERNAL_SERVER_ERROR)
            continue
        break

    sence_image = image_create(senario_result["scene"])
    del senario_result["scene"]
    senario_result["sence_image"] = sence_image

    for dialogue in senario_result["dialogue"]:
        dialogue_image = image_create(dialogue["image_prompt"])
        del dialogue["image_prompt"]
        dialogue["dialogue_images"] = dialogue_image

    return Response(senario_result)


def create_ChatCompletion(system_content: str, user_content: str):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": user_content,
            },
        ],
    )


def image_create(description: str) -> bytes:
    sence_image = openai.Image.create(
        prompt=(description + " without person at daytime."),
        n=1,
        size="512x512",
        response_format="b64_json",
    )

    return base64.b64decode(sence_image["data"][0]["b64_json"])
