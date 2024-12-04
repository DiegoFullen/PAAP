from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.list_users, name='user-list'),
    path('users/create/', views.create_user, name='user-create'),
    path('users/<str:email>/edit/', views.edit_user, name='user-edit'),
    path('users/<str:email>/delete/', views.delete_user, name='user-delete'),
]
