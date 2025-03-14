from django.urls import path, include
from . import views

from django.urls import re_path
from django.contrib.auth import views as auth_views


app_name="main"


urlpatterns = [
    path('best/', views.LookingBest.as_view(), name="best_page"),
    path('records/', views.LookingRecords.as_view(), name="records_page"),
    path('input_score/', views.InputScore.as_view(), name="input_score_page"),
    re_path(r'^score/(?P<encoded_pk>.+)/$', views.UpdateScore.as_view(), name="score"),




    path('register/', views.register, name='register'),  # ユーザー登録ページ
    path('login/', auth_views.LoginView.as_view(), name='login'),  # ログインページ
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ログアウト
]