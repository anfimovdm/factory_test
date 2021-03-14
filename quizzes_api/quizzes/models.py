from django.contrib.auth.models import User
from django.db import models

from .enums import QuestionsTypeEnum


class Quizzes(models.Model):
    begin = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    end = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'quizzes'
        verbose_name = verbose_name_plural = 'Quizzes'


class Questions(models.Model):
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200, blank=True)
    type = models.CharField(
        max_length=50,
        choices=QuestionsTypeEnum.get_choices(),
        default=QuestionsTypeEnum.SINGLE,
    )

    def __str__(self):
        return f'{self.pk}: {self.text}'

    class Meta:
        db_table = 'questions'
        verbose_name = verbose_name_plural = 'Questions'


class Answers(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE, related_name='answer')
    answer = models.CharField(max_length=200, blank=True)
    anonymous = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer

    class Meta:
        db_table = 'answers'
        verbose_name = verbose_name_plural = 'Answers'
