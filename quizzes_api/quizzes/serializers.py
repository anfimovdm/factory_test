from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers

from .enums import QuestionsTypeEnum
from .models import Quizzes, Questions, Answers


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(choices=QuestionsTypeEnum.get_choices())
    text = serializers.CharField(allow_blank=True)
    quiz = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='quizzes-detail',
    )
    answer = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='answers-detail',
    )

    def create(self, validated_data):
        return Questions.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(allow_blank=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)


class QuizzesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    begin = serializers.DateField()
    description = serializers.CharField(required=False)
    end = serializers.DateField(required=False, allow_null=True)
    name = serializers.CharField(required=False)
    active = serializers.BooleanField(required=False)
    questions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='questions-detail',
    )
    owner = UserSerializer(required=False, read_only=True)

    def create(self, validated_data):
        return Quizzes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.end = validated_data.get('end', instance.end)
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    answer = serializers.CharField(allow_blank=True)
    anonymous = serializers.BooleanField(default=False)
    user = UserSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)

    def create(self, validated_data):
        return Answers.objects.create(**validated_data)
