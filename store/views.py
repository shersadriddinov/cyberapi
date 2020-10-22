from collections import namedtuple
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.db import IntegrityError
from rest_framework import generics
from store.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from v1.models import *


class LotListView(generics.ListAPIView):
	"""
	Returns list of all lots

	:param premium - boolean, if 1 (True) returns only premium items, 0 (False_ return ordinary. If not specified, returns all
	:param order - order of returned list, you can use `date_created`, `tech_name`, or any other param.
	:return json containing requested lots
	"""
	pagination_class = LimitOffsetPagination
	serializer_class = LotSerializer

	def get_queryset(self):
		premium = self.request.query_params.get("premium", None)
		order = self.request.query_params.get("order", "-date_created")
		query = Lot.objects.filter(status=True)
		if premium is not None:
			query = query.filter(premium=bool(int(premium)))
		return query.order_by(order)

	def list(self, request, *args, **kwargs):
		LotTuple = namedtuple('LotTuple', ('lots',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = LotUnrealSerializer(LotTuple(lots=page))
			return self.get_paginated_response(response.data)
		response = LotUnrealSerializer(LotTuple(lots=self.get_queryset()))
		return Response(response.data)


class UserLotListView(generics.ListAPIView):
	"""
	Return list of user purchased lots
	:param premium - boolean, if 1 (True) returns only premium items, 0 (False_ return ordinary. If not specified, returns all
	:return json containing purchased lots
	"""
	pagination_class = LimitOffsetPagination
	serializer_class = UserLotSerializer

	def get_queryset(self):
		premium = self.request.query_params.get("premium", None)
		query = UserLots.objects.filter(user=self.request.user.profile)
		if premium is not None:
			query = query.filter(lot__premium=bool(int(premium)))
		user_lots_ids = query.values_list('lot_id', flat=True)
		return Lot.objects.filter(status=True, pk__in=user_lots_ids)

	def list(self, request, *args, **kwargs):
		UserLotTuple = namedtuple('UserLotTuple', ('lots',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = LotUnrealSerializer(UserLotTuple(lots=page))
			return self.get_paginated_response(response.data)
		response = LotUnrealSerializer(UserLotTuple(lots=self.get_queryset()))
		return Response(response.data)


class SearchLotView(generics.ListAPIView):
	"""
	Returns a list of lots matched by given query
	:param query - the string for searching in user names
	:param premium - boolean, if 1 (True) returns only premium items, 0 (False_ return ordinary. If not specified, returns all
	:param character - for character filter
	:param weapon - for weapon filter
	:param stock - for stock filter
	:param barrel - for barrel filter
	:param muzzle - for muzzle filter
	:param scope - for scope filter
	:param grip - for grip filter
	:param order - order of returned list, you can use `date_joined`, `username`, `last_login` or any other param.
	Use `-` before param (`-date_joined`) to get DESC order
	:return json containing list of users
	"""

	pagination_class = LimitOffsetPagination
	serializer_class = LotSerializer

	def get_queryset(self):
		search_query = self.request.query_params.get("query", False)
		premium = self.request.query_params.get("premium", None)
		character = self.request.query_params.get("character", False)
		weapon = self.request.query_params.get("weapon", False)
		stock = self.request.query_params.get("stock", False)
		barrel = self.request.query_params.get("barrel", False)
		muzzle = self.request.query_params.get("muzzle", False)
		mag = self.request.query_params.get("mag", False)
		grip = self.request.query_params.get("grip", False)
		scope = self.request.query_params.get("scope", False)
		order = self.request.query_params.get("order", "-date_created")

		search_filter = Q(status=True)
		search_filter.add(Q(character__tech_name__contains=search_query), Q.AND) if int(character) else False
		search_filter.add(Q(weapon__tech_name__contains=search_query), Q.AND) if int(weapon) else False
		search_filter.add(Q(stock__tech_name__contains=search_query), Q.AND) if int(stock) else False
		search_filter.add(Q(barrel__tech_name__contains=search_query), Q.AND) if int(barrel) else False
		search_filter.add(Q(muzzle__tech_name__contains=search_query), Q.AND) if int(muzzle) else False
		search_filter.add(Q(mag__tech_name__contains=search_query), Q.AND) if int(mag) else False
		search_filter.add(Q(grip__tech_name__contains=search_query), Q.AND) if int(grip) else False
		search_filter.add(Q(scope__tech_name__contains=search_query), Q.AND) if int(scope) else False
		search_filter.add(Q(premium=bool(int(premium))), Q.AND) if premium is not None else False
		if not (int(character) or int(weapon) or int(stock) or int(barrel) or int(muzzle) or int(mag) or int(grip) or int(scope)):
			search_filter.add(Q(tech_name__contains=search_query), Q.AND)
		print(search_filter)
		return Lot.objects.filter(search_filter).order_by(order)

	def list(self, request, *args, **kwargs):
		LotTuple = namedtuple('LotTuple', ('lots',))
		page = self.paginate_queryset(self.get_queryset())
		if page is not None:
			response = LotUnrealSerializer(LotTuple(lots=page))
			return self.get_paginated_response(response.data)
		response = LotUnrealSerializer(LotTuple(lots=self.get_queryset()))
		return Response(response.data)


class LotView(generics.RetrieveAPIView):
	"""
	Returns information about single lot specified in pk
	"""
	serializer_class = LotSerializer
	queryset = Lot.objects.filter(status=True)
	lookup_field = 'pk'


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def purchase(request, pk):
	"""
	Function to purchase lots, accepts only POST requests, takes lot id as pk and adds it to user, which was authenticated

	:param pk - lot id
	:return 200 OK
	"""
	lot = Lot.objects.get(pk=pk)
	user = request.user
	response = {
		'data': {"detail": "Lot has been successfully purchased"},
		'status': status.HTTP_200_OK
	}
	if lot.status:
		if lot.premium and user.profile.donate >= lot.price:
			user.profile.donate -= lot.price
			try:
				UserLots.objects.create(user=user.profile, lot=lot)
			except IntegrityError:
				response['data']['detail'] = "User already purchased this lot"
				response['status'] = status.HTTP_400_BAD_REQUEST
				user.profile.donate += lot.price
			user.profile.save()
		elif not lot.premium and user.profile.balance >= lot.price:
			user.profile.balance -= lot.price
			try:
				UserLots.objects.create(user=user.profile, lot=lot)
			except IntegrityError:
				response['data']['detail'] = "User already purchased this lot"
				response['status'] = status.HTTP_400_BAD_REQUEST
				user.profile.balance += lot.price
			user.profile.save()
		else:
			response['data']['detail'] = "Insufficient funds"
			response['status'] = status.HTTP_400_BAD_REQUEST
	else:
		response['data']['detail'] = 'Lot is unavailable to purchase'
		response['status'] = status.HTTP_400_BAD_REQUEST
	return Response(data=response['data'], status=response['status'])
