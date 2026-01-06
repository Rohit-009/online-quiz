from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Quiz, Question, Option
from .serializers import QuizSerializer
from admin_panel.permissions import IsAdminUser


# ----------------------------
# PUBLIC APIs (Students can use)
# ----------------------------

# List all quizzes
@api_view(['GET'])
def quiz_list(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)


# Get single quiz with questions + options
@api_view(['GET'])
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


# Submit answers & return score
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request):

    user = request.user
    quiz_id = request.data.get("quiz_id")
    answers = request.data.get("answers", {})

    quiz = get_object_or_404(Quiz, id=quiz_id)

    score = 0
    total = quiz.questions.count()

    # check answers
    for question in quiz.questions.all():
        selected_option_id = answers.get(str(question.id))

        if not selected_option_id:
            continue

        option = Option.objects.filter(id=selected_option_id, question=question, is_correct=True).first()

        if option:
            score += 1

    # save result
    from results.models import Result
    Result.objects.create(
        user=user,
        quiz=quiz,
        score=score
    )

    return Response({
        "quiz": quiz.title,
        "score": score,
        "total": total
    })


# ----------------------------
# ADMIN APIs (Protected)
# ----------------------------

# Create quiz
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_quiz(request):
    title = request.data.get("title")
    description = request.data.get("description")

    if not title:
        return Response({"error": "Title is required"}, status=400)

    quiz = Quiz.objects.create(
        title=title,
        description=description
    )

    return Response({"message": "Quiz created", "quiz_id": quiz.id})


# Add question
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_question(request):
    quiz_id = request.data.get("quiz_id")
    text = request.data.get("text")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    question = Question.objects.create(
        quiz=quiz,
        text=text
    )

    return Response({"message": "Question added", "question_id": question.id})


# Add option to question
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_option(request):
    question_id = request.data.get("question_id")
    text = request.data.get("text")
    is_correct = request.data.get("is_correct", False)

    question = get_object_or_404(Question, id=question_id)

    Option.objects.create(
        question=question,
        text=text,
        is_correct=is_correct
    )

    return Response({"message": "Option added"})
