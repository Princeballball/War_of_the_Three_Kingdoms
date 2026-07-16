from django.urls import path

from . import views


app_name = 'room'

urlpatterns = [
    path('create/', views.create_room_view, name='create'),
    path('join/<int:room_id>/', views.join_public_room_view, name='join_public'),
    path('join-private/', views.join_private_room_view, name='join_private'),
    path('auto-match/', views.auto_match_view, name='auto_match'),
    path('<str:code>/', views.detail_view, name='detail'),
    path('<str:code>/leave/', views.leave_view, name='leave'),
]
