import os
import numpy as np
from math import pi, cos, sin, sqrt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from mat4py import loadmat
import matplotlib.pyplot as plt
import pylab
from course.forms import LoginForm, QuizForm
from course.models import LessonContent, Lesson, LessonProgress, LessonComplete, UserAnswer, Question, Answer
from random import shuffle


def form_save(form, formName):
    if formName == 'SignUpForm':
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        communicate = "Zarejestrowałeś się pomyślnie"
        form = LoginForm()
        return user, communicate, form


def log_in(request, form):
    u = form.cleaned_data['username']
    p = form.cleaned_data['password']
    user = authenticate(username=u, password=p)
    if user is not None:
        if user.is_active:
            login(request, user)
            communicate = "Zalogowano pomyślnie!"
        else:
            communicate = "Konto jest nieaktywne."
    else:
        communicate = "Hasło bądź login są nieprawidłowe."
    return communicate


def lesson_progress_check(user_id, lesson_id, part):
    previous = True
    try:
        previous_lesson = LessonProgress.objects.get(user_id=user_id, lesson_id=lesson_id, part=part)
    except LessonProgress.DoesNotExist:
        previous = False
    return previous


def save_lesson_progress(user_id, lesson_id, part):
    try:
        previous_lesson = LessonProgress.objects.get(user_id=user_id, lesson_id=lesson_id, part=part)
    except LessonProgress.DoesNotExist:
        previous_lesson = LessonProgress(user_id=User(pk=user_id), lesson_id=Lesson(pk=lesson_id), part=part)
        previous_lesson.save()


def lesson_complete(user_id, lesson_id):
    try:
        is_complete = LessonComplete.objects.get(user_id=user_id, lesson_id=lesson_id)
    except LessonComplete.DoesNotExist:
        return False
    return True


def save_lesson_complete(user_id, lesson_id):
    try:
        is_complete = LessonComplete.objects.get(user_id=user_id, lesson_id=lesson_id)
    except LessonComplete.DoesNotExist:
        previous_lesson = LessonComplete(user_id=User(pk=user_id), lesson_id=Lesson(pk=lesson_id), complete=True)
        previous_lesson.save()


def push_content(lesson_id, part_of_the_lesson):
    css = Lesson.objects.get(pk=lesson_id).css
    js = Lesson.objects.get(pk=lesson_id).js
    title = Lesson.objects.get(pk=lesson_id).title
    content = LessonContent.objects.get(lesson_id=lesson_id, part_of_the_lesson=part_of_the_lesson).content

    return css, js, title, content


def last_next_content(lesson_id, part_of_the_lesson):
    previous = True
    sequent = True

    p_idx = int(part_of_the_lesson) - 1
    s_idx = int(part_of_the_lesson) + 1

    try:
        p = LessonContent.objects.get(lesson_id=lesson_id, part_of_the_lesson=p_idx)
    except LessonContent.DoesNotExist:
        previous = False
    if p_idx == 0:
        previous = False

    try:
        n = LessonContent.objects.get(lesson_id=lesson_id, part_of_the_lesson=s_idx)
    except LessonContent.DoesNotExist:
        sequent = False

    return previous, sequent, p_idx, s_idx


def defining_links(lesson_id):
    links = None
    if lesson_id == 1:
        links = {'Jądrowy moment magnetyczny': '1', 'Częstotliwość Larmora': '2', 'Zjawisko rezonansu': '3',
                 'Symulator - wpływ impulsu na wektor magnetyzacji': '4', 'Słowniczek i bibliografia': '5'}
    if lesson_id == 2:
        links = {'Wpływ impulsu RF na wektor magnetyzacji': '1', 'Zjawisko relaksacji': '2', 'Sekwencja spin-echo': '3',
                 'Diagram oraz animacja przedstawiający sekwencję spin-echo': '4',
                 'Wykorzystanie echa spinowego w MRI': '5',
                 'Przedstawienie obrazu mózgu z wykorzystaniem różnych wartości parametrów TE oraz TR oraz symulator': '6',
                 'Obrazy T1-, T2- i PD-zależne': '7', 'Zalety i wady echa spinowego': '8',
                 'Słowniczek i bibliografia': '9'}
    if lesson_id == 3:
        links = {'Przestrzeń k': '1', 'Przestrzenie danych i kroki przetwarzania': '2',
                 'Schemat - przestrzeń k oraz x': '3', 'Symulator - próbkowanie sygnału': '4',
                 'Akwizycja danych i wypełnianie przestrzeni k ': '5', 'Obrazowanie jednokanałowe i wielokanałowe': '6',
                 'Obrazowanie równoległe': '7', 'Słowniczek i bibliografia': '8'}
    if lesson_id == 4:
        links = {'Jednokanałowa akwizycja sygnału': '1', 'Wielokanałowa akwizycja sygnału': '2',
                 'Metoda SMF oraz SoS': '3',
                 'Obrazowanie równoległe przyspieszone - SENSE': '4', 'Metoda SENSE': '5', 'Metoda GRAPPA': '6',
                 'Symulator: rekonstrukcja obrazu': '7', 'Słowniczek i bibliografia': '8'}

    if lesson_id == 5:
        links = {'Dyfuzja': '1', 'Mierzenie dyfuzji': '2',
                 'Symulator - wpływ gradientu pola magnetycznego na rotację momentów magnetycznych': '3',
                 'Obrazowanie dyfuzji metodą rezonansu magnetycznego DWI': '4', 'Obrazowanie dyfuzyjne': '5',
                 'Obrazowanie tensora dyfuzji DTI': '6', 'Zastosowanie kliniczne obrazowania dyfuzji': '7',
                 'Słowniczek i bibliografia': '8'}

    return links


def unable_links(request, lesson_id):
    links = defining_links(lesson_id)
    for key in links.keys():
        if not lesson_progress_check(request.user.id, lesson_id, links[key]):
            links[key] = None
    return links


def download_data(request, lesson_id, part):
    css, js, title, content = push_content(lesson_id, part)
    previous, sequent, p_idx, s_idx = last_next_content(lesson_id, part)
    links = unable_links(request, lesson_id)
    if int(part) != 0:
        previous_part = int(part) - 1
    else:
        previous_part = 0
    progress = lesson_progress_check(request.user, lesson_id, int(previous_part))
    if part == 0:
        progress = True
    return css, js, title, content, previous, sequent, p_idx, s_idx, links, progress


def question_get(lesson_id):
    all_question = Question.objects.filter(lesson_id=lesson_id)
    question_id = []
    for question in all_question:
        question_id.append(question.pk)
    shuffle(question_id)
    question_id = question_id[0:8]
    return question_id


def last_result_get(request, lesson_number):
    try:
        user_result = list(UserAnswer.objects.filter(user_id=User(pk=request.user.pk),
                                                     lesson=Lesson.objects.get(number_of_lesson=lesson_number)))
        last_result = user_result[-1].result
    except UserAnswer.DoesNotExist:
        last_result = False
    return last_result


def save_User_Answer(request, question_id, lesson_id):
    form = QuizForm(question_id, request.POST)

    answer_1 = int(form['answer_1'].value())
    answer_2 = int(form['answer_2'].value())
    answer_3 = int(form['answer_3'].value())
    answer_4 = int(form['answer_4'].value())
    answer_5 = int(form['answer_5'].value())
    answer_6 = int(form['answer_6'].value())
    answer_7 = int(form['answer_7'].value())
    answer_8 = int(form['answer_8'].value())
    answer = [answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7, answer_8]

    question_1 = Answer.objects.get(pk=answer_1).question_id
    question_2 = Answer.objects.get(pk=answer_2).question_id
    question_3 = Answer.objects.get(pk=answer_3).question_id
    question_4 = Answer.objects.get(pk=answer_4).question_id
    question_5 = Answer.objects.get(pk=answer_5).question_id
    question_6 = Answer.objects.get(pk=answer_6).question_id
    question_7 = Answer.objects.get(pk=answer_7).question_id
    question_8 = Answer.objects.get(pk=answer_8).question_id

    true_answer = 0

    for a in answer:
        if Answer.objects.get(pk=a).is_true:
            true_answer = true_answer + 1

    result = (true_answer / 8.0) * 100

    user_answer = UserAnswer(user=User(request.user.pk),
                             answer_1_id=Answer.objects.get(pk=answer_1),
                             answer_2_id=Answer.objects.get(pk=answer_2),
                             answer_3_id=Answer.objects.get(pk=answer_3),
                             answer_4_id=Answer.objects.get(pk=answer_4),
                             answer_5_id=Answer.objects.get(pk=answer_5),
                             answer_6_id=Answer.objects.get(pk=answer_6),
                             answer_7_id=Answer.objects.get(pk=answer_7),
                             answer_8_id=Answer.objects.get(pk=answer_8),

                             question_1_id=Question.objects.get(pk=question_1.pk),
                             question_2_id=Question.objects.get(pk=question_2.pk),
                             question_3_id=Question.objects.get(pk=question_3.pk),
                             question_4_id=Question.objects.get(pk=question_4.pk),
                             question_5_id=Question.objects.get(pk=question_5.pk),
                             question_6_id=Question.objects.get(pk=question_6.pk),
                             question_7_id=Question.objects.get(pk=question_7.pk),
                             question_8_id=Question.objects.get(pk=question_8.pk),

                             lesson=Lesson.objects.get(number_of_lesson=1), result=result)
    user_answer.save()
    if result > 90:
        communicate = "Zaliczyłeś moduł bardzo dobrze!\nMożesz przejść do kolejnej lekcji"
        save_lesson_complete(request.user.pk, lesson_id)
        complete = True

    else:
        communicate = "Słabo Ci poszło!\nPowtórz materiał jeszcze raz albo spróbuj ponownie rozwiązać test wiedzy"
        complete = False

    return result, complete, communicate


def sensitivity_map(Mx, My, coils):
    ejex = np.arange(Mx).reshape(1, Mx)
    ejex = ejex + 1
    ejey = np.linspace(1, My, My)

    vX = np.tile(ejex.transpose(), (1, My))
    vY = np.tile(ejey, (Mx, 1))

    vX = pi / 2 * vX / (vX.max())
    vY = pi / 2 * vY / (vY.max())

    Theta = np.linspace(0, (2 * pi - (2 * pi / coils)), coils)
    Theta = Theta[0:-1]

    MapW = np.zeros((coils, Mx, My))

    for ii in range(0, int(coils / 2)):

        if Theta[ii] <= pi / 2:
            N1 = vX * cos(Theta[ii]) + vY * sin(Theta[ii])
            N1 = N1 / (N1.max()) * pi / 2
            MapW[ii, :, :] = np.cos((N1))
            jj = int((coils / 2)) + ii
            MapW[jj, :, :] = np.sin(N1)

        else:
            N1 = vX * abs(cos(Theta[ii])) + (pi / 2 - vY) * sin(Theta[ii])
            N1 = N1 / (N1.max()) * pi / 2
            MapW[ii, :, :] = np.sin(N1)
            jj = int((coils / 2)) + ii
            MapW[jj, :, :] = np.cos(N1)

    MapW = MapW / sqrt(coils / 2)

    return MapW


def my_reconstruction(coils, Sigma, rho, parallel):
    data = loadmat(os.path.join(os.path.dirname(__file__), 'static', 'T1_data.mat'))
    I = data.get('I')

    Mx, My = np.shape(I)
    MapW = sensitivity_map(Mx, My, coils)

    if coils != 1:
        It = np.tile(I, (coils, 1, 1)) * MapW
    else:
        It = np.tile(I, (coils, 1, 1))
        MapW = 1

    corr = 0

    if (np.size(Sigma) > 1) or (rho > 0):
        corr = 1

    if corr == 0:
        sigma = sqrt(Sigma)
        Int = It + sigma * np.random.randn(coils, Mx, My) + 1j * np.random.randn(coils, Mx, My)

    else:
        if np.size(Sigma) == 1:
            s1 = Sigma
            Sigma = s1 * (np.eye(coils) + rho * (np.ones((coils)) - np.eye(coils)))

        Nc = np.random.randn(coils, Mx, My) + 1j * np.random.randn(coils, Mx, My)
        D, V = np.linalg.eigh(Sigma)

        W = V * np.sqrt(D)

        Nc2 = np.zeros((coils, Mx, My)) * 1j

        for ii in range(0, Mx):
            for jj in range(0, My):
                if coils != 1:
                    Nc2[:, ii, jj] = W @ np.squeeze(Nc[:, ii, jj])
                else:
                    Nc2[:, ii, jj] = W @ Nc[:, ii, jj]

        Int = It + Nc2

    SN = np.fft.fftshift(np.fft.fftshift(np.fft.fft2(Int), 1), 2)
    S0 = np.fft.fftshift(np.fft.fftshift(np.fft.fft2(It), 1), 2)

    ML0 = np.sqrt(sum((abs(It) ** 2), 0))

    if parallel == 0:
        # Metoda SoS
        ML = np.sqrt(sum((abs(Int) ** 2), 0))

    elif parallel == 1:
        # single coil, only for coils == 1
        ML = np.sqrt(sum((abs(Int) ** 2), 0))
    else:
        # SENSE
        rate = np.array([2])

        TasaM = rate[0]

        if np.size(rate) == 2:
            FsLn = rate[1]

            if (rate[1] > rate[0]):
                print('Initial sample line mus be smaller orr equal to acceleration rate')

        else:
            FsLn = 1

            #
        x, y, z = np.shape(S0)

        Sk = SN[0:x][:, ::TasaM][:, :, 0:z]

        SN = Sk

        mz, Mx, My = np.shape(Sk)
        coiil, Nx2, yy = np.shape(MapW)

        IxS = np.zeros((coils, Mx, My)) * 1j

        for ii in range(0, coils):
            IxS[ii, :, :] = np.fft.ifft2(np.fft.fftshift(np.fft.fftshift(Sk[ii, :, :], 0), 1))

        Is = np.zeros((Nx2, My)) * 1j
        mp = np.zeros((coiil, 2)) * 1j

        for jj in range(0, Mx):
            for ii in range(0, My):
                if (jj + Mx * (rate - 1)) > Nx2:
                    D1 = (jj + Mx * (rate - 1)) - Nx2
                else:
                    D1 = 0

                a = MapW[:, jj, ii]
                b = MapW[:, jj - int(D1) + Mx * (int(rate) - 1), ii]

                mp[:, 0] = a[:]
                mp[:, 1] = b[:]
                mp2 = np.conj(mp).transpose() * np.mat(mp)
                I_mat = np.squeeze(IxS[:, jj, ii])[np.newaxis]
                I_mat = I_mat.transpose()
                myIs = np.transpose(np.linalg.inv(mp2) * np.conj(mp).transpose() * I_mat)
                a = jj - int(D1) + Mx * (int(rate) - 1)
                Is[jj, ii] = myIs[0, 0]
                Is[a, ii] = myIs[0, 1]

        ML = np.abs(Is)

    return (SN, S0, ML0, ML)


def generate_k_space_and_x_space_graphs(date, ML, coils, SN, reconstruction):
    # x-space files
    nameX = 'xspace' + str(int(date)) + '.svg'
    filenameX = os.path.join('simulations', nameX)
    sizes = np.shape(ML)
    fig = plt.figure()
    fig.set_size_inches(1. * sizes[0] / sizes[1], 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(np.abs(ML), cmap=pylab.gray())
    plt.savefig(os.path.join(os.path.dirname(__file__), 'static', filenameX), dpi=sizes[0], cmap=pylab.gray())
    plt.close()

    # k-space file
    if coils == 1:
        myImageK = SN[0, 0::, 0::]

        name = 'kspace' + str(int(date)) + '.svg'
        filename = os.path.join('simulations', name)

        sizes = np.shape(myImageK)
        fig = plt.figure()
        fig.set_size_inches(1. * sizes[0] / sizes[1], 1, forward=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(np.log(np.abs(myImageK)), cmap=pylab.gray())
        plt.savefig(os.path.join(os.path.dirname(__file__), 'static', filename), dpi=sizes[0],
                    cmap=pylab.gray())
        plt.close()

    elif coils == 4:
        if reconstruction == 2:
            myImageK = np.zeros((268, 526))
            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i, j] = SN[0, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i, j + 270] = SN[0, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 140, j] = SN[0, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 140, j + 270] = SN[0, i, j]

        else:
            mz, mx, my = np.shape(SN)
            myImageK = np.zeros((2 * mx + 14, 2 * my + 14))

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i, j] = SN[0, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[mx + i + 14, j] = SN[1, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i, my + j + 14] = SN[2, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[mx + i + 14, my + j + 14] = SN[3, i, j]

        name = 'kspace' + str(int(date)) + '.svg'
        filename = os.path.join('simulations', name)

        sizes = np.shape(myImageK)
        fig = plt.figure()
        fig.set_size_inches(1. * sizes[1] / sizes[0], 1, forward=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(np.log(np.abs(myImageK)), cmap=pylab.gray(), interpolation='nearest',
                  aspect='equal')
        plt.savefig(os.path.join(os.path.dirname(__file__), 'static', filename), dpi=sizes[0],
                    cmap=pylab.gray())
        plt.close()


    else:
        mz, mx, my = np.shape(SN)
        if reconstruction == 2:
            mz, mx, my = np.shape(SN)
            myImageK = np.zeros((548, 526))

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i, j] = SN[0, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i, j + 270] = SN[1, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 140, j] = SN[2, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 140, 270 + j] = SN[3, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 280, j] = SN[4, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 280, 270 + j] = SN[5, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 420, j] = SN[6, i, j]

            for i in range(0, 128):
                for j in range(0, 256):
                    myImageK[i + 420, 270 + j] = SN[7, i, j]

        else:
            myImageK = np.zeros((526, 1054))

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i, j] = SN[0, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i, j + 266] = SN[1, i, j]

            for i in range(0, 256):
                for j in range(0, 256):
                    myImageK[i, j + 532] = SN[2, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i, j + 798] = SN[3, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i + 270, j] = SN[4, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i + 270, j + 266] = SN[5, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i + 270, j + 532] = SN[6, i, j]

            for i in range(0, mx):
                for j in range(0, my):
                    myImageK[i + 270, j + 798] = SN[7, i, j]

        name = 'kspace' + str(int(date)) + '.svg'
        filename = os.path.join('simulations', name)

        sizes = np.shape(myImageK)
        fig = plt.figure()
        fig.set_size_inches(1. * sizes[1] / sizes[0], 1, forward=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(np.log(np.abs(myImageK)), cmap=pylab.gray(), interpolation='nearest',
                  aspect='equal')
        plt.savefig(os.path.join(os.path.dirname(__file__), 'static', filename), dpi=sizes[0],
                    cmap=pylab.gray())
        plt.close()

    return filenameX, filename
