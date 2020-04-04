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


class ProfileSerializer(serializers.ModelSerializer):
	"""

	"""

	class Meta:
		model = Profile
		fields = ('balance', 'donate', 'karma')


class BalanceSerializer(serializers.ModelSerializer):
	"""

	"""
	class Meta:
		model = Profile
		fields = ('balance', )


class GeneralUserSerializer(serializers.ModelSerializer):
	"""
	All :model:`User` fields
	"""
	server_stats = ProfileSerializer(source='profile')

	class Meta:
		model = User
		fields = ("id", "username", "first_name", "email", "server_stats",)
		read_only_fields = ("server_stats", )


class UserListSerializer(serializers.ModelSerializer):
	"""

	"""

	class Meta:
		model = User
		fields = ("id", "username", "first_name",)


class NewUserSerializer(serializers.Serializer):
	"""

	"""
	user = GeneralUserSerializer()
	token = TokenSerializer()
