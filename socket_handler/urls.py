from django.urls import path

from socket_handler import views

urlpatterns = [
	# Notifications
	path('connect/', views.NotificationView.as_view()),
	path('notif/<int:pk>/', views.NotificationDisableView.as_view()),

	# Friend
	path('friend/request/', views.FriendNotificationView.as_view()),
	path('friend/add/<int:pk>/', views.confirm_friendship),
	path('friend/remove/<int:pk>/', views.remove_friend),

	# Server

]
