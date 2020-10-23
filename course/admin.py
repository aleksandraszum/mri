from django.contrib import admin

from course.models import Lesson, LessonContent, LessonComplete, LessonProgress, Question, Answer, UserAnswer, Profile

admin.site.register(Lesson)
admin.site.register(LessonContent)
admin.site.register(LessonProgress)
admin.site.register(LessonComplete)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserAnswer)
admin.site.register(Profile)
