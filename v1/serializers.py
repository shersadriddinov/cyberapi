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


class CharacterSerializer(serializers.ModelSerializer):
	"""

	"""

	class Meta:
		model = Character
		fields = ("id", "tech_name", "default")


class UserCharacterSerializer(serializers.ModelSerializer):
	"""

	"""

	class Meta:
		model = UserCharacter
		fields = ("id", "profile", "character", "date_added", "main")


class UserWeaponSerializer(serializers.ModelSerializer):
	"""

	"""

	class Meta:
		model = UserWeapon
		fields = (
			"id", "profile", "weapon_with_addons", "main",
			"user_addon_stock", "user_addon_barrel", "user_addon_muzzle",
			"user_addon_mag", "user_addon_scope", "user_addon_grip"
		)


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
			"karma", "client_settings_json",
		)
		read_only_fields = ("balance", "donate", "karma",)

	def update(self, instance, validated_data):
		profile = validated_data.get('profile', None)
		if profile['client_settings_json']:
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


class UserUnrealSerializer(serializers.Serializer):
	users = UserListSerializer(many=True)


class WeaponSerializer(serializers.ModelSerializer):
	"""

	"""

	class Meta:
		model = Weapon
		fields = ("id", "tech_name", "default", "slot")


class NewUserSerializer(serializers.Serializer):
	"""

	"""
	user = GeneralUserSerializer()
	token = TokenSerializer()
	start_characters = CharacterSerializer(many=True)
	start_weapons_first_slot = WeaponSerializer(many=True)
	start_weapons_second_slot = WeaponSerializer(many=True)


class CharacterUnrealSerializer(serializers.Serializer):
	characters = CharacterSerializer(many=True)


class WeaponUnrealSeializer(serializers.Serializer):
	weapons = WeaponSerializer(many=True)


class AddonSerializer(serializers.Serializer):
	"""

	"""
	id = serializers.IntegerField()
	tech_name = serializers.CharField()
	default = serializers.BooleanField()


class WeaponAddonSerializer(serializers.Serializer):
	"""

	"""
	weapon = WeaponSerializer()
	stock = AddonSerializer(many=True)
	barrel = AddonSerializer(many=True)
	muzzle = AddonSerializer(many=True)
	mag = AddonSerializer(many=True)
	scope = AddonSerializer(many=True)
	grip = AddonSerializer(many=True)


class UserWeaponConfigSerializer(serializers.ModelSerializer):
	"""

	"""

	class Meta:
		model = UserWeaponConfig
		fields = "__all__"


class UserWeaponConfigUnrealSerializer(serializers.Serializer):
	configs = UserWeaponConfigSerializer(many=True)
