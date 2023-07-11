"""
URL configuration for django_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import openai, character_gen_ai, memoryroom

app_name="gen_ai_api"
urlpatterns = [
    path("", openai.index, name="index"),
    
    path("step3/<str:uuid>/chapter/<str:chapter_no>/", openai.step3, name="step3"),
    
    path("character/<str:uuid>", character_gen_ai.gen_character, name="gen_character"),
    
    path("memoryroom/<str:uuid>/chapter/<str:chapter_no>/", memoryroom.gen_memoryroom, name="gen_character"),
]