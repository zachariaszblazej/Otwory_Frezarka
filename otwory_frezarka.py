from flask import Flask, render_template, request
import math
import string
from decimal import *
import matplotlib.pyplot as plt

app = Flask(__name__)


def wylicz_kat_beta(ilosc_otworow):
    getcontext().prec = 4
    return Decimal(str(360 / ilosc_otworow))


def znajdz_kolejny_punkt(gamma, srednica_podzialowa):
    getcontext().prec = 4
    srednica_podzialowa = Decimal(str(srednica_podzialowa))
    promien = srednica_podzialowa / Decimal('2')

    if gamma == 90:
        x = 0.0
        y = float(promien)

    elif gamma == 270:
        x = 0.0
        y = float(-promien)

    else:

        gamma_rad = Decimal(str(math.radians(gamma)))
        tangens = Decimal(str(math.tan(gamma_rad)))

        x_abs = promien / Decimal(str(math.sqrt(tangens ** 2 + Decimal('1'))))
        x = -x_abs if 90 < gamma < 270 else x_abs

        y = Decimal(tangens * x)

        x = round(float(x), 3)
        y = round(float(y), 3)

    if -0.001 < x < 0.001:
        x = 0.0

    if -0.001 < y < 0.001:
        y = 0.0

    result = [x, y]

    return result


def narysuj_obraz_pogladowy(punkty, srednica_podzialowa, alfa, ilosc_otworow):
    fig = plt.figure()

    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    plt.gca().set_aspect('equal', adjustable='box')

    plt.title(f'alfa = {alfa}, ilość otworów = {ilosc_otworow}, PD = {srednica_podzialowa}')

    promien = float(srednica_podzialowa) / 2
    granica = promien * 1.3

    plt.xlim(-granica, granica)
    plt.ylim(-granica, granica)

    plt.axvline(x=0, color='black')
    plt.axhline(y=0, color='black')

    circle = plt.Circle((0, 0), promien, fill=False, linestyle='dashed')
    axes.add_artist(circle)

    for xp, yp, ozn in punkty:
        plt.scatter(xp, yp, s=200)

        if ilosc_otworow <= 25:
            plt.annotate(ozn, (xp, yp), textcoords="offset points", xytext=(0, 10), ha='left', va='bottom',
                         fontsize='medium', fontweight='bold', color="red")

    plt.savefig('./static/obraz_pogladowy.png', bbox_inches='tight')


def znajdz_wszystkie_otwory(ilosc_otworow, alfa, srednica_podzialowa):
    getcontext().prec = 4
    alfa = Decimal(alfa)
    beta = wylicz_kat_beta(ilosc_otworow)
    gamma = alfa

    punkty = []

    for i in range(0, ilosc_otworow):
        punkt = znajdz_kolejny_punkt(gamma, srednica_podzialowa)
        oznaczenie = string.ascii_uppercase[i] if ilosc_otworow <= 25 else i + 1
        punkt.append(oznaczenie)
        punkty.append(punkt)
        gamma += beta

    narysuj_obraz_pogladowy(punkty, srednica_podzialowa, alfa, ilosc_otworow)

    return punkty


@app.route('/')
def home():
    return render_template('base.html', alfa=0, ilosc_otworow=2, srednica=1)


@app.route('/wylicz_otwory', methods=['GET', 'POST'])
def wylicz_otwory():
    if request.method == 'POST':
        ilosc_otworow = int(request.form['ilosc_otworow'])
        alfa = request.form['alfa']
        srednica_podzialowa = request.form['srednica']

        punkty = znajdz_wszystkie_otwory(ilosc_otworow, alfa, srednica_podzialowa)

        return render_template('wylicz_otwory.html', ilosc_otworow=ilosc_otworow, alfa=alfa,
                               srednica=srednica_podzialowa, punkty=punkty)
