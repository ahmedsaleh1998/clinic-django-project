# class CommentSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     content = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField()

#     def create(self, validated_data):
#         return Comment(**validated_data)

#     def update(self, instance, validated_data):
#         instance.email = validated_data.get('email', instance.email)
#         instance.content = validated_data.get('content', instance.content)
#         instance.created = validated_data.get('created', instance.created)
#         return instance

from importlib.metadata import requires
from rest_framework import serializers
from .models import Appointments
from django.contrib.auth.models import User  


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class AppointmentsSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    date=serializers.DateField(required=False)
    time=serializers.TimeField(required=False)
    class Meta:
        model = Appointments
        fields = '__all__'
