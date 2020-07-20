from django.urls import path

from socket_handler import views

urlpatterns = [
	path('connect/', views.ConnectUser.as_view()),

	# Friend
	path('friend/request/', views.FriendNotificationView.as_view()),
	path('friend/add/', views.confirm_friendship),
	path('friend/remove/', views.remove_friend),
]
