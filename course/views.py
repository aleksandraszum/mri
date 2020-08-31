from django.http import HttpResponse
from django.shortcuts import render

from course.models import Lesson, LessonContent


def index(request):
    return render(request, 'index.html')


def basic_NMR(request, part):
    css = Lesson.objects.get(pk=1).css
    js = Lesson.objects.get(pk=1).js
    title = Lesson.objects.get(pk=1).title
    content = LessonContent.objects.get(lesson_id=1, part_of_the_lesson=part).content
    previous = True
    again = True

    p_idx = int(part) - 1
    n_idx = int(part) + 1

    try:
        p = LessonContent.objects.get(lesson_id=1, part_of_the_lesson=p_idx)
    except LessonContent.DoesNotExist:
        previous = False

    try:
        n = LessonContent.objects.get(lesson_id=1, part_of_the_lesson=n_idx)
    except LessonContent.DoesNotExist:
        again = False

    return render(request, 'course/baseNMR.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'next': again,
                   'p_idx': p_idx, 'n_idx': n_idx})
