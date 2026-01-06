from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('login/', views.login_page, name="login_page"),
    path('register/', views.register_page, name="register_page"),
    path('home/', views.quiz_list_page, name="quiz_list_page"),
    path('quiz/<int:quiz_id>/', views.quiz_attempt_page, name="quiz_attempt_page"),
    path('result/', views.result_page, name="result_page"),   # ⬅ NEW
]
