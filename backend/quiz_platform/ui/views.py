from django.shortcuts import render

def login_page(request):
    return render(request, "ui/login.html")

def register_page(request):
    return render(request, "ui/register.html")

def quiz_list_page(request):
    return render(request, "ui/quiz_list.html")

def quiz_attempt_page(request, quiz_id):
    return render(request, "ui/quiz_attempt.html", {"quiz_id": quiz_id})

def result_page(request):
    return render(request, "ui/result.html")
