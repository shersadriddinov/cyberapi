from rest_framework import serializers
from socket_handler.models import *


class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notification
		fields = "__all__"
