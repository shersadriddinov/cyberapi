from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):
	"""

	"""
	class Meta:
		model = Token
		fields = ('key', )


class GeneralUserSerializer(serializers.ModelSerializer):
	"""
	All :model:`User` fields
	"""

	class Meta:
		model = User
		fields = ("id", "username", "email")


class NewUserSerializer(serializers.Serializer):
	"""

	"""
	user = GeneralUserSerializer()
	token = TokenSerializer()
