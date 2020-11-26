from collections import namedtuple
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics

from socket_handler.permissions import IsValidGameServer, IsValidServer
from .serializers import *
from .permissions import IsNewUser, IsUserTokenBelongToUser, IsValidServerORTokenMatches
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from socket_handler.models import *
from socket_handler.serializers import *
from .utils import temp_user_profile_get

NewUser = namedtuple('NewUser', ('user', 'token', 'start_characters', "start_weapons_first_slot", "start_weapons_second_slot"))
WeaponAddon = namedtuple('WeaponAddon', ('weapon', 'stock', 'barrel', 'muzzle', 'mag', 'scope', 'grip'))


@api_view(['POST', ])
@permission_classes([AllowAny])
def login(request, ):
	"""
	Function to login user with username and password. After successful user and password match, deletes old User token
	and creates new Token. User state activates.

	:return json containing user id and user new token
	"""
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
	"""
	Function to logout user. While log out user token is deprecated

	:return 200 OK
	"""
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
		first_name = request.data.get('first_name',)
		last_name = request.data.get('last_name', '')
		email = request.data.get('email', False)
		password = request.data.get('password', False)

		try:
			user = User.objects.get(username=username)
		except ObjectDoesNotExist:
			user = User.objects.create_user(
				username=username,
				first_name=first_name,
				last_name=last_name,
				email=email,
				password=password,
				last_login=timezone.now(),
				is_staff=False,
				is_active=True,
			)
			if not user.first_name:
				user.first_name = "Player" + str(user.id)
				user.save()
			group = Group.objects.get(name="Players")
			group.user_set.add(user)
			token = Token.objects.get(user=user)
			new_user = NewUser(
				user=user,
				token=token,
				start_characters=Character.objects.filter(default=True, hidden=False),
				start_weapons_first_slot=Weapon.objects.filter(start=True, hidden=False, slot=0),
				start_weapons_second_slot=Weapon.objects.filter(start=True, hidden=False, slot=1),
			)
			response = NewUserSerializer(new_user, context={'request': request})
			return Response(response.data, status=status.HTTP_201_CREATED)
		else:
			response = {
				'detail': "username already taken"
			}
			return Response(data=response, status=status.HTTP_409_CONFLICT)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def set_default_character(request, pk):
	"""
	Function to set default character that user has chosen

	:param pk - id of the character
	:return 200 OK
	"""
	character = Character.objects.filter(default=True, pk=pk)
	if not character:
		return Response(data={"detail": "Character doesn't exists or its not default"}, status=status.HTTP_404_NOT_FOUND)
	else:
		try:
			UserCharacter.objects.create(
				profile=request.user.profile,
				character=character.first(),
			)
		except IntegrityError:
			return Response(data={"detail": "User already has this character"}, status=status.HTTP_400_BAD_REQUEST)
		return Response(data={"detail": "Successfully added character to user"}, status=status.HTTP_200_OK)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def set_default_weapon(request, pk):
	"""
	Function to set start weapon that user has chosen

	:param pk - id of the weapon
	:return 200 OK
	"""
	weapon = Weapon.objects.filter(pk=pk, start=True)
	if not weapon:
		return Response(data={"detail": "Weapon is not start weapon or not found"}, status=status.HTTP_404_NOT_FOUND)
	else:
		if not UserWeapon.objects.filter(profile=request.user.profile, weapon_with_addons__weapon__slot=weapon.first().slot, weapon_with_addons__weapon__start=True):
			UserWeapon.objects.create(
				profile=request.user.profile,
				weapon_with_addons=WeaponAddons.objects.get(weapon=weapon.first()),
			)
			return Response(data={"detail": "Successfully added weapon to user"}, status=status.HTTP_200_OK)
		else:
			return Response(data={"detail": "Slot not empty"}, status=status.HTTP_400_BAD_REQUEST)


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
	permission_classes = (IsValidServerORTokenMatches, )
	lookup_field = u'pk'

	def get_queryset(self):
		return User.objects.filter(is_active=True)

	def get(self, request, *args, **kwargs):
		response = temp_user_profile_get(self.get_object())
		return Response(data=response, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		user = self.get_object()
		if request.user is user:
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
			response = temp_user_profile_get(user)
			return Response(data=response, status=status.HTTP_200_OK)
		else:
			response = temp_user_profile_get(self.get_object())
			return Response(data=response)

	def destroy(self, request, *args, **kwargs):
		user = self.get_object()
		if request.user is user:
			user.is_active = False
			user.save()
			response = {
				'detail': 'User moved to non active, your data still remains'
			}
			return Response(data=response, status=status.HTTP_200_OK)
		else:
			return Response(data={"detail": "You are not allowed to change details"})


@api_view(['GET', ])
@permission_classes([IsValidServerORTokenMatches, ])
def get_main_character(request, pk):
	main = UserCharacter.objects.filter(profile=User.objects.get(pk=pk).profile, main=True)[0]
	response = UserCharacterSerializer(main, context={"request": request})
	return Response(response.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
	"""
	Returns a list containing either all character or only user character if specified with `user_only` param. User is
	identified by token used for this request

	:param user_only - boolean flag (1 - True, otherwise always False) to get characters of User or all characters
	:param order - order of returned list, you can use `date_created`, `tech_name`, or any other param.
	Use `-` before param (`-date_joined`) to get DESC order

	:return json containing characters
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

	def list(self, request, *args, **kwargs):
		CharacterTuple = namedtuple('CharacterTuple', ('characters',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = CharacterUnrealSerializer(CharacterTuple(characters=page))
			return self.get_paginated_response(response.data)
		response = CharacterUnrealSerializer(CharacterTuple(characters=self.get_queryset()))
		return Response(response.data)


class CharacterView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Get or delete character from user, depending on requests's method used. User is identified by token used in request.

	use **GET** - to get info about character
	use **DELETE** - to removed from user characters
	"""
	serializer_class = CharacterSerializer
	queryset = Character.objects.filter(hidden=False)
	lookup_field = "pk"

	def update(self, request, *args, **kwargs):
		response = dict()
		character = self.get_object()
		user_character = UserCharacter.objects.get(profile=request.user.profile, character=character)
		if user_character:
			user_character.main = True
			user_character.save()
			response['detail'] = "Successfully made main character"
			response_status = status.HTTP_200_OK
		else:
			response['detail'] = "Character given not found in user characters"
			response_status = status.HTTP_404_NOT_FOUND
		return Response(data=response, status=response_status)

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
	"""
	Function to add character specified by id to user, user identified by token used

	:param request - request object
	:param pk - id of character, which is adding to the user
	:return 200 OK
	"""
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


@api_view(['GET', ])
@permission_classes([IsValidServerORTokenMatches, ])
def get_main_weapon(request, pk):
	main = UserWeapon.objects.filter(profile=User.objects.get(pk=pk).profile, main=True)[0]
	response = UserWeaponSerializer(main, context={"request": request})
	return Response(response.data, status=status.HTTP_200_OK)


class WeaponListView(generics.ListAPIView):
	"""
	Returns a list containing either all weapons or only user weapon if specified with `user_only` param. User is
	identified by token used for this request

	:param user_only - boolean flag (1 - True, otherwise always False) to get weapons of User or all weapons
	:param slot - specifies a slot type to return, 0 - primary, 1 - secondary
	:param order - order of returned list, you can use `date_created`, `tech_name`, or any other param.
	Use `-` before param (`-date_joined`) to get DESC order

	:return json containing weapons
	"""
	serializer_class = WeaponSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		user_only = self.request.query_params.get('user_only', False)
		slot = self.request.query_params.get('slot', False)
		order = self.request.query_params.get('order', '-date_created')

		if self.request.user and user_only == "1":
			user_weapon = UserWeapon.objects.filter(profile=self.request.user.profile).values_list('weapon_with_addons__weapon', flat=True)
			query = Weapon.objects.filter(pk__in=user_weapon, hidden=False)
		else:
			query = Weapon.objects.filter(hidden=False)

		if slot:
			query = query.filter(slot=int(slot))

		return query.order_by(order)

	def list(self, request, *args, **kwargs):
		WeaponTuple = namedtuple('WeaponTuple', ('weapons',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = WeaponUnrealSeializer(WeaponTuple(weapons=page))
			return self.get_paginated_response(response.data)
		response = WeaponUnrealSeializer(WeaponTuple(weapons=self.get_queryset()))
		return Response(response.data)


class WeaponView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Get or delete weapon with addons from user, depending on requests's method used. User is identified by token used
	in request.

	use **GET** - to get info about weapon
	use **DELETE** - to removed from user weapon
	"""
	serializer_class = WeaponAddonSerializer
	queryset = Weapon.objects.filter(hidden=False)
	lookup_field = "pk"

	def get(self, request, *args, **kwargs):
		user_only = self.request.query_params.get('user_only', False)
		weapon = self.get_object()
		weapon_with_addons = WeaponAddons.objects.get(weapon=weapon)
		if request.user and user_only == "1":
			profile = Profile.objects.get(user=request.user)
			user_weapon = UserWeapon.objects.get(profile=profile, weapon_with_addons=weapon_with_addons)
			response = UserWeaponSerializer(user_weapon, context={"request": request})
		else:
			serializer = WeaponAddon(
				weapon=weapon,
				stock=weapon_with_addons.stock.filter(hidden=False),
				barrel=weapon_with_addons.barrel.filter(hidden=False),
				muzzle=weapon_with_addons.muzzle.filter(hidden=False),
				mag=weapon_with_addons.mag.filter(hidden=False),
				scope=weapon_with_addons.scope.filter(hidden=False),
				grip=weapon_with_addons.grip.filter(hidden=False),
			)
			response = WeaponAddonSerializer(serializer, context={"request": request})
		return Response(response.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		profile = Profile.objects.get(user=request.user)
		weapon_with_addons = WeaponAddons.objects.get(weapon=self.get_object())
		try:
			user_weapon = UserWeapon.objects.get(profile=profile, weapon_with_addons=weapon_with_addons)
		except ObjectDoesNotExist:
			response = {"detail": "User does not have such weapon"}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
		else:
			stock = request.data.get('stock', False)
			barrel = request.data.get('barrel', False)
			muzzle = request.data.get('muzzle', False)
			mag = request.data.get('mag', False)
			grip = request.data.get('grip', False)
			scope = request.data.get('scope', False)

			user_weapon.user_addon_stock.append(stock)
			user_weapon.user_addon_barrel.append(barrel)
			user_weapon.user_addon_muzzle.append(muzzle)
			user_weapon.user_addon_mag.append(mag)
			user_weapon.user_addon_grip.append(grip)
			user_weapon.user_addon_scope.append(scope)

			user_weapon.save()
			response = UserWeaponSerializer(user_weapon, context={"request": request})
			return Response(response.data, status=status.HTTP_202_ACCEPTED)

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
	"""
	Function to add weapon specified by id to user, user identified by token used

	:param request - request object
	:param pk - id of weapon, which is adding to the user
	:return 200 OK
	"""
	response = dict()
	profile = Profile.objects.get(user=request.user)
	weapon = Weapon.objects.get(pk=pk)
	user_weapon = UserWeapon.objects.filter(profile=profile, weapon_with_addons__weapon=weapon)
	if user_weapon:
		response['detail'] = "Weapon given already belongs to user"
		response_status = status.HTTP_400_BAD_REQUEST
	else:
		weapon_with_addons = WeaponAddons.objects.get(weapon=weapon)
		UserWeapon.objects.create(
			profile=profile,
			weapon_with_addons=weapon_with_addons,
		).save()
		response['detail'] = "Successfully added to user weapons"
		response_status = status.HTTP_200_OK
	return Response(data=response, status=response_status)


class UsersList(generics.ListAPIView):
	"""
	Returns a list containing all active user's

	:param user_only - boolean flag (1 - True, otherwise always False) to get list of friends of the User
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
		user_only = self.request.query_params.get('user_only', False)

		if self.request.user and user_only == "1":
			friends = FriendsList.objects.filter(profile__user=self.request.user).values_list('friend', flat=True)
			query = User.objects.filter(is_active=True, is_staff=False, profile__in=friends).order_by(order)
		else:
			query = User.objects.filter(is_active=True, is_staff=False).order_by(order)
		return query

	def list(self, request, *args, **kwargs):
		UserTuple = namedtuple('UserTuple', ('users',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = UserUnrealSerializer(UserTuple(users=page))
			return self.get_paginated_response(response.data)
		response = UserUnrealSerializer(UserTuple(users=self.get_queryset()))
		return Response(response.data)


class UserSearchView(generics.ListAPIView):
	"""
	Returns a list containing active non-staff user's matched given query

	:param query - the string for searching in user names
	:param user_only - boolean flag (1 - True, otherwise always False) to search in list of friends of the User
	:param order - order of returned list, you can use `date_joined`, `username`, `last_login` or any other param.
	Use `-` before param (`-date_joined`) to get DESC order
	:param limit - limit list results to certain number (optional) if not used whole list will be returned
	:param offset - you can use it skip some number of results you already used. (optional)
	:return json containing list of users
	"""
	serializer_class = UserListSerializer
	pagination_class = LimitOffsetPagination
	permission_classes = [IsAuthenticated, IsValidGameServer]

	def get_queryset(self):
		order = self.request.query_params.get('order', '-date_joined')
		user_only = int(self.request.query_params.get('user_only', False))
		query = self.request.query_params.get(u'query')
		if self.request.user and user_only == 1:
			friends_list = FriendsList.objects.filter(profile__user=self.request.user, friend__user__first_name__contains=query).values_list('friend', flat=True)
			return User.objects.filter(is_active=True, is_staff=False, profile__in=friends_list).order_by(order)
		else:
			return User.objects.filter(first_name__contains=query, is_active=True, is_staff=False).order_by(order)

	def list(self, request, *args, **kwargs):
		UserTuple = namedtuple('UserTuple', ('users',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = UserUnrealSerializer(UserTuple(users=page))
			return self.get_paginated_response(response.data)
		response = UserUnrealSerializer(UserTuple(users=self.get_queryset()))
		return Response(response.data)


class UserConfigView(generics.ListCreateAPIView):
	"""
	Get list of your weapons configs or make create one

	use **GET** for list of configs
	use **POST** for creating user config, send json containing ids of weapon, stock, barrel, muzzle, mag, grip, scope
	"""
	serializer_class = UserWeaponConfigSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		order = self.request.query_params.get('order', '-date_created')
		slot = self.request.query_params.get('slot', False)
		query = UserWeaponConfig.objects.filter(weapon__profile__user=self.request.user)
		if slot:
			query = query.filter(weapon__weapon_with_addons__weapon__slot=int(slot))
		return query.order_by(order)

	def post(self, request, *args, **kwargs):
		character = request.data.get('character', None)
		current = request.data.get("current", None)
		weapon = request.data.get('weapon', None)
		stock = request.data.get('stock', None)
		barrel = request.data.get('barrel', None)
		muzzle = request.data.get('muzzle', None)
		mag = request.data.get('mag', None)
		grip = request.data.get('grip', None)
		scope = request.data.get('scope', None)

		try:
			user_weapon = UserWeapon.objects.get(profile=request.user.profile, weapon_with_addons=WeaponAddons.objects.get(weapon=weapon))
		except UserWeapon.DoesNotExist:
			return Response({"detail": "User does not have such weapon"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			config, created = UserWeaponConfig.objects.get_or_create(
				profile=request.user.profile,
				weapon=user_weapon,
				slot=user_weapon.weapon_with_addons.weapon.slot,
				character=Character.objects.get(pk=character),
			)
			if created:
				config.stock = Stock.objects.get(pk=stock) if stock else None
				config.grip = Grip.objects.get(pk=grip) if grip else None
				config.barrel = Barrel.objects.get(pk=barrel) if barrel else None
				config.mag = Mag.objects.get(pk=mag) if mag else None
				config.muzzle = Muzzle.objects.get(pk=muzzle) if muzzle else None
				config.scope = Scope.objects.get(pk=scope) if scope else None
				config.current = current if current is not None else False
				config.save()
			response = UserWeaponConfigSerializer(config, context={"request": request})
			return Response(response.data, status=status.HTTP_202_ACCEPTED)

	def list(self, request, *args, **kwargs):
		ConfigTuple = namedtuple('ConfigTuple', ('configs',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = UserWeaponConfigUnrealSerializer(ConfigTuple(configs=page))
			return self.get_paginated_response(response.data)
		response = UserWeaponConfigUnrealSerializer(ConfigTuple(configs=self.get_queryset()))
		return Response(response.data)


class UserConfigUpdateView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Get, update, delete user weapon config, depending on request's method used. Config is identified by configs
	id passed.
	use **GET** - to get info about config
	use **PUT** - to update config field
	use **DELETE** - to delete config

	:param order - order of returned list, you can use `date_created`
	:return json containing user weapon config information
	"""
	serializer_class = UserWeaponConfigSerializer
	queryset = UserWeaponConfig.objects.all()
	lookup_field = "pk"

	def update(self, request, *args, **kwargs):
		config = self.get_object()
		stock = request.data.get('stock', False)
		barrel = request.data.get('barrel', False)
		muzzle = request.data.get('muzzle', False)
		mag = request.data.get('mag', False)
		grip = request.data.get('grip', False)
		scope = request.data.get('scope', False)
		current = request.data.get('current', None)
		slot = request.data.get('slot', False)

		config.stock = Stock.objects.get(pk=stock) if stock else config.stock
		config.barrel = Barrel.objects.get(pk=barrel) if barrel else config.barrel
		config.muzzle = Muzzle.objects.get(pk=muzzle) if muzzle else config.muzzle
		config.mag = Mag.objects.get(pk=mag) if mag else config.mag
		config.grip = Grip.objects.get(pk=grip) if grip else config.grip
		config.scope = Scope.objects.get(pk=scope) if scope else config.scope
		config.slot = int(slot) if slot else config.slot
		if current is not None:
			config.current = current

		result = config.save()
		if result:
			response = UserWeaponConfigSerializer(config, context={"request": request})
			return Response(response.data, status=status.HTTP_202_ACCEPTED)
		else:
			response = {"detail": "User does not have such addon"}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)

