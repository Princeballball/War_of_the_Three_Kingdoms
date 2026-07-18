from django.urls import path

from . import views


app_name = 'game'

urlpatterns = [
    path('<int:game_id>/', views.detail_view, name='detail'),
    path('<int:game_id>/choose-general/', views.choose_general_view, name='choose_general'),
    path('<int:game_id>/draw/', views.draw_cards_view, name='draw_cards'),
    path('<int:game_id>/end-turn/', views.end_turn_view, name='end_turn'),
    path('<int:game_id>/use-card/', views.use_card_view, name='use_card'),
    path('<int:game_id>/respond/', views.respond_view, name='respond'),
]
