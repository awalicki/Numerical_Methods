import numpy as np
import tkinter as tk
from tkinter import messagebox


def wybierz_funkcje(typ_funkcji):
    funkcje = {
        'f(x) = x': lambda x: x,
        'f(x) = |x|': lambda x: np.abs(x),
        'f(x) = x^3 - 2x^2 + 4x - 4': lambda x: x**3 - 2*x**2 + 4*x - 4,
        'f(x) = sin(x)': lambda x: np.sin(x),
        'f(x) = sin(x) + 0.5x': lambda x: np.sin(x) + 0.5*x
    }
    return funkcje[typ_funkcji]

def simpsons_rule(f, a, b, eps):
    n = 2
    last_result = float("inf")

    while True:
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        fx = f(x)

        suma1 = 0
        for i in range(2, n, 2):
            suma1 += fx[i]

        suma2 = 0
        for i in range(1, n, 2):
            suma2 += fx[i]

        wynik = h / 3 * (fx[0] + 2 * suma1 + 4 * suma2 + fx[n])

        if abs(wynik - last_result) < eps:
            return wynik

        last_result = wynik
        n = n * 2

        if n > 1_000_000:
            raise Exception("Za dużo kroków – pętla się nie kończy.")


def gauss_legendre(f, a, b, nodes=4):
    if nodes != 4:
        raise NotImplementedError("Obecnie zaimplementowano tylko wersję 4-punktową")

    # Ręcznie podane węzły xi i wagi wi dla 4-punktowej kwadratury Gaussa-Legendre'a
    xi = [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116]
    wi = [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]

    suma = 0
    for i in range(nodes):
        # Przeskalowanie xi z [-1, 1] na [a, b]
        x = 0.5 * (b - a) * xi[i] + 0.5 * (b + a)
        suma += wi[i] * f(x)

    return 0.5 * (b - a) * suma


def uruchom_funkcje():
    try:
        typ_funkcji = zmienna_funkcja.get()
        metoda = zmienna_metoda.get()
        a = float(pole_poczatek.get())
        b = float(pole_koniec.get())
        eps = float(pole_dokladnosc.get())

        if eps <= 0:
            messagebox.showerror("Błąd", "Dokładność musi być większa od zera!")
            return
        if a >= b:
            messagebox.showerror("Błąd", "Początek przedziału musi być mniejszy niż koniec!")
            return

        f = wybierz_funkcje(typ_funkcji)

        if metoda == 'Złożona kwadratura Newtona-Cotesa':
            wynik = simpsons_rule(f, a, b, eps)
        else:
            wynik = gauss_legendre(f, a, b, nodes=4)

        print("Wynik", f"Wynik całkowania ({metoda}):\n{wynik:.8f}")

    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem: {str(e)}")


# Interfejs graficzny
okno = tk.Tk()
okno.title("Metody całkowania numerycznego")

etykieta_metoda = tk.Label(okno, text="Wybierz metodę:")
etykieta_metoda.grid(row=0, column=0, padx=5, pady=5)
zmienna_metoda = tk.StringVar(value="Złożona kwadratura Newtona-Cotesa")
opcje_metoda = [
    'Złożona kwadratura Newtona-Cotesa',
    'Całkowanie na przedziale [a,b)'
]
menu_metoda = tk.OptionMenu(okno, zmienna_metoda, *opcje_metoda)
menu_metoda.grid(row=0, column=1, padx=5, pady=5)

etykieta_funkcja = tk.Label(okno, text="Wybierz funkcję:")
etykieta_funkcja.grid(row=1, column=0, padx=5, pady=5)
zmienna_funkcja = tk.StringVar(value="f(x) = sin(x)")
opcje_funkcji = [
    'f(x) = x',
    'f(x) = |x|',
    'f(x) = x^3 - 2x^2 + 4x - 4',
    'f(x) = sin(x)',
    'f(x) = sin(x) + 0.5x'
]
menu_funkcji = tk.OptionMenu(okno, zmienna_funkcja, *opcje_funkcji)
menu_funkcji.grid(row=1, column=1, padx=5, pady=5)

etykieta_poczatek = tk.Label(okno, text="Początek przedziału (a):")
etykieta_poczatek.grid(row=2, column=0, padx=5, pady=5)
pole_poczatek = tk.Entry(okno)
pole_poczatek.grid(row=2, column=1, padx=5, pady=5)
pole_poczatek.insert(0, "0")

etykieta_koniec = tk.Label(okno, text="Koniec przedziału (b):")
etykieta_koniec.grid(row=3, column=0, padx=5, pady=5)
pole_koniec = tk.Entry(okno)
pole_koniec.grid(row=3, column=1, padx=5, pady=5)
pole_koniec.insert(0, "1")

etykieta_dokladnosc = tk.Label(okno, text="Dokładność (Simpson):")
etykieta_dokladnosc.grid(row=4, column=0, padx=5, pady=5)
pole_dokladnosc = tk.Entry(okno)
pole_dokladnosc.grid(row=4, column=1, padx=5, pady=5)
pole_dokladnosc.insert(0, "0.0001")

przycisk_uruchom = tk.Button(okno, text="Uruchom obliczenia", command=uruchom_funkcje)
przycisk_uruchom.grid(row=5, column=0, columnspan=2, pady=10)

okno.mainloop()
