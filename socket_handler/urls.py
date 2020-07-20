from django.urls import path

from socket_handler import views

urlpatterns = [
	path('connect/', views.NotificationView.as_view()),

	# Friend
	path('friend/request/', views.FriendNotificationView.as_view()),
	path('friend/add/<int:pk>/', views.confirm_friendship),
	path('friend/remove/<int:pk>/', views.remove_friend),
]
