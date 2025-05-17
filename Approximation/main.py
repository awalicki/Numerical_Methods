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


def hermite_polynomials(n, x):
    if n == 0:
        return [np.ones_like(x)]
    elif n == 1:
        return [np.ones_like(x), 2 * x]

    H = [np.ones_like(x), 2 * x]
    for k in range(2, n + 1):
        Hk = 2 * x * H[-1] - 2 * (k - 1) * H[-2]
        H.append(Hk)
    return H


def wartosc_wielomianu_hermite(x, wspolczynniki):
    n = len(wspolczynniki) - 1
    if n < 0:
        return np.zeros_like(x)

    H = hermite_polynomials(n, x)
    wynik = np.zeros_like(x)
    for i in range(n + 1):
        wynik += wspolczynniki[i] * H[i]
    return wynik


def aproksymacja_hermite(f, stopien, eps):
    def funkcja_waga(t):
        return np.exp(-t ** 2)

    def calka_hermite(fun, eps):
        # Całkujemy od -inf do +inf z wagą exp(-x^2)
        # Dla uproszczenia przybliżamy całkę na skończonym przedziale [-bound, bound]
        bound = 5.0  # Wartość wystarczająco duża, bo exp(-5^2) ≈ 1.4e-12
        return simpsons_rule(lambda x: fun(x) * funkcja_waga(x), -bound, bound, eps)

    wsp = []
    for k in range(stopien + 1):
        def Hk(t):
            return hermite_polynomials(k, np.array([t]))[k][0]

        def licznik(t):
            return f(t) * Hk(t)

        def mianownik(t):
            return Hk(t) ** 2

        licz = calka_hermite(licznik, eps)
        mian = calka_hermite(mianownik, eps)

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

        # Aproksymacja Hermite'a działa na całej osi rzeczywistej z wagą exp(-x^2)
        # Dla celów wizualizacji ograniczamy wykres do podanego przedziału [a, b]
        wsp = aproksymacja_hermite(f, stopien, eps)

        x_vals = np.linspace(a, b, 500)
        y_real = f(x_vals)
        y_aprox = wartosc_wielomianu_hermite(x_vals, wsp)

        plt.figure()
        plt.plot(x_vals, y_real, label="Funkcja")
        plt.plot(x_vals, y_aprox, label="Aproksymacja Hermite'a")
        plt.legend()
        plt.title("Aproksymacja Hermite'a")
        plt.grid(True)
        plt.show()

        def blad_kwadratowy(x):
            return (f(x) - wartosc_wielomianu_hermite(x, wsp)) ** 2 * np.exp(-x ** 2)

        # Obliczamy błąd na całej osi rzeczywistej (z wagą)
        bound = 5.0
        blad = np.sqrt(simpsons_rule(blad_kwadratowy, -bound, bound, eps))
        print(f"Błąd aproksymacji: {blad:.6f}")

    except Exception as e:
        messagebox.showerror("Błąd", str(e))


# GUI
okno = tk.Tk()
okno.title("Aproksymacja wielomianowa (Hermite)")

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