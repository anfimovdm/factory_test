from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import (
    AnswersViewSet,
    QuestionsViewSet,
    QuizzesViewSet,
)


router = DefaultRouter()
router.register(r'answers', AnswersViewSet)
router.register(r'quizzes', QuizzesViewSet)
router.register(r'questions', QuestionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'openapi',
        get_schema_view(
            title='QuizzesAPI',
            description='API for all things',
            version='1.0',
        ),
        name='openapi-schema',
    ),
    path(
        'swagger-ui/',
        TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={
                'schema_url': 'openapi-schema',
            },
        ),
        name='swagger-ui',
    ),
]
