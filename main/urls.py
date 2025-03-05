from django.urls import path, include
from . import views

from django.urls import re_path

from .views import profile_view

app_name="main"

def custom_logout(request):
    logout(request)
    return redirect('/')

urlpatterns = [
    path('best/', views.LookingBest.as_view(), name="best_page"),
    path('records/', views.LookingRecords.as_view(), name="records_page"),
    path('input_score/', views.InputScore.as_view(), name="input_score_page"),
    re_path(r'^score/(?P<encoded_pk>.+)/$', views.UpdateScore.as_view(), name="score"),
    

    path('accounts/', include('allauth.urls')),
    path('profile/', profile_view, name='profile'),
    path('sync-scores/', views.sync_scores, name='sync_scores'),
]