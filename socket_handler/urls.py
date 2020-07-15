from django.urls import path

from socket_handler import views

urlpatterns = [
	path('connect/', views.ConnectUser.as_view())
]
