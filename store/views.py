from collections import namedtuple
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
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

	:param premium - boolean, if True returns only premium items, False return ordinary. If not specified, returns all
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
			query = query.filter(premium=bool(premium))
		return query.order_by(order)

	def list(self, request, *args, **kwargs):
		LotTuple = namedtuple('LotTuple', ('lots',))
		response = LotUnrealSerializer(LotTuple(lots=self.get_queryset()))
		return Response(response.data)


class UserLotListView(generics.ListAPIView):
	"""
	Return list of user purchased lots
	:param premium - boolean, if True returns only premium items, False return ordinary. If not specified, returns all
	:param order - order of returned list, you can use `date_created`, `tech_name`, or any other param.
	:return json containing purchased lots
	"""
	pagination_class = LimitOffsetPagination
	serializer_class = UserLotSerializer

	def get_queryset(self):
		premium = self.request.query_params.get("premium", None)
		order = self.request.query_params.get("order", "-date_created")
		query = UserLots.objects.filter(status=True)
		if premium is not None:
			query = query.filter(premium=bool(premium))
		return query.order_by(order)

	def list(self, request, *args, **kwargs):
		UserLotTuple = namedtuple('UserLotTuple', ('lots',))
		response = LotUnrealSerializer(UserLotTuple(lots=self.get_queryset()))
		return Response(response.data)


class SearchLotView(generics.ListAPIView):
	"""
	Returns a list of lots matched by given query
	:param query - the string for searching in user names
	:param premium - boolean, if True returns only premium items, False return ordinary. If not specified, returns all
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
		search_filter.add(Q(character__tech_name__contains=search_query), Q.AND) if character else False
		search_filter.add(Q(weapon__tech_name__contains=search_query), Q.AND) if weapon else False
		search_filter.add(Q(stock__tech_name__contains=search_query), Q.AND) if stock else False
		search_filter.add(Q(barrel__tech_name__contains=search_query), Q.AND) if barrel else False
		search_filter.add(Q(muzzle__tech_name__contains=search_query), Q.AND) if muzzle else False
		search_filter.add(Q(mag__tech_name__contains=search_query), Q.AND) if mag else False
		search_filter.add(Q(grip__tech_name__contains=search_query), Q.AND) if grip else False
		search_filter.add(Q(scope__tech_name__contains=search_query), Q.AND) if scope else False
		search_filter.add(Q(premium=bool(premium)), Q.AND) if premium is not None else False
		return Lot.objects.filter(search_filter).order_by(order)

	def list(self, request, *args, **kwargs):
		LotTuple = namedtuple('LotTuple', ('lots',))
		response = LotUnrealSerializer(LotTuple(lots=self.get_queryset()))
		return Response(response.data)


class LotView(generics.RetrieveAPIView):
	"""

	"""
	pass


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def purchase(request, pk):
	"""

	"""
	pass
