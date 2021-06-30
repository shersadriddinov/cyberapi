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
	path('server/assign/<int:pk>/', views.assign_server),
	path('server/update/', views.update_server_state),
	path('server/list/', views.ServerListView.as_view()),
	path('server/<int:pk>/', views.ServerView.as_view()),

	# Invites
	path('invite/list/', views.InviteListView.as_view()),
	path('invite/<int:pk>/', views.InviteView.as_view()),

	# Game Stats
	path('stats/', views.PlayerStats.as_view()),
	path('stats/update/', views.update_user_stats)
]
