from collections import namedtuple
from django.contrib.auth.models import User
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
		premium = self.request.query_params("premium", None)
		order = self.request.query_params("order", "-date_created")
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
		premium = self.request.query_params("premium", None)
		order = self.request.query_params("order", "-date_created")
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

	"""
	pass


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
