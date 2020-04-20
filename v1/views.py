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


NewUser = namedtuple('NewUser', ('user', 'token'))
WeaponAddon = namedtuple('WeaponAddon', ('weapon', 'addons'))


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
				user.is_active = True
				user.save()
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
		return Response(data={"detail": "You are logged out successfully"}, status=status.HTTP_200_OK)
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
			group = Group.objects.get(name="Players")
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
		password = request.data.get('password', False)

		user.username = username if username else user.username
		user.first_name = first_name if first_name else user.first_name
		user.email = email if email else user.email
		user.profile.client_settings_json = client_settings_json if client_settings_json else user.profile.client_settings_json
		if password:
			user.set_password(password)
		user.save()

		response = GeneralUserSerializer(user, context={"request": request})
		return Response(response.data, status=status.HTTP_202_ACCEPTED)

	def destroy(self, request, *args, **kwargs):
		user = self.get_object()
		user.is_active = False
		user.save()
		response = {
			'detail': 'User moved to non active, your data still remains'
		}
		return Response(data=response, status=status.HTTP_200_OK)


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


class CharacterListView(generics.ListAPIView):
	"""

	"""
	serializer_class = CharacterSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		user_only = int(self.request.query_params.get('user_only', False))
		order = self.request.query_params.get('order', '-date_created')

		if self.request.user and user_only == 1:
			profile = Profile.objects.get(user=self.request.user)
			user_characters = UserCharacter.objects.filter(profile=profile).values_list('character', flat=True)
			query = Character.objects.filter(pk__in=user_characters, hidden=False).order_by(order)
		else:
			query = Character.objects.filter(hidden=False).order_by(order)
		return query


class CharacterView(generics.RetrieveDestroyAPIView):
	"""

	"""
	serializer_class = CharacterSerializer
	queryset = Character.objects.filter(hidden=False)
	lookup_field = "pk"

	def destroy(self, request, *args, **kwargs):
		response = dict()
		profile = Profile.objects.get(user=request.user)
		character = self.get_object()
		user_character = UserCharacter.objects.filter(profile=profile, character=character)
		if user_character:
			user_character.delete()
			response['detail'] = "Successfully removed from user characters"
			response_status = status.HTTP_200_OK
		else:
			response['detail'] = "Character given not found in user characters"
			response_status = status.HTTP_404_NOT_FOUND
		return Response(data=response, status=response_status)


@api_view(["PUT"])
@permission_classes([IsUserTokenBelongToUser])
def add_character_to_user(request, pk):
	response = dict()
	profile = Profile.objects.get(user=request.user)
	character = Character.objects.get(pk=pk)
	user_character = UserCharacter.objects.filter(profile=profile, character=character)
	if user_character:
		response['detail'] = "Character given already belongs to user"
		response_status = status.HTTP_400_BAD_REQUEST
	else:
		UserCharacter.objects.create(profile=profile, character=character).save()
		response['detail'] = "Successfully added to user characters"
		response_status = status.HTTP_200_OK
	return Response(data=response, status=response_status)


class WeaponListView(generics.ListAPIView):
	"""

	"""
	serializer_class = WeaponSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		user_only = int(self.request.query_params.get('user_only', False))
		order = self.request.query_params.get('order', '-date_created')

		if self.request.user and user_only == 1:
			profile = Profile.objects.get(user=self.request.user)
			user_weapon = UserWeapon.objects.filter(profile=profile).values_list('weapon_with_addons', flat=True)
			query = Weapon.objects.filter(pk__in=user_weapon, hidden=False).order_by(order)
		else:
			query = Weapon.objects.filter(hidden=False).order_by(order)
		return query


class WeaponView(generics.RetrieveDestroyAPIView):
	"""

	"""
	serializer_class = WeaponAddonSerializer
	queryset = Weapon.objects.filter(hidden=False)
	lookup_field = "pk"

	def get(self, request, *args, **kwargs):
		weapon = self.get_object()
		weapon_with_addons = WeaponAddons.objects.get(weapon=weapon)
		addons = {
			'stock': Stock.objects.get(pk=weapon_with_addons.stock.id),
			'barrel': Barrel.objects.get(pk=weapon_with_addons.barrel.id),
			'muzzle': Muzzle.objects.get(pk=weapon_with_addons.muzzle.id),
			'mag': Mag.objects.get(pk=weapon_with_addons.mag.id),
			'scope': Stock.objects.get(pk=weapon_with_addons.scope.id),
			'grip': Stock.objects.get(pk=weapon_with_addons.grip.id),
		}
		weapon_with_addons = WeaponAddons(weapon=weapon, addons=addons)
		response = WeaponAddonSerializer(weapon_with_addons, context={"request": request})
		return Response(response.data, status=status.HTTP_200_OK)

	def destroy(self, request, *args, **kwargs):
		response = dict()
		profile = Profile.objects.get(user=request.user)
		weapon = self.get_object()
		user_weapon = UserWeapon.objects.filter(profile=profile, weapon_with_addons__weapon=weapon)
		if user_weapon:
			user_weapon.delete()
			response['detail'] = "Successfully removed from user weapons"
			response_status = status.HTTP_200_OK
		else:
			response['detail'] = "Weapon given not found in user weapons"
			response_status = status.HTTP_404_NOT_FOUND
		return Response(data=response, status=response_status)


@api_view(["PUT"])
@permission_classes([IsUserTokenBelongToUser])
def add_weapon_to_user(request, pk):
	response = dict()
	profile = Profile.objects.get(user=request.user)
	weapon = Weapon.objects.get(pk=pk)
	user_weapon = UserWeapon.objects.filter(profile=profile, weapon_with_addons__weapon=weapon)
	if user_weapon:
		response['detail'] = "Weapon given already belongs to user"
		response_status = status.HTTP_400_BAD_REQUEST
	else:
		weapon_with_addons = WeaponAddons.objects.get(weapon=weapon)
		default_stock_id = weapon_with_addons.stock.filter(default=True).value_list('stock__id', flat=True)
		default_barrel_id = weapon_with_addons.barrel.filter(default=True).value_list('barrel__id', flat=True)
		default_muzzle_id = weapon_with_addons.muzzle.filter(default=True).value_list('muzzle__id', flat=True)
		default_mag_id = weapon_with_addons.mag.filter(default=True).value_list('mag__id', flat=True)
		default_scope_id = weapon_with_addons.scope.filter(default=True).value_list('scope__id', flat=True)
		default_grip_id = weapon_with_addons.grip.filter(default=True).value_list('grip__id', flat=True)
		UserWeapon.objects.create(
			profile=profile,
			weapon_with_addons=weapon_with_addons,
			user_addon_stock=default_stock_id,
			user_addon_barrel=default_barrel_id,
			user_addon_muzzle=default_muzzle_id,
			user_addon_mag=default_mag_id,
			user_addon_scope=default_scope_id,
			user_addon_grip=default_grip_id,
		).save()
		response['detail'] = "Successfully added to user weapons"
		response_status = status.HTTP_200_OK
	return Response(data=response, status=response_status)



