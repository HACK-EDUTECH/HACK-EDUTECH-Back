from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def index(request):
    return Response("openai_api")


@api_view(["GET"])
def step3(request, uuid, chapter_no):
    data = {
        "test":"123",
        "UUID": uuid,
        "chapter_no": chapter_no,
    }
    return Response(data)