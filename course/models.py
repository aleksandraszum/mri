from django.contrib.auth.models import User
from django.db import models


class Lesson(models.Model):
    number_of_lesson = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=50)
    css = models.TextField(null=True)
    js = models.TextField(null=True)

    def __str__(self):
        return f"{self.title}"


class LessonContent(models.Model):
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    part_of_the_lesson = models.PositiveIntegerField()
    content = models.TextField()

    def __str__(self):
        return f" {self.lesson_id} - Part of the Lesson: {self.part_of_the_lesson}"


class Quiz(models.Model):
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    ask = models.CharField(max_length=200)
    answer_1 = models.CharField(max_length=200)
    answer_2 = models.CharField(max_length=200)
    answer_3 = models.CharField(max_length=200)
    answer_4 = models.CharField(max_length=200)
    good_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"Lesson ID: {self.lesson_id} - ask: {self.ask}"


class LessonProgress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    part = models.IntegerField()

    def __str__(self):
        return f"User: {self.user_id} - lesson: {self.lesson_id} - content: {self.part}"


class LessonComplete(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user_id} - lesson: {self.lesson_id}"


