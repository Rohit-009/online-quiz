from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_list),
    path("<int:quiz_id>/", views.quiz_detail),
    path("submit/", views.submit_quiz),

    # admin APIs
    path("create/", views.create_quiz),
    path("add-question/", views.add_question),
    path("add-option/", views.add_option),
]
