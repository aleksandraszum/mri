import os
import time

import numpy as np
import matplotlib.pyplot as plt
import pylab
from django.shortcuts import render

from course.algorithms import last_next_content, push_content, my_reconstruction, generate_k_space_and_x_space_graphs, \
    defining_links
from course.forms import AlgorithmForm
from course.models import Lesson, LessonContent


def index(request):
    return render(request, 'index.html')


def basic_nmr(request, part):
    css, js, title, content = push_content(1, part)
    previous, sequent, p_idx, s_idx = last_next_content(1, part)
    links = defining_links(1)

    return render(request, 'course/baseNMR.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part})


def basic_nmr_base(request):
    css, js, title, content = push_content(1, 0)
    links = defining_links(1)

    return render(request, 'course/baseNMR.html',
                  {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1})


def spin_echo(request, part):
    css, js, title, content = push_content(2, part)
    previous, sequent, p_idx, s_idx = last_next_content(2, part)
    links = defining_links(2)

    return render(request, 'course/spin_echo.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'part': part})


def spin_echo_base(request):
    css, js, title, content = push_content(2, 0)
    links = defining_links(2)

    return render(request, 'course/baseNMR.html',
                  {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1})


def k_space(request, part):
    css, js, title, content = push_content(3, part)
    previous, sequent, p_idx, s_idx = last_next_content(3, part)
    links = defining_links(3)

    return render(request, 'course/k_space.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links})


def k_space_base(request):
    css, js, title, content = push_content(3, 0)
    links = defining_links(3)

    return render(request, 'course/k_space.html',
                  {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1})


def reconstruction(request, part):
    css, js, title, content = push_content(4, part)
    previous, sequent, p_idx, s_idx = last_next_content(4, part)
    links = defining_links(4)

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
                      {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                       'p_idx': p_idx, 's_idx': s_idx, 'links': links, 'form': form, 'filename': filename,
                       'filenameX': filenameX, 'coils': coils, 'sigma': sigma, 'reconstruction': name_reconstruction})

    return render(request, 'course/reconstruction.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links})


def reconstruction_base(request):
    css, js, title, content = push_content(4, 0)
    links = defining_links(4)

    return render(request, 'course/reconstruction.html',
                  {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1})


def diffusion(request, part):
    css, js, title, content = push_content(5, part)
    previous, sequent, p_idx, s_idx = last_next_content(5, part)

    links = defining_links(5)

    return render(request, 'course/diffusion.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links})


def diffusion_base(request):
    css, js, title, content = push_content(5, 0)
    links = defining_links(5)

    return render(request, 'course/diffusion.html',
                  {'text': content, 'links': links, 'title': title, 'sequent': True, 's_idx': 1})


def lessons(request):
    return render(request, 'course/lessons.html')


def quiz(request):
    return render(request, 'course/quiz.html')
