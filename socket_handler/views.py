from v1.models import *
from socket_handler.models import *
from socket_handler.serializers import *
from socket_handler.permissions import *
from socket_handler.utils import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class ConnectUser(generics.ListAPIView):
	"""
	#TODO: write clear docs
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = NotificationSerializer

	def get_queryset(self):
		query = Notification.objects.filter(user=self.request.user, status=True)
		for item in query:
			if item.notif_type not in [1, ]:
				item.status = False
				item.save()
		return query


class FriendNotificationView(generics.ListCreateAPIView):
	"""
	#TODO: write clear docs
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = NotificationSerializer

	def get_queryset(self):
		return Notification.objects.filter(profile=self.request.user, type=1, status=True)

	def create(self, request, *args, **kwargs):
		response = dict()
		friend = Profile.objects.get(args[0], False)
		if friend:
			friendship = FriendsList.objects.filter(profile=request.user, friend=friend)
			if not friendship:
				friendship_notif = Notification.objects.get_or_create(
					user=friend,
					notif_type=1,
					friend_id=request.user.id,
				)
				data = {
					"action": "notification",
					"type": 1,
					"uuid": friend.id,
					"friend": request.user.id
				}
				result = send_to_socket(data)
				if result == True:
					response = NotificationSerializer(friendship_notif, context={"request": request})
					return Response(response.data, status=status.HTTP_201_CREATED)
				else:
					response['detail'] = result
					response_status = status.HTTP_417_EXPECTATION_FAILED
					return Response(data=response, status=response_status)
			else:
				response['detail'] = "User is already your friend"
				response_status = status.HTTP_409_CONFLICT
			return Response(data=response, status=response_status)
		else:
			response['detail'] = "Friend not found"
			response_status = status.HTTP_409_CONFLICT
			return Response(data=response, status=response_status)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def confirm_friendship(request, pk):
	"""
	#TODO: write clear docs
	"""
	response = dict()
	friend = Profile.objects.get(pk, False)
	result = FriendsList.add_friend(request.user, friend) if friend else False
	if result:
		send_to_socket({"action": "friend_request_confirm", "friend": request.user, "uuid": friend})
		response['detail'] = "User added to friends list"
		response_status = status.HTTP_201_CREATED
	else:
		response['detail'] = "User already in friends list"
		response_status = status.HTTP_409_CONFLICT
	return Response(data=response, status=response_status)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def remove_friend(request, pk):
	"""
	#TODO: write clear docs
	"""
	response = dict()
	friend = Profile.objects.get(pk, False)
	result = FriendsList.remove_friend(request.user, friend) if friend else False
	if result:
		response['detail'] = "User removed from friends list"
		response_status = status.HTTP_201_CREATED
	else:
		response['detail'] = "User does not present in friends list"
		response_status = status.HTTP_409_CONFLICT
	return Response(data=response, status=response_status)
