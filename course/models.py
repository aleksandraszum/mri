from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


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


class LessonProgress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE, default=None)
    part = models.IntegerField(default=None)

    def __str__(self):
        return f"User: {self.user_id} - lesson: {self.lesson_id} - content: {self.part}"


class LessonComplete(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE, default=1)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user_id} - lesson: {self.lesson_id}"


class Question(models.Model):
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    question = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.question}"


class Answer(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer}"


class UserAnswer(models.Model):
    time = models.DateTimeField(default=datetime.now, blank=False)
    question_1_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_1')
    question_2_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_2')
    question_3_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_3')
    question_4_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_4')
    question_5_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_5')
    question_6_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_6')
    question_7_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_7')
    question_8_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_8')

    answer_1_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_1')
    answer_2_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_2')
    answer_3_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_3')
    answer_4_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_4')
    answer_5_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_5')
    answer_6_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_6')
    answer_7_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_7')
    answer_8_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='answer_8')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    result = models.FloatField(default=0, blank=False)

    def __str__(self):
        return f"{self.user} - {self.time}"


