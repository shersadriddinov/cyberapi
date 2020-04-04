from collections import namedtuple
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from .serializers import *
from .permissions import IsNewUser, IsUserTokenBelongToUser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


NewUser = namedtuple(u'NewUser', (u'user', u'token'))


@api_view(['POST', ])
@permission_classes([AllowAny])
def login(request, ):
	username = request.data.get('username', False)
	password = request.data.get('password', False)

	if username and password:
		try:
			user = User.objects.get(username=username)
		except:
			return Response(data={'detail': "User not found"}, status=status.HTTP_404_NOT_FOUND)
		else:
			if check_password(password, user.password):
				try:
					Token.objects.get(user=user).delete()
				except:
					pass
				token = Token.objects.create(user=user)
				token.save()
				response = {
					'id': user.id,
					'token': token.key,
				}
				return Response(data=response, status=status.HTTP_200_OK)
			else:
				return Response(data={'detail': "Username or password didn't match"}, status=status.HTTP_404_NOT_FOUND)

	else:
		return Response(data={'detail': "Provide username and password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def logout(request, ):
	pk = request.GET.get('user', False)
	user = User.objects.get(pk=pk) if pk else False
	if user:
		Token.objects.get(user=user).delete()
		return Response(data={"detail": "You are logged out succesfully"}, status=status.HTTP_200_OK)
	else:
		return Response(data={"detail": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)


class Auth(generics.CreateAPIView):
	"""
	Create new :model:`User` instance, makes sure that user does not exist already in database
	:param username
	:param first_name (optional)
	:param last_name (optional)
	:param email
	:param password
	:return json with GeneralUserSerializer objects (id, username, email)
	"""
	serializer_class = GeneralUserSerializer()
	permission_classes = (IsNewUser, )

	def post(self, request, *args, **kwargs):
		username = request.data.get('username', False)
		first_name = request.data.get('first_name', '')
		last_name = request.data.get('last_name', '')
		email = request.data.get('email', False)
		password = request.data.get('password', False)

		try:
			user = User.objects.get(username=username)
		except ObjectDoesNotExist:
			user = User.objects.create(
				username=username,
				first_name=first_name,
				last_name=last_name,
				email=email,
				password=password,
				last_login=timezone.now(),
				is_staff=False,
				is_active=True,
			)
			group = Group.objects.get(pk=1)  # Gamers group id = 1
			group.user_set.add(user)
			token = Token.objects.get(user=user)
			new_user = NewUser(user=user, token=token)
			response = NewUserSerializer(new_user, context={'request': request})
			return Response(response.data, status=status.HTTP_201_CREATED)
		else:
			response = {
				'detail': "username already taken"
			}
			return Response(data=response, status=status.HTTP_409_CONFLICT)


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
	"""
	Get, update, delete user information, depending on requests's method used. User is identified by user id passed.
	You cannot update user's token, balance, donate & karma with this request!
	use **GET** - to get info about user
	use **PUT** - to update one or more fields by passing params to update in json
	use **DELETE** - to delete user

	:param username
	:param first_name (optional)
	:param last_name (optional)
	:param email
	:param password
	:return json containing user information
	"""
	serializer_class = GeneralUserSerializer
	permission_classes = (IsUserTokenBelongToUser, )
	lookup_field = u'pk'

	def get_queryset(self):
		return User.objects.filter(is_active=True)

	def update(self, request, *args, **kwargs):
		user = self.get_object()
		username = request.data.get('username', False)
		first_name = request.data.get('first_name', False)
		email = request.data.get('email', False)
		client_settings_json = request.data.get('client_settings_json', False)

		user.username = username if username else user.username
		user.first_name = first_name if first_name else user.first_name
		user.email = email if email else user.email
		user.profile.client_settings_json = client_settings_json if client_settings_json else user.profile.client_settings_json
		user.save()

		response = GeneralUserSerializer(user, context={"request": request})
		return Response(response.data, status=status.HTTP_202_ACCEPTED)


class UsersList(generics.ListAPIView):
	"""
	Returns a list containing all active user's
	:param order - order of returned list, you can use `date_joined`, `username`, `last_login` or any other param.
	Use `-` before param (`-date_joined`) to get DESC order
	:param limit - limit list results to certain number (optional) if not used whole list will be returned
	:param offset - you can use it skip some number of results you already used. (optional)
	:return json containing list of users
	"""
	serializer_class = UserListSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		order = self.request.query_params.get('order', '-date_joined')
		return User.objects.filter(is_active=True, is_staff=False).order_by(order)
