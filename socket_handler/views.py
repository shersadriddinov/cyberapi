from v1.models import *
from socket_handler.models import *
from socket_handler.serializers import *
from socket_handler.permissions import *
from socket_handler.utils import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class NotificationView(generics.ListAPIView):
	"""
	Returns a list containing all active notifications. Use it after every connection to web socket, and each time
	socket sends notification
	```json
	{"action": "notification"}
	```

	:return json containing list of notifications
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
	Get list of your friend requests or make friend request

	use **GET** for list of friend requests
	use **POST** to create friend request by specifying friend's user id
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = NotificationSerializer

	def get_queryset(self):
		return Notification.objects.filter(user=self.request.user, notif_type=1, status=True)

	def create(self, request, *args, **kwargs):
		response = dict()
		friend = User.objects.get(pk=request.data.get('friend'))
		if friend:
			friendship = FriendsList.objects.filter(profile__user=request.user, friend__user=friend)
			if not friendship:
				friendship_notif, created = Notification.objects.get_or_create(
					user=friend,
					notif_type=1,
					friend_id=request.user,
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
	Function to confirm friend request

	:param request - user request object
	:param pk - friend's user id
	:param confirm - boolean (1 - True, 0 -False) to add friend or ignore
	:return json containing result (added or already in your friend list)
	"""
	response = dict()
	friend = Profile.objects.get(user=pk)
	notification = Notification.objects.get(user=request.user, notif_type=1, friend_id=pk)
	notification.status = False
	notification.save()
	if int(request.GET.get("confirm", False)) == 1:
		result = FriendsList.add_friend(Profile.objects.get(user=request.user), friend) if friend else False
		if result:
			send_to_socket({"action": "friend_request_confirm", "friend": request.user.id, "uuid": friend.id})
			response['detail'] = "User added to friends list"
			response_status = status.HTTP_201_CREATED
		else:
			response['detail'] = "User already in friends list"
			response_status = status.HTTP_409_CONFLICT
	else:
		response['detail'] = "Friend Request ignored"
		response_status = status.HTTP_200_OK
	return Response(data=response, status=response_status)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def remove_friend(request, pk):
	"""
	Function to remove someone from your friend list

	:param request - user request object
	:param pk - friend's user id
	:return json containing result (removed or not found in your list)
	"""
	response = dict()
	friend = Profile.objects.get(user=pk)
	result = FriendsList.remove_friend(Profile.objects.get(user=request.user), friend) if friend else False
	if result:
		response['detail'] = "User removed from friends list"
		response_status = status.HTTP_201_CREATED
	else:
		response['detail'] = "User does not present in friends list"
		response_status = status.HTTP_409_CONFLICT
	return Response(data=response, status=response_status)
