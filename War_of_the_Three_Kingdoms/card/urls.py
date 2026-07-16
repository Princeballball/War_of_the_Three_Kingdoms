from django.urls import path

from .views import CardLibraryView


app_name = 'card'

urlpatterns = [
    path('', CardLibraryView.as_view(), name='library'),
]
