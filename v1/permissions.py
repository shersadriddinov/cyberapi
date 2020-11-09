from django.contrib.auth.hashers import check_password
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from cyberAPI.settings import DEFAULT_SERVER_PROFILE


class IsNewUser(BasePermission):
	def has_permission(self, request, view):
		user_key = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
		user = User.objects.get(username='default_user')
		new_user_token = Token.objects.get(user=user)
		if user_key == new_user_token.key:
			return True


class IsUserTokenBelongToUser(BasePermission):
	def has_object_permission(self, request, view, obj):
		user_key = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
		token = Token.objects.get(user=obj)
		if token.key == user_key:
			return True


class IsValidServerORTokenMatches(BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.META.get('HTTP_AUTHORIZATION') is not None:
			user_key = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
			token = Token.objects.get(user=obj)
			if token.key == user_key:
				return True
		else:
			login = request.data.get('login', False)
			password = request.data.get("password", False)
			default = User.objects.get(username=DEFAULT_SERVER_PROFILE)

			try:
				user = User.objects.get(username=login)
			except User.DoesNotExist:
				return False
			else:
				if user.is_staff and user.username == default.username and check_password(password, default.password):
					return True
				else:
					return False
