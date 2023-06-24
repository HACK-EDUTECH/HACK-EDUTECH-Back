from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import os
import pyrebase
import pandas as pd
import json

config = {
    "apiKey": os.environ["FIREBASE_API_KEY"],
    "authDomain": os.environ["FIREBASE_AUTO_DOMAIN"],
    "databaseURL": os.environ["FIREBASE_URL"],
    "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


# Create your views here.
@api_view(["GET", "POST"])
def index(request):
    if request.method == "POST":
        data_file = request.FILES["data"]
        df = pd.read_excel(data_file, index_col=0)
        result = df.to_json(orient="table")
        print(result)
        database.update({"data_table": json.loads(result)})

        return HttpResponseRedirect("/")

    pyreResponse = database.child("data_table").get()
    data = pyreResponse.val()
    # for v in data.items():
    #     print(v)
    return render(request, "data_input/main.html", data)
