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
