import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


def wybierz_funkcje(typ_funkcji):
    funkcje = {
        'f(x) = x': lambda x: x,
        'f(x) = |x|': lambda x: np.abs(x),
        'f(x) = x^3 - 2x^2 + 4x - 4': lambda x: x**3 - 2*x**2 + 4*x - 4,
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


def gauss_legendre(f, a, b, nodes):
    dane = {
        2: {
            'xi': [-0.5773502692, 0.5773502692],
            'wi': [1.0, 1.0]
        },
        3: {
            'xi': [-0.7745966692, 0.0, 0.7745966692],
            'wi': [0.5555555556, 0.8888888889, 0.5555555556]
        },
        4: {
            'xi': [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116],
            'wi': [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]
        },
        5: {
            'xi': [-0.9061798459, -0.5384693101, 0.0, 0.5384693101, 0.9061798459],
            'wi': [0.2369268850, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268850]
        }
    }

    if nodes not in dane:
        raise NotImplementedError("Obsługiwane są tylko liczby węzłów: 2, 3, 4, 5")

    xi = dane[nodes]['xi']
    wi = dane[nodes]['wi']
    suma = 0.0

    for i in range(nodes):
        x = 0.5 * (b - a) * xi[i] + 0.5 * (a + b)
        suma += wi[i] * f(x)

    return 0.5 * (b - a) * suma


def legendre_polynomials(n, x):
    if n == 0:
        return [np.ones_like(x)]
    elif n == 1:
        return [np.ones_like(x), x]

    P = [np.ones_like(x), x]
    for k in range(2, n + 1):
        Pk = ((2*k - 1)*x*P[-1] - (k - 1)*P[-2]) / k
        P.append(Pk)
    return P


def wartosc_wielomianu_legendre(x, wspolczynniki):
    n = len(wspolczynniki) - 1
    if n < 0:
        return np.zeros_like(x)

    P = legendre_polynomials(n, x)
    wynik = np.zeros_like(x)
    for i in range(n + 1):
        wynik += wspolczynniki[i] * P[i]
    return wynik


def aproksymacja_legendre(f, a, b, stopien, metoda, param):
    def f_trans(t):
        x = 0.5 * (b - a) * t + 0.5 * (a + b)
        return f(x)

    wsp = []
    for k in range(stopien + 1):
        def Pk(t):
            return legendre_polynomials(k, np.array([t]))[k][0]

        def licznik(t):
            return f_trans(t) * Pk(t)

        def mianownik(t):
            return Pk(t) ** 2

        if metoda == "simpson":
            licz = simpsons_rule(licznik, -1, 1, param)
            mian = simpsons_rule(mianownik, -1, 1, param)
        else:
            licz = gauss_legendre(licznik, -1, 1, int(param))
            mian = gauss_legendre(mianownik, -1, 1, int(param))

        wsp.append(licz / mian)
    return wsp


def uruchom_funkcje():
    try:
        typ_funkcji = zmienna_funkcja.get()
        metoda = zmienna_metoda.get()
        a = float(pole_poczatek.get())
        b = float(pole_koniec.get())
        eps = float(pole_dokladnosc.get())
        stopien = int(pole_stopien.get())

        f = wybierz_funkcje(typ_funkcji)

        if metoda == 'Złożona kwadratura Newtona-Cotesa':
            wsp = aproksymacja_legendre(f, a, b, stopien, "simpson", eps)
        else:
            wsp = aproksymacja_legendre(f, a, b, stopien, "gauss", int(zmienna_lw.get()))

        x_vals = np.linspace(a, b, 500)
        y_real = f(x_vals)
        t_vals = (2 * x_vals - a - b) / (b - a)
        y_aprox = wartosc_wielomianu_legendre(t_vals, wsp)

        plt.figure()
        plt.plot(x_vals, y_real, label="Funkcja")
        plt.plot(x_vals, y_aprox, label="Aproksymacja")
        plt.legend()
        plt.title("Aproksymacja Legendre'a")
        plt.grid(True)
        plt.show()

        def blad_kwadratowy(x):
            t = (2*x - a - b)/(b - a)
            return (f(x) - wartosc_wielomianu_legendre(t, wsp))**2

        if metoda == 'Złożona kwadratura Newtona-Cotesa':
            blad = np.sqrt(simpsons_rule(blad_kwadratowy, a, b, eps))
        else:
            blad = np.sqrt(gauss_legendre(blad_kwadratowy, a, b, int(zmienna_lw.get())))

        print(f"Błąd aproksymacji: {blad:.6f}")

    except Exception as e:
        messagebox.showerror("Błąd", str(e))


def aktualizuj_gui(*args):
    if zmienna_metoda.get() == "Całkowanie na przedziale [a,b)":
        etykieta_lw.grid(row=7, column=0, padx=5, pady=5)
        menu_lw.grid(row=7, column=1, padx=5, pady=5)
    else:
        etykieta_lw.grid_remove()
        menu_lw.grid_remove()


# GUI
okno = tk.Tk()
okno.title("Aproksymacja wielomianowa (Legendre)")

etykieta_metoda = tk.Label(okno, text="Metoda całkowania:")
etykieta_metoda.grid(row=0, column=0)
zmienna_metoda = tk.StringVar(value="Złożona kwadratura Newtona-Cotesa")
menu_metoda = tk.OptionMenu(okno, zmienna_metoda,
                             'Złożona kwadratura Newtona-Cotesa',
                             'Całkowanie na przedziale [a,b)')
menu_metoda.grid(row=0, column=1)

etykieta_funkcja = tk.Label(okno, text="Funkcja:")
etykieta_funkcja.grid(row=1, column=0)
zmienna_funkcja = tk.StringVar(value="f(x) = sin(x)")
menu_funkcja = tk.OptionMenu(okno, zmienna_funkcja,
                             'f(x) = x',
                             'f(x) = |x|',
                             'f(x) = x^3 - 2x^2 + 4x - 4',
                             'f(x) = sin(x)',
                             'f(x) = sin(x) + 0.5x')
menu_funkcja.grid(row=1, column=1)

tk.Label(okno, text="Początek przedziału (a):").grid(row=2, column=0)
pole_poczatek = tk.Entry(okno)
pole_poczatek.grid(row=2, column=1)
pole_poczatek.insert(0, "0")

tk.Label(okno, text="Koniec przedziału (b):").grid(row=3, column=0)
pole_koniec = tk.Entry(okno)
pole_koniec.grid(row=3, column=1)
pole_koniec.insert(0, "1")

tk.Label(okno, text="Dokładność (eps):").grid(row=4, column=0)
pole_dokladnosc = tk.Entry(okno)
pole_dokladnosc.grid(row=4, column=1)
pole_dokladnosc.insert(0, "0.0001")

tk.Label(okno, text="Stopień wielomianu:").grid(row=5, column=0)
pole_stopien = tk.Entry(okno)
pole_stopien.grid(row=5, column=1)
pole_stopien.insert(0, "4")

etykieta_lw = tk.Label(okno, text="Liczba węzłów (Gauss):")
zmienna_lw = tk.StringVar(value="4")
menu_lw = tk.OptionMenu(okno, zmienna_lw, "2", "3", "4", "5")
etykieta_lw.grid_remove()
menu_lw.grid_remove()

przycisk = tk.Button(okno, text="Uruchom", command=uruchom_funkcje)
przycisk.grid(row=6, column=0, columnspan=2, pady=10)

zmienna_metoda.trace_add("write", aktualizuj_gui)

okno.mainloop()
