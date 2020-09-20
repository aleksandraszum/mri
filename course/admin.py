from django.contrib import admin

# Register your models here.
from course.models import Lesson, LessonContent, Quiz, LessonComplete, LessonProgress

admin.site.register(Lesson)
admin.site.register(LessonContent)
admin.site.register(Quiz)
admin.site.register(LessonProgress)
admin.site.register(LessonComplete)
