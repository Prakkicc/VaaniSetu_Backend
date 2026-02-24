from rest_framework import serializers
from .models import Scheme

class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = '__all__'

class UserProfileSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    income = serializers.IntegerField()
    gender = serializers.CharField()
    caste = serializers.CharField()
    state = serializers.CharField()
    scheme_type = serializers.CharField(required=False)