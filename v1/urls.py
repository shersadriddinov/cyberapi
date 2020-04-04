from django.urls import path

from . import views

urlpatterns = [
	# User
	path('auth/', views.Auth.as_view()),
	path('login/', views.login),
	path('logout/', views.logout),
	path('user/<int:pk>/', views.UserProfile.as_view()),
	path('user/list/', views.UsersList.as_view()),
]
