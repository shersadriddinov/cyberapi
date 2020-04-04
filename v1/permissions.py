from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


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
