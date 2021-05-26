from .models import Match
from .serializer import MatchSerializer
from rest_framework.response import Response
import redis


class DB:
    def __init__(self):
        self.match = Match
        self.serializer = MatchSerializer


    def match_schedule(self):
        match = self.match.objects.all()
        serializer = self.serializer(match, many=True)
        return serializer.data

    def match_schedule_team(self, team_name):
        match_one = self.match.objects.filter(team_one=team_name)
        match_two = self.match.objects.filter(team_two=team_name)
        match = {*match_one, *match_two}
        serializer = self.serializer(match, many=True)
        return serializer.data

    def match_id(self, id):
        match = self.match.objects.get(pk=id)
        serializer = self.serializer(match)
        return serializer.data

    def match_update(self, data):
        serializer = self.serializer(data)
        new_match = self.match(serializer.data)
        new_match.pk = data['id']
        new_match.save()

    def match_delete(self, data):
        id = data['id']
        self.match.objects.get(pk=id).delete()

    def match_create(self, data):
        serializer = self.serializer(data=data)
        if not serializer.is_valid():
            return Response(status=400)
        new_match = self.match(**serializer.data)
        new_match.save()

class RedisCache:
    def __init__(self, cache: redis.Redis):
        self.redis = cache

    def get(self, id):
        record = self.redis.get(id)
        if not record:
            return None
        return record

    def delete(self, id):
        try:
            self.redis.delete(id)
        except:
            return