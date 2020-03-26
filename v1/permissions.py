from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class IsNewUser(BasePermission):
	def has_permission(self, request, view):
		user_key = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
		user = User.objects.get(username='default_user')
		new_user_token = Token.objects.get(user=user)
		print(user_key)
		print(new_user_token.key)
		if user_key == new_user_token.key:
			return True
