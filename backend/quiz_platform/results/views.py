from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Max

from .models import Result
from quizzes.models import Quiz


# -----------------------------
# 1) SAVE RESULT
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_result(request):
    user = request.user
    quiz_id = request.data.get("quiz_id")
    score = request.data.get("score")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    result = Result.objects.create(
        user=user,
        quiz=quiz,
        score=score
    )

    return Response({
        "message": "Result saved",
        "result_id": result.id
    })


# -----------------------------
# 2) USER RESULT HISTORY
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_results(request, user_id):
    results = Result.objects.filter(user_id=user_id).order_by("-created_at")

    data = []

    for r in results:
        total_questions = r.quiz.questions.count()
        percentage = round((r.score / total_questions) * 100, 2) if total_questions else 0

        data.append({
            "quiz": r.quiz.title,
    "quiz_id": r.quiz.id,
    "score": r.score,
    "percentage": percentage,
    "date": r.created_at,
        })

    return Response(data)


# -----------------------------
# 3) LEADERBOARD (top scores)
# -----------------------------
@api_view(['GET'])
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    top_scores = (
        Result.objects
        .filter(quiz=quiz)
        .values("user__username")
        .annotate(best_score=Max("score"))
        .order_by("-best_score")[:10]
    )

    data = []

    for r in top_scores:
        data.append({
            "username": r["user__username"],
            "score": r["best_score"],
        })

    return Response({
        "quiz": quiz.title,
        "leaderboard": data
    })
