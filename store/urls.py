from django.urls import path

from . import views

urlpatterns = [
	path('lots/', views.LotListView.as_view()),
	path('lots/<int:pk>/', views.LotView.as_view()),
	path('userlots/', views.UserLotListView.as_view()),
	path('search/', views.SearchLotView.as_view()),
	path('purchase/<int:pk>/', views.purchase)
]
