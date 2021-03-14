from django.db import transaction

from rest_framework import (
    permissions,
    status,
    viewsets,
)
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.response import (
    Response,
)

from .models import (
    Answers,
    Questions,
    Quizzes,
)
from .permissions import (
    IsOwnerOrReadOnly,
)
from .serializers import (
    AnswerSerializer,
    QuestionSerializer,
    QuizzesSerializer,
)


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def get_answers_by_user_id(self, request, *args, **kwargs):
        """
        Получает ответы на все вопросы по уникальному идентификатору пользователя
        """
        user_id = request.user.id
        return Response(
            self.serializer_class(
                self.queryset.filter(user_id=user_id),
                many=True,
                context={'request': request},
            ).data,
            status=status.HTTP_200_OK,
        )


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuizzesViewSet(viewsets.ModelViewSet):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'add_question':
            return QuestionSerializer
        elif self.action == 'complete_quiz':
            return AnswerSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    @action(detail=True, methods=['get', 'post'])
    def add_question(self, request, *args, **kwargs):
        """
        Добавляет новый вопрос в опрос
        """
        quiz = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(quiz=quiz)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=True, methods=['get', 'post'])
    def complete_quiz(self, request, *args, **kwargs):
        """
        Прохождение опроса
        """
        quiz = self.get_object()
        questions = quiz.questions.exclude(
            answer__user=request.user,
        )
        serializer = self.get_serializer(data=request.data)
        for question in questions:
            question_ser = QuestionSerializer(
                question,
                context={'request': request},
            )
            if serializer.is_valid():
                serializer.save(question=question, user=request.user)
                return Response(question_ser.data, status=status.HTTP_201_CREATED)
            return Response(question_ser.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def get_all_active_quizzes(self, request, *args, **kwargs):
        """
        Показывает все активные опросы
        """
        queryset = self.queryset.filter(active=True)
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={'request': request},
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
