from v1.models import *
from socket_handler.models import *
from socket_handler.serializers import *
from socket_handler.permissions import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes


class ConnectUser(generics.ListAPIView):
	"""

	"""
	permission_classes = (IsAdminUser, IsValidUser)
	serializer_class = NotificationSerializer

	def get_queryset(self):
		query = Notification.objects.filter(user=self.request.connected_user, status=True)
		for item in query:
			if item.notif_type not in [1, ]:
				item.status = False
				item.save()
		return query
