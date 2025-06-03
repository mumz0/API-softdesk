"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from projects.views import ProjectCommentAPIView, ProjectAPIView, ProjectContributorsView, ProjectIssueAPIView
from users.views import UserAPIView, CreateUserAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def redirect_to_token(request):
    """Redirige vers l'endpoint de récupération du token JWT"""
    return redirect('token_obtain_pair')

urlpatterns = [
    path('', redirect_to_token, name='home'),
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/users/create/', CreateUserAPIView.as_view(), name='create-user'),
    path('api/users/', UserAPIView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
    
    path('projects/', ProjectAPIView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectAPIView.as_view(), name='project-detail'),
    
    path('projects/<int:project_id>/contributors/', ProjectContributorsView.as_view(), name='project-contributors'),
    path('projects/<int:project_id>/contributors/<int:user_id>/', ProjectContributorsView.as_view(), name='project-contributor'),

    path('projects/<int:project_id>/issues/', ProjectIssueAPIView.as_view(), name='list_create_issues'),
    path('projects/<int:project_id>/issues/<int:issue_id>/', ProjectIssueAPIView.as_view(), name='issue'),
    
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', ProjectCommentAPIView.as_view(), name='comment-list-create'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<uuid:uuid>/', ProjectCommentAPIView.as_view(), name='comment-detail'),
]
