from django.urls import path

from . import views

urlpatterns = [
	# User
	path('auth/', views.Auth.as_view()),
	path('login/', views.login),
	path('logout/', views.logout),
	path('user/<int:pk>/', views.UserProfile.as_view()),
	path('user/list/', views.UsersList.as_view()),

	# Character
	path('character/list/', views.CharacterListView.as_view()),
	path('character/<int:pk>/', views.CharacterView.as_view()),
	path('character/<int:pk>/add', views.add_character_to_user),

	# Weapon
	path('weapon/list/', views.WeaponListView.as_view()),
	path('weapon/<int:pk>/', views.WeaponView.as_view()),
	path('weapon/<int:pk>/add', views.add_weapon_to_user),
]
