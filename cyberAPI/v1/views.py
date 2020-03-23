from collections import namedtuple
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import generics
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


NewUser = namedtuple(u'NewUser', (u'user', u'token'))


class Auth(generics.CreateAPIView):
	"""
	Create new user instance, makes sure that user does not exist already in database
	"""
	serializer_class = GeneralUserSerializer()

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

	"""
	serializer_class = GeneralUserSerializer
	lookup_field = u'pk'

	def get_queryset(self):
		return User.objects.filter(is_active=True)


class UsersList(generics.ListAPIView):
	"""

	"""
	serializer_class = GeneralUserSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		order = self.request.query_params.get('order', '-date_joined')
		return User.objects.filter(is_active=True).order_by(order)
