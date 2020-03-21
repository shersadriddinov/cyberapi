from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status


def ok(requset):
	return HttpResponse('ok')
