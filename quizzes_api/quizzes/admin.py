from django.contrib import admin

from .models import Questions, Quizzes, Answers


admin.site.register(Questions)
admin.site.register(Quizzes)
admin.site.register(Answers)
