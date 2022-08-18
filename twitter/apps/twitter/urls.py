from django.urls import path

from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('load/tweets/', views.LoadTweetsView.as_view(), name='load_tweets')
]
