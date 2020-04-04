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


class ClientSettingsJSONSerializer(serializers.ModelSerializer):
	"""

	"""
	client_settings_json = serializers.JSONField()

	class Meta:
		model = Profile
		fields = ('client_settings_json', )


class GeneralUserSerializer(serializers.ModelSerializer):
	"""
	All :model:`User` fields
	"""
	balance = serializers.IntegerField(source='profile.balance', read_only=True)
	donate = serializers.IntegerField(source='profile.donate', read_only=True)
	karma = serializers.IntegerField(source='profile.karma', read_only=True)
	client_settings_json = serializers.JSONField(source='profile.client_settings_json')

	class Meta:
		model = User
		fields = (
			"id", "username", "first_name",
			"email", "balance", "donate",
			"karma", "client_settings_json"
		)
		read_only_fields = ("balance", "donate", "karma")


class UserListSerializer(serializers.ModelSerializer):
	"""

	"""
	client_settings_json = serializers.JSONField(source='profile.client_settings_json', read_only=True)

	class Meta:
		model = User
		fields = ("id", "username", "first_name", "client_settings_json")


class NewUserSerializer(serializers.Serializer):
	"""

	"""
	user = GeneralUserSerializer()
	token = TokenSerializer()
