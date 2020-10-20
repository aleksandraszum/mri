import random
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import models
from django.forms import formset_factory
from django.shortcuts import render

from course.algorithms import last_next_content, push_content, my_reconstruction, generate_k_space_and_x_space_graphs, \
    defining_links, lesson_progress_check, save_lesson_progress, lesson_complete, form_save, log_in, download_data, \
    save_lesson_complete, result_question_get, save_User_Answer
from course.forms import AlgorithmForm, SignUpForm, LoginForm, QuizForm
from course.models import LessonProgress, Lesson, Question, Answer, UserAnswer
from random import shuffle


def index(request):
    return render(request, 'index.html')


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user, communicate, form = form_save(form, 'SignUpForm')
        return render(request, 'course/login.html',
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
        last_result, question_id = result_question_get(request, 1)
        form = QuizForm(question_id)

        if request.method == 'POST':
            result, complete, communicate = save_User_Answer(request, question_id)

            return render(request, 'course/after_quiz.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'links': links, 'user': request.user,
                           'progress': progress, 'result': result, 'communicate': communicate, 'complete': complete})

        return render(request, 'course/quiz.html',
                      {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                       'sequent': sequent, 'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                       'progress': progress, 'form': form, 'last_result': last_result})

    return render(request, 'course/quiz.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                   'sequent': sequent,'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'user': request.user,
                   'progress': progress})


def spin_echo(request, part):
    css, js, title, content = push_content(2, part)
    if request.user.is_authenticated:
        previous, sequent, p_idx, s_idx = last_next_content(2, part)
        links = defining_links(2)
        user = request.user
        user_id = user.id
        previous_part = int(part) - 1
        progress = lesson_progress_check(user, 2, int(previous_part))
        if progress:
            save_lesson_progress(user_id, 2, int(part))
            return render(request, 'course/spin_echo.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                           'sequent': sequent,
                           'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/spin_echo.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})

    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/spin_echo.html', {'login': False, 'communicate': communicate, 'title': title})


def spin_echo_base(request):
    css, js, title, content = push_content(2, 0)
    if request.user.is_authenticated:
        links = defining_links(2)
        user_id = request.user.id
        save_lesson_progress(user_id, 2, 0)
        is_complete = lesson_complete(user_id, 1)
        if is_complete:
            save_lesson_progress(user_id, 2, 0)
            return render(request, 'course/spin_echo.html',
                          {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/spin_echo.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})
    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/spin_echo.html', {'login': False, 'communicate': communicate, 'title': title})


def k_space(request, part):
    css, js, title, content = push_content(3, part)
    if request.user.is_authenticated:
        previous, sequent, p_idx, s_idx = last_next_content(3, part)
        links = defining_links(3)
        user = request.user
        user_id = user.id
        previous_part = int(part) - 1
        progress = lesson_progress_check(user, 3, int(previous_part))
        if progress:
            save_lesson_progress(user_id, 3, int(part))
            return render(request, 'course/k_space.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                           'sequent': sequent,
                           'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/k_space.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})

    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/k_space.html', {'login': False, 'communicate': communicate, 'title': title})


def k_space_base(request):
    css, js, title, content = push_content(3, 0)
    if request.user.is_authenticated:
        links = defining_links(3)
        user_id = request.user.id
        save_lesson_progress(user_id, 3, 0)
        is_complete = lesson_complete(user_id, 2)
        if is_complete:
            save_lesson_progress(user_id, 3, 0)
            return render(request, 'course/k_space.html',
                          {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/k_space.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})
    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/k_space.html', {'login': False, 'communicate': communicate, 'title': title})


def reconstruction(request, part):
    css, js, title, content = push_content(4, part)
    previous, sequent, p_idx, s_idx = last_next_content(4, part)
    links = defining_links(4)
    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        previous_part = int(part) - 1
        progress = lesson_progress_check(user, 4, int(previous_part))
        if progress:
            save_lesson_progress(user_id, 4, int(part))
            if int(part) == 7:
                filename = None
                filenameX = None
                coils = None
                sigma = None
                name_reconstruction = None

                if request.method == 'POST':
                    form = AlgorithmForm(request.POST)
                    if form.is_valid():
                        coils = int(form['coils'].value())
                        sigma = float(form['sigma'].value())
                        correlation = float(form['correlation'].value())
                        reconstruction = int(form['reconstruction'].value())

                        if coils == 1:
                            correlation = 0
                            reconstruction = 0
                            name_reconstruction = 'Metoda SoS dla obrazowania jednokanałowego'
                        else:
                            if reconstruction == 0:
                                reconstruction = 1
                                name_reconstruction = 'Metoda SoS dla obrazowania wielokanałowego'

                            else:
                                reconstruction = 2
                                name_reconstruction = 'Metoda SENSE'
                        SN, S0, ML0, ML = my_reconstruction(coils, sigma,
                                                            correlation, reconstruction)
                        date = time.time()
                        filenameX, filename = generate_k_space_and_x_space_graphs(date, ML, coils, SN, reconstruction)
                    else:
                        print('Form has invalid fields')
                else:
                    form = AlgorithmForm()

                return render(request, 'course/reconstruction.html',
                              {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                               'sequent': sequent,
                               'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'form': form, 'filename': filename,
                               'filenameX': filenameX, 'coils': coils, 'sigma': sigma,
                               'reconstruction': name_reconstruction, 'login': True})

            return render(request, 'course/reconstruction.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                           'sequent': sequent,
                           'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/baseNMR.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})

    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/reconstruction.html',
                      {'login': False, 'communicate': communicate, 'title': title})


def reconstruction_base(request):
    css, js, title, content = push_content(4, 0)
    links = defining_links(4)
    if request.user.is_authenticated:
        user_id = request.user.id
        save_lesson_progress(user_id, 4, 0)
        is_complete = lesson_complete(user_id, 3)
        if is_complete:
            save_lesson_progress(user_id, 4, 0)
            return render(request, 'course/reconstruction.html',
                          {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/reconstruction.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})
    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/reconstruction.html',
                      {'login': False, 'communicate': communicate, 'title': title})


def diffusion(request, part):
    css, js, title, content = push_content(5, part)
    previous, sequent, p_idx, s_idx = last_next_content(5, part)

    links = defining_links(5)
    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        previous_part = int(part) - 1
        progress = lesson_progress_check(user, 5, int(previous_part))

        if progress:
            save_lesson_progress(user_id, 5, int(part))
            return render(request, 'course/diffusion.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                           'sequent': sequent,
                           'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/diffusion.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})
    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        form = LoginForm()
        return render(request, 'course/diffusion.html', {'login': False, 'communicate': communicate, 'title': title})


def diffusion_base(request):
    css, js, title, content = push_content(5, 0)
    links = defining_links(5)
    if request.user.is_authenticated:
        user_id = request.user.id
        save_lesson_progress(user_id, 5, 0)
        is_complete = lesson_complete(user_id, 4)
        if is_complete:
            save_lesson_progress(user_id, 5, 0)
            return render(request, 'course/diffusion.html',
                          {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/diffusion.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})
    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        form = LoginForm()
        return render(request, 'course/diffusion.html', {'login': False, 'communicate': communicate, 'title': title})


def lessons(request):
    return render(request, 'course/lessons.html')
