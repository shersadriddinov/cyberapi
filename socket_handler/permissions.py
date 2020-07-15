from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


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
