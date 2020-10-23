import random
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import models
from django.forms import formset_factory
from django.shortcuts import render

from course.algorithms import last_next_content, push_content, my_reconstruction, generate_k_space_and_x_space_graphs, \
    defining_links, lesson_progress_check, save_lesson_progress, lesson_complete, form_save, log_in, download_data, \
    save_lesson_complete, save_User_Answer, last_result_get, question_get, image_get, lesson_progress_get, unable_title, \
    lesson_complete_check, unable_quiz
from course.forms import AlgorithmForm, SignUpForm, LoginForm, QuizForm
from course.models import LessonProgress, Lesson, Question, Answer, UserAnswer, Profile, LessonComplete
from random import shuffle


def index(request):
    return render(request, 'index.html')


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user, communicate, form = form_save(form, 'SignUpForm')
        return render(request, 'course/signup.html',
                      {'user': request.user, 'communicate': communicate, 'form': form})
    return render(request, 'course/signup.html', {'user': request.user, 'form': form})


def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        communicate = log_in(request, form)
        return render(request, 'course/login.html',
                      {'user': request.user, 'form': form, 'communicate': communicate})
    return render(request, 'course/login.html', {'user': request.user, 'form': form})


def logout_view(request):
    logout(request)
    communicate = "Wylogowano pomyślnie!"
    return render(request, 'index.html', {'communicate': communicate})


def basic_nmr(request, part):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 1, part)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        save_lesson_progress(request.user.id, 1, int(part))

    return render(request, 'course/baseNMR.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'user': request.user,
                   'progress': progress})


def basic_nmr_base(request):
    try:
        save_lesson_progress(request.user.id, 1, 0)
    except ValueError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html',
                      {'user': request.user, 'communicate': communicate})
    css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 1, 0)
    return render(request, 'course/baseNMR.html',
                  {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1, 'user': request.user,
                   'progress': progress})


def basic_nmr_quiz(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 1, 5)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        try:
            last_result = last_result_get(request, 1)
        except IndexError:
            last_result = False
        question_id = question_get(1)
        form = QuizForm(question_id)

        if request.method == 'POST':
            result, complete, communicate = save_User_Answer(request, question_id, 1)

            return render(request, 'course/after_quiz.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'links': links, 'user': request.user,
                           'progress': progress, 'result': result, 'communicate': communicate, 'complete': complete,
                           'next_lesson': 'spin_echo'})

    return render(request, 'course/quiz.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                   'progress': progress, 'form': form, 'last_result': last_result})


def spin_echo_base(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 2, 0)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/spin_echo.html',
                      {'communicate': communicate, 'user': request.user})
    is_complete = lesson_complete(request.user.id, 1)
    if is_complete:
        save_lesson_progress(request.user.id, 2, 0)
        return render(request, 'course/spin_echo.html',
                      {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1,
                       'user': request.user, 'progress': True})

    return render(request, 'course/spin_echo.html',
                  {'css': css, 'js': js, 'title': title, 'user': request.user})


def spin_echo(request, part):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 2, part)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/spin_echo.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        save_lesson_progress(request.user.id, 2, int(part))

    return render(request, 'course/spin_echo.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'user': request.user,
                   'progress': progress})


def spin_echo_quiz(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 2, 9)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/spin_echo.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        try:
            last_result = last_result_get(request, 2)
        except IndexError:
            last_result = False

        question_id = question_get(2)
        form = QuizForm(question_id)

        if request.method == 'POST':
            result, complete, communicate = save_User_Answer(request, question_id, 2)

            return render(request, 'course/after_quiz.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'links': links, 'user': request.user,
                           'progress': progress, 'result': result, 'communicate': communicate, 'complete': complete,
                           'next_lesson': 'dane_w_przestrzeni_k'})

    return render(request, 'course/quiz.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                   'progress': progress, 'form': form, 'last_result': last_result})


def k_space_base(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 3, 0)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/k_space.html',
                      {'communicate': communicate, 'user': request.user})
    is_complete = lesson_complete(request.user.id, 2)
    if is_complete:
        save_lesson_progress(request.user.id, 3, 0)
        return render(request, 'course/k_space.html',
                      {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1,
                       'user': request.user, 'progress': True})
    return render(request, 'course/k_space.html',
                  {'css': css, 'js': js, 'title': title, 'user': request.user})


def k_space(request, part):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 3, part)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/k_space.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        save_lesson_progress(request.user.id, 3, int(part))

    return render(request, 'course/k_space.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'user': request.user,
                   'progress': progress})


def k_space_quiz(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 3, 8)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        try:
            last_result = last_result_get(request, 3)
        except IndexError:
            last_result = False

        question_id = question_get(3)
        form = QuizForm(question_id)

        if request.method == 'POST':
            result, complete, communicate = save_User_Answer(request, question_id, 3)

            return render(request, 'course/after_quiz.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'links': links, 'user': request.user,
                           'progress': progress, 'result': result, 'communicate': communicate, 'complete': complete,
                           'next_lesson': 'rekonstrukcja_danych'})

        return render(request, 'course/quiz.html',
                      {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                       'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                       'progress': progress, 'form': form, 'last_result': last_result})

    return render(request, 'course/quiz.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                   'progress': progress})


def reconstruction_base(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 4, 0)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/reconstruction.html',
                      {'communicate': communicate, 'user': request.user})
    is_complete = lesson_complete(request.user.id, 3)
    if is_complete:
        save_lesson_progress(request.user.id, 4, 0)
        return render(request, 'course/reconstruction.html',
                      {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1,
                       'user': request.user, 'progress': True})
    return render(request, 'course/reconstruction.html',
                  {'css': css, 'js': js, 'title': title, 'user': request.user})


def reconstruction(request, part):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 4, part)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/reconstruction.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        save_lesson_progress(request.user.id, 4, int(part))

        if int(part) == 7:
            filename = None
            filenameX = None
            coils = None
            sigma = None
            name_reconstruction = None

            form = AlgorithmForm()
            if request.method == 'POST':
                filenameX, filename, coils, sigma, name_reconstruction = image_get(request)
            return render(request, 'course/reconstruction.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                           'sequent': sequent,
                           'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'form': form, 'filename': filename,
                           'filenameX': filenameX, 'coils': coils, 'sigma': sigma,
                           'reconstruction': name_reconstruction, 'user': request.user, 'progress': progress})

    return render(request, 'course/reconstruction.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'user': request.user,
                   'progress': progress})


def reconstruction_quiz(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 4, 8)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        try:
            last_result = last_result_get(request, 4)
        except IndexError:
            last_result = False

        question_id = question_get(4)
        form = QuizForm(question_id)

        if request.method == 'POST':
            result, complete, communicate = save_User_Answer(request, question_id, 4)

            return render(request, 'course/after_quiz.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'links': links, 'user': request.user,
                           'progress': progress, 'result': result, 'communicate': communicate, 'complete': complete,
                           'next_lesson': 'obrazowanie_dyfuzji'})

        return render(request, 'course/quiz.html',
                      {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                       'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                       'progress': progress, 'form': form, 'last_result': last_result})

    return render(request, 'course/quiz.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                   'progress': progress})


def diffusion_base(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 5, 0)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/diffusion.html',
                      {'communicate': communicate, 'user': request.user})
    is_complete = lesson_complete(request.user.id, 4)
    if is_complete:
        save_lesson_progress(request.user.id, 5, 0)
        return render(request, 'course/diffusion.html',
                      {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1,
                       'user': request.user, 'progress': True})
    return render(request, 'course/diffusion.html',
                  {'css': css, 'js': js, 'title': title, 'user': request.user})


def diffusion(request, part):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 5, part)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/diffusion.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        save_lesson_progress(request.user.id, 5, int(part))

    return render(request, 'course/diffusion.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'user': request.user,
                   'progress': progress})


def diffusion_quiz(request):
    try:
        css, js, title, content, previous, sequent, p_idx, s_idx, links, progress = download_data(request, 5, 8)
    except TypeError:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html',
                      {'user': request.user, 'communicate': communicate})
    if progress:
        try:
            last_result = last_result_get(request, 5)
        except IndexError:
            last_result = False

        question_id = question_get(5)
        form = QuizForm(question_id)

        if request.method == 'POST':
            result, complete, communicate = save_User_Answer(request, question_id, 5)

            return render(request, 'course/after_quiz.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'links': links, 'user': request.user,
                           'progress': progress, 'result': result, 'communicate': communicate, 'complete': complete,
                           'lesson': 5})

        return render(request, 'course/quiz.html',
                      {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                       'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                       'progress': progress, 'form': form, 'last_result': last_result})

    return render(request, 'course/quiz.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                   'progress': progress})


def lessons(request):
    return render(request, 'course/lessons.html')


def profile(request):
    try:
        profile = Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'index.html', {'communicate': communicate})

    complete = [True, True, True, True, True]

    for i in range(1, 6):
        try:
            lesson = LessonComplete.objects.get(user_id=User(pk=request.user.pk), lesson_id=Lesson(number_of_lesson=i))
        except LessonComplete.DoesNotExist:
            complete[i - 1] = False

    titles = unable_title(request)
    quiz = unable_quiz(request)

    return render(request, 'course/profile.html',
                  {'profile': profile, 'complete': complete, 'titles': titles, 'quiz': quiz})
