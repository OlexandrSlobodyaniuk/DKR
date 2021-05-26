from json import loads
from rest_framework.request import Request
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from .service import Auth
from .serializers import RegistrationSerializer, LogSerializer

class PlayerAuthView(APIView):
    def __init__(self):
        super().__init__()
        self.auth = Auth()
        self.log_serializer = LogSerializer
        self.reg_serializer = RegistrationSerializer
    #for logout
    def get(self, request: Request):
        self.auth.logout(request)
        return Response(status=200)

    #for login
    def post(self ,request: HttpRequest):
        player_data = loads(request.body)
        player_serializer = self.log_serializer(data=player_data)
        if player_serializer.is_valid():
            self.auth.login(request, player_serializer.data['username'],
                            player_serializer.data['password'])
            return Response(status=200)
        else:
            return Response(status=400)

    #for register
    def put(self, request: Request):
        player_data = loads(request.body)
        player_serializer = self.reg_serializer(data=player_data)
        if player_serializer.is_valid():
            self.auth.register(player_serializer.data)
            return Response(status=200)
        return Response(status=400)
