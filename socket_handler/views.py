from collections import namedtuple

from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination

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

	def get_queryset(self):
		return Notification.objects.filter(user=self.request.user, status=True)

	def list(self, request, *args, **kwargs):
		NotificationTuple = namedtuple('NotificationTuple', ('notifications',))
		response = NotificationUnrealSerializer(NotificationTuple(notifications=self.get_queryset()))
		return Response(response.data)


class NotificationDisableView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Get, update, delete user notification, depending on requests's method used. Notification is identified by notification
	id passed.
	use **GET** - to get info about notif
	use **PUT** - to update status of notification
	use **DELETE** - to delete notif

	:param status - boolean True or False
	:return json containing user information
	"""

	serializer_class = NotificationSerializer
	permission_classes = (IsAuthenticated, )
	lookup_field = "pk"
	queryset = Notification.objects.filter(status=True)

	def update(self, request, *args, **kwargs):
		notif = self.get_object()
		notif_status = bool(request.data.get('status', True))

		notif.status = notif_status
		notif.save()

		response = NotificationSerializer(notif, context={"request": request})
		return Response(response.data, status=status.HTTP_202_ACCEPTED)


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

	def list(self, request, *args, **kwargs):
		FriendRequestTuple = namedtuple('FriendRequestTuple', ('notifications',))
		response = NotificationUnrealSerializer(FriendRequestTuple(notifications=self.get_queryset()))
		return Response(response.data)

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


class ServerListView(generics.ListCreateAPIView):
	"""
	Get list of game servers or create one

	use **GET** for list of servers
	use **POST** for creating server, send json containing user, host, port, status, game type, server type
	:param order - order of returned list, you can use `date_created`
	:param server_type - 0 - public, 1 - private
	:param game_type - 0 - casual
	:param status - 0 - Waiting for players, 1 - Game in process, 2 - Game finished, 3 - Ready for close
	:return json containing server information
	"""
	pagination_class = LimitOffsetPagination

	def post(self, request, *args, **kwargs):
		pass

	def get_queryset(self):
		order = self.request.query_params("order", "-date_created")
		server_type = int(self.request.query_params("server_type", 0))
		game_type = self.request.query_params("game_type", False)  # type str
		status = self.request.query_params("status", False)  # type str

		server_filter = Q(server_type=server_type)
		server_filter.add(Q(game_type=int(game_type)), Q.AND) if game_type else False
		server_filter.add(Q(status=int(status)), Q.AND) if status else False

		return Server.objects.filter(server_filter).order_by(order)

	def list(self, request, *args, **kwargs):
		ServerTuple = namedtuple('ServerTuple', ('servers',))
		response = ServerUnrealSerializer(ServerTuple(servers=self.get_queryset()))
		return Response(response.data)


class ServerView(generics.RetrieveUpdateAPIView):
	"""
	Get, update, game server, depending on request's method used. Server is identified by server's
	id passed.
	use **GET** - to get info about server
	use **PUT** - to update server field

	:param order - order of returned list, you can use `date_created`
	:return json containing user weapon config information
	"""
	serializer_class = ServerSerializer
	queryset = Server.objects.all()
	lookup_field = "pk"

	def update(self, request, *args, **kwargs):
		server = self.get_object()
		game_type = self.request.query_params("game_type", False)  # type str
		server_type = int(self.request.query_params("server_type", 0))

		server.game_type = int(game_type) if game_type else False
		server.server_type = server_type if server_type else False
		result = server.save()
		if result:
			response = ServerSerializer(server, context={"request": request})
			return Response(response.data, status=status.HTTP_202_ACCEPTED)
		else:
			response = {"detail": "Can't save server update"}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)
