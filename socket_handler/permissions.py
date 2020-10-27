from django.contrib.auth.hashers import check_password
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from cyberAPI.settings import DEFAULT_SERVER_PROFILE
from socket_handler.models import Server


class IsValidUser(BasePermission):
	def has_permission(self, request, view):
		uuid = request.query_params.get("uuid", False)
		token = request.query_params.get("token", False)

		if uuid and token:
			try:
				user = User.objects.get(pk=uuid)
			except:
				return False
			else:
				real_token = Token.objects.get(user=user)
				if real_token.key == token:
					request.connected_user = user
					return True


class IsValidServer(BasePermission):
	def has_permission(self, request, view):
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


class IsValidGameServer(BasePermission):
	def has_permission(self, request, view):
		token = request.data.get("token", False)
		try:
			Server.objects.get(token=token)
		except Server.DoesNotExist:
			return False
		else:
			return True
