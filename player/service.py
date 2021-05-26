from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from rest_framework.response import Response
from db.service import DB

class Auth:
    def __init__(self):
        self.db = DB()

    def login(self,request, username, password):
        player = authenticate(username=username, password=password)
        if player:
            login(request, player)
        else:
            return Response(status=400)

    def logout(self, request):
        logout(request)

    def register(self, data):
        try:
            player = User(**data)
            player.save()
        except:
            return Response(status=400)

