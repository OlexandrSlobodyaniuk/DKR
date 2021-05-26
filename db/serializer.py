from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Match
        fields = '__all__'