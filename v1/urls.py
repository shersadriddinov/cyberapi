from django.urls import path

from . import views

urlpatterns = [
	# User
	path('auth/', views.Auth.as_view()),
	path('login/', views.login),
	path('logout/', views.logout),
	path('user/setchar/<int:pk>/', views.set_default_character),
	path('user/setweap/<int:pk>/', views.set_default_weapon),
	path('user/<int:pk>/', views.UserProfile.as_view()),
	path('user/list/', views.UsersList.as_view()),
	path('user/search/', views.UserSearchView.as_view()),
	path('user/config/list/', views.UserConfigView.as_view()),
	path('user/config/<int:pk>/', views.UserConfigUpdateView.as_view()),

	# Character
	path('character/main/<int:pk>/', views.get_main_character),
	path('character/list/', views.CharacterListView.as_view()),
	path('character/<int:pk>/', views.CharacterView.as_view()),
	path('character/<int:pk>/add', views.add_character_to_user),

	# Weapon
	path('weapon/main/<int:pk>/', views.get_main_weapon),
	path('weapon/list/', views.WeaponListView.as_view()),
	path('weapon/<int:pk>/', views.WeaponView.as_view()),
	path('weapon/<int:pk>/add', views.add_weapon_to_user),
]
