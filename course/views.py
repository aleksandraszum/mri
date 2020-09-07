import os
import time

import numpy as np
import matplotlib.pyplot as plt
import pylab
from django.shortcuts import render

from course.algorithms import last_next_content, push_content, my_reconstruction, generate_k_space_and_x_space_graphs
from course.forms import AlgorithmForm
from course.models import Lesson, LessonContent


def index(request):
    return render(request, 'index.html')


def basic_nmr(request, part):
    css, js, title, content = push_content(1, part)
    previous, sequent, p_idx, s_idx = last_next_content(1, part)
    links = {'Jądrowy moment magnetyczny': '1', 'Częstotliwość Larmora': '2', 'Zjawisko rezonansu': '3',
             'Symulator - wpływ impulsu na wektor magnetyzacji': '4', 'Słowniczek i bibliografia': '5'}

    for k, v in links.items():
        print(k, 'corresponds to', v)

    return render(request, 'course/baseNMR.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links})


def spin_echo(request, part):
    css, js, title, content = push_content(2, part)
    previous, sequent, p_idx, s_idx = last_next_content(2, part)
    links = {'Wpływ impulsu RF na wektor magnetyzacji': '1', 'Zjawisko relaksacji': '2', 'Sekwencja spin-echo': '3',
             'Diagram przedstawiający sekwencję spin-echo': '4', 'Animacja przedstawiająca sekwencję spin-echo': '5',
             'Wykorzystanie echa spinowego w MRI': '6',
             'Przedstawienie obrazu mózgu z wykorzystaniem różnych wartości parametrów TE oraz TR': 7,
             'Obrazy T1-, T2- i PD-zależne': '8', 'Symulator - wybierz czas TR oraz TE': '9',
             'Zalety i wady echa spinowego': '10', 'Słowniczek i bibliografia': '11'}

    return render(request, 'course/spin_echo.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links})


def k_space(request, part):
    css, js, title, content = push_content(3, part)
    previous, sequent, p_idx, s_idx = last_next_content(3, part)
    links = {'Przestrzeń k': '1', 'Przestrzenie danych i kroki przetwarzania': '2',
             'Schemat - przestrzeń k oraz x': '3', 'Symulator - próbkowanie sygnału': '4',
             'Akwizycja danych i wypełnianie przestrzeni k ': '5', 'Obrazowanie jednokanałowe i wielokanałowe': '6',
             'Obrazowanie równoległe': '7', 'Słowniczek i bibliografia': '8'}

    return render(request, 'course/k_space.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links})


def reconstruction(request, part):
    css, js, title, content = push_content(4, part)
    previous, sequent, p_idx, s_idx = last_next_content(4, part)
    links = {'Jednokanałowa akwizycja sygnału': '1', 'Wielokanałowa akwizycja sygnału': '2', 'Metoda SMF oraz SoS': '3',
             'Obrazowanie równoległe przyspieszone - SENSE': '4', 'Metoda SENSE': '5', 'Metoda GRAPPA': '6',
             'Symulator: rekonstrukcja obrazu': '7', 'Słowniczek i bibliografia': '8'}

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


def diffusion(request, part):
    css, js, title, content = push_content(5, part)
    previous, sequent, p_idx, s_idx = last_next_content(5, part)

    links = {'Dyfuzja': '1', 'Mierzenie dyfuzji': '2',
             'Symulator - wpływ gradientu pola magnetycznego na rotację momentów magnetycznych': '3',
             'Obrazowanie dyfuzji metodą rezonansu magnetycznego DWI': '4', 'Obrazowanie dyfuzyjne': '5',
             'Obrazowanie tensora dyfuzji DTI': '6', 'Zastosowanie kliniczne obrazowania dyfuzji': '7',
             'Słowniczek i bibliografia': '8'}

    return render(request, 'course/diffusion.html',
                  {'css': css, 'js': js, 'title': title, 'text': content, 'previous': previous, 'sequent': sequent,
                   'p_idx': p_idx, 's_idx': s_idx, 'links': links})
