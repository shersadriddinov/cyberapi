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
			"host_address", "port", "init_user",
			"token", "game_type", "status",
			"server_type", "date_created"
		)


class ServerUnrealSerializer(serializers.ModelSerializer):
	servers = ServerSerializer(many=True)
