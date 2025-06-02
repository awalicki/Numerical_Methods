import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


def wybierz_funkcje(typ_funkcji):
    funkcje = {
        'f(x) = x': lambda x: x,
        'f(x) = |x|': lambda x: np.abs(x),
        'f(x) = x^3 - 2x^2 + 4x - 4': lambda x: x ** 3 - 2 * x ** 2 + 4 * x - 4,
        'f(x) = sin(x)': lambda x: np.sin(x),
        'f(x) = sin(x) + 0.5x': lambda x: np.sin(x) + 0.5 * x
    }
    return funkcje[typ_funkcji]


def simpsons_rule(f, a, b, eps):
    n = 2
    poprzedni_wynik = float("inf")

    while True:
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        fx = f(x)

        suma1 = sum(fx[i] for i in range(2, n, 2))
        suma2 = sum(fx[i] for i in range(1, n, 2))

        wynik = h / 3 * (fx[0] + 2 * suma1 + 4 * suma2 + fx[n])

        if abs(wynik - poprzedni_wynik) < eps:
            return wynik

        poprzedni_wynik = wynik
        n = n * 2

        if n > 1_000_000:
            raise Exception("Za dużo kroków – pętla się nie kończy.")

#generacja wielomianów n - stopień najwyzszego wielomianu, x - punkty dla których obliczamy wartości wielomianów
def legendre_polynomials(n, x):
    P = [np.ones_like(x), x]
    for k in range(1, n):
        P_next = ((2 * k + 1) * x * P[-1] - k * P[-2]) / (k + 1)
        P.append(P_next)
    return P


def wartosc_wielomianu_legendre(x, wspolczynniki):
    n = len(wspolczynniki) - 1
    if n < 0:
        return np.zeros_like(x) #lista zer o długości x
    P = legendre_polynomials(n, x)
    wynik = np.zeros_like(x)
    for i in range(n + 1):
        wynik += wspolczynniki[i] * P[i]
    return wynik #wartości wielomianu aproksymującego dla wszystkich punktów w x


def transformuj_do_minus1_1(x, a, b):
    return 2 * (x - a) / (b - a) - 1


def transformuj_z_minus1_1(x, a, b):
    return 0.5 * ((b - a) * x + (b + a))

#oblicza kolejne współczynniki ck
def aproksymacja_legendre(f, stopien, eps, a, b):
    def calka_legendre(fun, eps):
        return simpsons_rule(fun, -1, 1, eps)

    wsp = []
    for k in range(stopien + 1):
        #wartość wielomianu dla pojedynczego punktu t
        def Pk(t):
            return legendre_polynomials(k, np.array([t]))[k][0]

        def licznik(t):
            x = transformuj_z_minus1_1(t, a, b)
            return f(x) * Pk(t)

        def mianownik(t):
            return Pk(t) ** 2

        licz = calka_legendre(licznik, eps)
        mian = calka_legendre(mianownik, eps)

        wsp.append(licz / mian)
    return wsp


def uruchom_funkcje():
    try:
        typ_funkcji = zmienna_funkcja.get()
        a = float(pole_poczatek.get())
        b = float(pole_koniec.get())
        eps = float(pole_dokladnosc.get())
        stopien = int(pole_stopien.get())

        f = wybierz_funkcje(typ_funkcji)
        wsp = aproksymacja_legendre(f, stopien, eps, a, b)

        x_vals = np.linspace(a, b, 500)
        x_mapped = transformuj_do_minus1_1(x_vals, a, b)
        y_real = f(x_vals)
        y_aprox = wartosc_wielomianu_legendre(x_mapped, wsp)

        plt.figure()
        plt.plot(x_vals, y_real, label="Funkcja")
        plt.plot(x_vals, y_aprox, label="Aproksymacja Legendre'a")
        plt.legend()
        plt.title("Aproksymacja Legendre'a")
        plt.grid(True)
        plt.show()

        def blad_kwadratowy(t):
            x = transformuj_z_minus1_1(t, a, b)
            return (f(x) - wartosc_wielomianu_legendre(t, wsp)) ** 2

        blad = np.sqrt(simpsons_rule(blad_kwadratowy, -1, 1, eps))
        print(f"Błąd aproksymacji: {blad:.6f}")

    except Exception as e:
        messagebox.showerror("Błąd", str(e))


# GUI
okno = tk.Tk()
okno.title("Aproksymacja")

etykieta_funkcja = tk.Label(okno, text="Funkcja:")
etykieta_funkcja.grid(row=0, column=0)
zmienna_funkcja = tk.StringVar(value="f(x) = sin(x)")
menu_funkcja = tk.OptionMenu(okno, zmienna_funkcja,
                             'f(x) = x',
                             'f(x) = |x|',
                             'f(x) = x^3 - 2x^2 + 4x - 4',
                             'f(x) = sin(x)',
                             'f(x) = sin(x) + 0.5x')
menu_funkcja.grid(row=0, column=1)

tk.Label(okno, text="Początek przedziału (a):").grid(row=1, column=0)
pole_poczatek = tk.Entry(okno)
pole_poczatek.grid(row=1, column=1)
pole_poczatek.insert(0, "-2")

tk.Label(okno, text="Koniec przedziału (b):").grid(row=2, column=0)
pole_koniec = tk.Entry(okno)
pole_koniec.grid(row=2, column=1)
pole_koniec.insert(0, "2")

tk.Label(okno, text="Dokładność (eps):").grid(row=3, column=0)
pole_dokladnosc = tk.Entry(okno)
pole_dokladnosc.grid(row=3, column=1)
pole_dokladnosc.insert(0, "0.0001")

tk.Label(okno, text="Stopień wielomianu:").grid(row=4, column=0)
pole_stopien = tk.Entry(okno)
pole_stopien.grid(row=4, column=1)
pole_stopien.insert(0, "4")

przycisk = tk.Button(okno, text="Uruchom", command=uruchom_funkcje)
przycisk.grid(row=5, column=0, columnspan=2, pady=10)

okno.mainloop()