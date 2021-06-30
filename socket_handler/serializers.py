from rest_framework import serializers
from socket_handler.models import *


class UserNotifSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("id", "first_name", )


class NotificationSerializer(serializers.ModelSerializer):
	user = UserNotifSerializer()
	friend_id = UserNotifSerializer()

	class Meta:
		model = Notification
		fields = "__all__"


class NotificationUnrealSerializer(serializers.Serializer):
	notifications = NotificationSerializer(many=True)


class ServerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Server
		fields = (
			"id", "host_address", "port", "init_user", "game_type", "status",
			"server_type", "date_created"
		)


class ServerUnrealSerializer(serializers.Serializer):
	servers = ServerSerializer(many=True)


class GameServerSeriazlizer(serializers.ModelSerializer):
	class Meta:
		model = Server
		fields = "__all__"


class InviteSerializer(serializers.ModelSerializer):
	server = ServerSerializer()

	class Meta:
		model = Invite
		fields = "__all__"


class InviteUnrealSerializer(serializers.Serializer):
	invites = InviteSerializer(many=True)


class PlayerStatsSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlayerStatistic
		fields = "__all__"


class PlayerStatsUnrealSerializer(serializers.Serializer):
	stats = PlayerStatsSerializer(many=True)
