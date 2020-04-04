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

	def update(self, instance, validated_data):
		profile = validated_data.get('profile', None)
		if profile['client_settings_json']:
			print(profile)
			instance.profile.client_settings_json = profile['client_settings_json']
			instance.profile.save()
			del validated_data['profile']
		return super(GeneralUserSerializer, self).update(instance, validated_data)


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
