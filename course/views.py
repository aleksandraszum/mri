from django.http import HttpResponse
from django.shortcuts import render

from course.algorithms import last_next_content, push_content
from course.models import Lesson, LessonContent


def index(request):
    return render(request, 'index.html')


def basic_NMR(request, part):
    css, js, title, content = push_content(1, part)

    previous, sequent, p_idx, s_idx = last_next_content(1, part)

    return render(request, 'course/baseNMR.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx})


def spin_echo(request, part):
    css, js, title, content = push_content(2, part)

    previous, sequent, p_idx, s_idx = last_next_content(2, part)

    return render(request, 'course/spin_echo.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx})


def k_space(request, part):
    css, js, title, content = push_content(3, part)

    previous, sequent, p_idx, s_idx = last_next_content(3, part)

    return render(request, 'course/k_space.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx})


def reconstruction(request, part):
    css, js, title, content = push_content(4, part)

    previous, sequent = last_next_content(4, part)
    p_idx = int(part) - 1
    s_idx = int(part) + 1

    return render(request, 'course/reconstruction.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx})


def diffusion(request, part):
    css, js, title, content = push_content(5, part)

    previous, sequent, p_idx, s_idx = last_next_content(5, part)

    return render(request, 'course/spin_echo.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx})
