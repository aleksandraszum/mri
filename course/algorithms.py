import os

import numpy as np
from math import pi, cos, sin, sqrt, log
from mat4py import loadmat
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pylab

from course.models import LessonContent, Lesson


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

    try:
        n = LessonContent.objects.get(lesson_id=lesson_id, part_of_the_lesson=s_idx)
    except LessonContent.DoesNotExist:
        sequent = False

    return previous, sequent, p_idx, s_idx


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