import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render

from course.algorithms import last_next_content, push_content, my_reconstruction, generate_k_space_and_x_space_graphs, \
    defining_links, lesson_progress_check, save_lesson_progress, lesson_complete
from course.forms import AlgorithmForm, SignUpForm, LoginForm
from course.models import LessonProgress, Lesson


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'index.html', {'user': user, 'login': True})
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            communicate = "Zarejestrowałeś się pomyślnie"

            form = LoginForm()
            return render(request, 'course/login.html',
                          {'communicate': communicate, 'login': False, 'form': form})
        return render(request, 'course/signup.html', {'form': form, 'login': False})


def login_view(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'index.html', {'user': user, 'login': True})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                u = form.cleaned_data['username']
                p = form.cleaned_data['password']
                user = authenticate(username=u, password=p)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'index.html', {'form': form, 'login': True})
                    else:
                        communicate = "Konto jest nieaktywne."
                        return render(request, 'course/login.html',
                                      {'form': form, 'communicate': communicate, 'login': False})
                else:
                    communicate = "Hasło bądź login są nieprawidłowe."
                    return render(request, 'course/login.html',
                                  {'form': form, 'communicate': communicate, 'login': False})
        else:
            form = LoginForm()
            return render(request, 'course/login.html', {'form': form, 'login': False})


def logout_view(request):
    logout(request)
    communicate = "Wylogowano pomyślnie!"
    return render(request, 'index.html', {'communicate': communicate})


def basic_nmr(request, part):
    css, js, title, content = push_content(1, part)
    if request.user.is_authenticated:
        previous, sequent, p_idx, s_idx = last_next_content(1, part)
        links = defining_links(1)
        user = request.user
        user_id = user.id
        previous_part = int(part) - 1
        progress = lesson_progress_check(user, 1, int(previous_part))
        if progress:
            save_lesson_progress(user_id, 1, int(part))
            return render(request, 'course/baseNMR.html',
                          {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous,
                           'sequent': sequent,
                           'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part, 'login': True})
        else:
            communicate = "Nie masz jeszcze dostępu do tej części kursu"
            return render(request, 'course/baseNMR.html',
                          {'css': css, 'js': js, 'title': title, 'communicate': communicate, 'login': True})

    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html', {'login': False, 'communicate': communicate, 'title': title})


def basic_nmr_base(request):
    css, js, title, content = push_content(1, 0)
    if request.user.is_authenticated:
        links = defining_links(1)
        user_id = request.user.id
        save_lesson_progress(user_id, 1, 0)
        return render(request, 'course/baseNMR.html',
                      {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1, 'login': True})
    else:
        communicate = "Dostęp tylko dla zalogowanych!"
        return render(request, 'course/baseNMR.html', {'login': False, 'communicate': communicate, 'title': title})


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
        is_complete = lesson_complete(user_id, 2)
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
        is_complete = lesson_complete(user_id, 3)
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
        is_complete = lesson_complete(user_id, 4)
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
        is_complete = lesson_complete(user_id, 5)
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


def quiz(request):
    return render(request, 'course/quiz.html')
