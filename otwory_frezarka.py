from flask import Flask, render_template, request
import math
import matplotlib.pyplot as plt

app = Flask(__name__)


def wylicz_kat_beta(ilosc_otworow):
    return 360 / ilosc_otworow


def znajdz_kolejny_punkt(gamma, srednica_podzialowa):
    promien = srednica_podzialowa / 2

    if gamma == 90:
        x = 0.0
        y = promien

    elif gamma == 270:
        x = 0.0
        y = -promien

    else:

        gamma_rad = math.radians(gamma)
        tangens = math.tan(gamma_rad)

        x_abs = promien / math.sqrt(tangens ** 2 + 1)
        x = -x_abs if 90 < gamma < 270 else x_abs

        y = tangens * x

        x = round(x, 3)
        y = round(y, 3)

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

    promien = srednica_podzialowa / 2
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
            xtext = 5 if xp >= 0 else -3
            ytext = 10 if yp >= 0 else -20
            xytext = (xtext, ytext)

            ha = 'left' if xp >= 0 else 'right'

            plt.annotate(ozn, (xp, yp), textcoords="offset points", xytext=xytext, ha=ha,
                         fontsize='medium', fontweight='bold', color="red")

    plt.savefig('./static/obraz_pogladowy.png', bbox_inches='tight')


def znajdz_wszystkie_otwory(ilosc_otworow, alfa, srednica_podzialowa):
    if srednica_podzialowa < 0 or ilosc_otworow < 0 or alfa < 0:
        return 'Wszystkie pola muszą być dodatnie.'

    elif (ilosc_otworow // 1) != (ilosc_otworow / 1):
        return 'Ilość otworów musi być dodatnią liczbą całkowitą.'

    elif ilosc_otworow == 1 and (alfa > 360 or alfa < 0):
        return 'Przy 1 otworze kąt alfa musi być liczbą z przedziału 0-360.'

    elif (ilosc_otworow == 2 or ilosc_otworow == 3) and (alfa > 180 or alfa < 0):
        return f'Przy {int(ilosc_otworow)} otworach kąt alfa musi być liczbą z przedziału 0-180.'

    elif ilosc_otworow > 3 and (alfa < 0 or alfa > 90):
        return f'Przy {int(ilosc_otworow)} otworach kąt alfa musi być liczbą z przedziału 0-90.'

    ilosc_otworow = int(ilosc_otworow)
    beta = wylicz_kat_beta(ilosc_otworow)
    gamma = alfa

    punkty = []

    for i in range(0, ilosc_otworow):
        punkt = znajdz_kolejny_punkt(gamma, srednica_podzialowa)
        oznaczenie = i + 1
        punkt.append(oznaczenie)
        punkty.append(punkt)
        gamma += beta

    narysuj_obraz_pogladowy(punkty, srednica_podzialowa, alfa, ilosc_otworow)

    return punkty


@app.errorhandler(ValueError)
def server_error(err):
    app.logger.exception(err)
    return render_template('error_page.html'), 500


@app.route('/')
def home():
    return render_template('base.html', alfa=0, ilosc_otworow=2, srednica=1)


@app.route('/wylicz_otwory', methods=['GET', 'POST'])
def wylicz_otwory():
    if request.method == 'POST':
        ilosc_otworow = float(request.form['ilosc_otworow'])
        alfa = float(request.form['alfa'])
        srednica_podzialowa = float(request.form['srednica'])

        punkty = znajdz_wszystkie_otwory(ilosc_otworow, alfa, srednica_podzialowa)
        typ = (type(punkty) == str)

        return render_template('wylicz_otwory.html', ilosc_otworow=ilosc_otworow, alfa=alfa,
                               srednica=srednica_podzialowa, punkty=punkty, typ=typ)
