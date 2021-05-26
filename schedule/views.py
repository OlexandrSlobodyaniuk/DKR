from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.response import Response
from db.service import DB
from db.service import RedisCache
from json import dumps, loads
import redis
import os


DEFAULT_SETTINGS = ['localhost', 6379, 1]
DOCKER_SETTINGS = [os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'), os.environ.get('REDIS_DB')]
cache = redis.Redis(host=DEFAULT_SETTINGS[0], port=DEFAULT_SETTINGS[1], db=DEFAULT_SETTINGS[2])

class ScheduleView(APIView):
    def __init__(self):
        super().__init__()
        self.database = DB()
        self.cache = RedisCache(cache)

    def get(self, request: Request):
        id = request.query_params.get('id', None)
        if id:
            match = self.cache.get(id)
            if match:
                return Response(dumps(match), status=200)
            match = self.database.match_id(id)
            return Response(dumps(match), status=200)
        try:
            team_name = request.query_params.get('team_name', None)
            if team_name:
                match = self.database.match_schedule_team(team_name)
                return Response(dumps(match), status=200)
            else:
                match = self.database.match_schedule()
                return Response(dumps(match), status=200)
        except:
            return Response(status=400)

    def post(self, request: HttpRequest):
        data = loads(request.body)
        try:
            self.database.match_update(data)
            self.cache.delete(data['id'])
            return Response(status=200)
        except:
            return Response(status=400)

    def put(self, request: HttpRequest):
        data = loads(request.body)
        try:
            self.database.match_create(data)
            return Response(status=200)
        except:
            return Response(status=400)

    def delete(self, request: HttpRequest):
        data = loads(request.body)
        try:
            self.database.match_delete(data)
            self.cache.delete(data['id'])
            return Response(status=200)
        except:
            return Response(status=400)

