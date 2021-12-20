from flask import Flask, render_template, request
import math
from decimal import *

app = Flask(__name__)


def wylicz_kat_beta(ilosc_otworow):
    getcontext().prec = 4
    return Decimal(str(360 / ilosc_otworow))


def znajdz_pierwszy_punkt(alfa, srednica_podzialowa):
    getcontext().prec = 4
    srednica_podzialowa = Decimal(str(srednica_podzialowa))
    promien = srednica_podzialowa / Decimal('2')

    # alfa = Decimal(str(alfa))

    if alfa == 90:
        x = 0.0
        y = float(promien)

    else:

        alfa_rad = Decimal(str(math.radians(alfa)))
        tangens = Decimal(str(math.tan(alfa_rad)))

        x = promien / Decimal(str(math.sqrt(tangens ** 2 + Decimal('1'))))
        y = Decimal(tangens * x)

        x = float(x)
        y = float(y)

    if x < 0.001:
        x = 0.0

    if y < 0.001:
        y = 0.0

    result = (x, y)

    return result


def znajdz_kolejny_punkt(gamma, srednica_podzialowa):
    getcontext().prec = 4
    srednica_podzialowa = Decimal(str(srednica_podzialowa))
    promien = srednica_podzialowa / Decimal('2')

    # gamma = Decimal(str(gamma))

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

        x = float(x)
        y = float(y)

    if x < 0.001:
        x = 0.0

    if y < 0.001:
        y = 0.0

    result = (x, y)

    return result


def znajdz_wszystkie_otwory(ilosc_otworow, alfa, srednica_podzialowa):
    getcontext().prec = 4
    alfa = Decimal(alfa)
    beta = wylicz_kat_beta(ilosc_otworow)
    gamma = alfa + beta

    punkty = []
    punkt_1 = znajdz_pierwszy_punkt(alfa, srednica_podzialowa)
    punkty.append(punkt_1)

    for i in range(0, ilosc_otworow - 1):
        punkt = znajdz_kolejny_punkt(gamma, srednica_podzialowa)
        punkty.append(punkt)
        gamma += beta

    return punkty


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/wylicz_otwory', methods=['GET', 'POST'])
def wylicz_otwory():
    if request.method == 'POST':
        ilosc_otworow = int(request.form['ilosc_otworow'])
        alfa = request.form['alfa']
        srednica_podzialowa = request.form['srednica']

        punkty = znajdz_wszystkie_otwory(ilosc_otworow, alfa, srednica_podzialowa)
        return render_template('wylicz_otwory.html', ilosc_otworow=ilosc_otworow, alfa=alfa,
                               srednica=srednica_podzialowa, punkty=punkty)
