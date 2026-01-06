from django.urls import path
from .views import save_result, user_results, leaderboard

urlpatterns = [
    path("save/", save_result),
    path("user/<int:user_id>/", user_results),
    path("leaderboard/<int:quiz_id>/", leaderboard),
]
