from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.contrib.auth.views import LogoutView


# API home message (optional)
def home(request):
    return JsonResponse({
        "message": "Online Quiz Platform API is running",
        "endpoints": {
            "register": "/api/accounts/register/",
            "login": "/api/accounts/login/",
            "quizzes": "/api/quizzes/"
        }
    })


urlpatterns = [

    # 🔥 admin logout redirects to UI login page
    path('admin/logout/', LogoutView.as_view(next_page='/login/'), name='admin-logout'),

    # Django admin
    path('admin/', admin.site.urls),

    # APIs
    path('api/accounts/', include('accounts.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/results/', include('results.urls')),

    # UI pages (login, register, quiz pages)
    path('', include('ui.urls')),

    # Optional JSON API root
    path('api/', home),
]
