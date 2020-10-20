from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class LotSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lot
		fields = ("__all__", )


class LotUnrealSerializer(serializers.Serializer):
	lots = LotSerializer(many=True)


class UserLotSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserLots
		fields = ("lot", "date_purchased")
		depth = 1


class UserLotUnrealSerializer(serializers.Serializer):
	lots = UserLotSerializer(many=True)
