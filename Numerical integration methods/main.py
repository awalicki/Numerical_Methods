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
    poprzedni_wynik = float("inf")

    while True:
        h = (b - a) / n
        x = np.linspace(a, b, n + 1) #wektor punktów od a do b
        fx = f(x)

        suma1 = 0 #waga 2
        for i in range(2, n, 2):
            suma1 += fx[i]

        suma2 = 0 #waga 4
        for i in range(1, n, 2):
            suma2 += fx[i]

        wynik = h / 3 * (fx[0] + 2 * suma1 + 4 * suma2 + fx[n])

        if abs(wynik - poprzedni_wynik) < eps:
            return wynik

        poprzedni_wynik = wynik
        n = n * 2

        if n > 1_000_000:
            raise Exception("Za dużo kroków – pętla się nie kończy.")

def gauss_legendre(f, a, b, nodes):
    # Węzły i wagi dla n = 2–5 z tabel wykładowych lub standardowych źródeł
    gauss_data = {
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

    if nodes not in gauss_data:
        raise NotImplementedError(f"Obsługiwane są tylko liczby węzłów: {list(gauss_data.keys())}")

    xi = gauss_data[nodes]['xi']
    wi = gauss_data[nodes]['wi']

    suma = 0.0
    for i in range(nodes):
        x = 0.5 * (b - a) * xi[i] + 0.5 * (a + b)  # transformacja z [-1, 1] do [a, b]
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
            wynik = gauss_legendre(f, a, b, int(zmienna_lw.get()))

        print("Wynik", f"Wynik całkowania ({metoda}):\n{wynik:.8f}")

    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem: {str(e)}")


def aktualizuj_gui(*args):
    if zmienna_metoda.get() == "Całkowanie na przedziale [a,b)":
        etykieta_lw.grid(row=5, column=0, padx=5, pady=5)
        menu_lw.grid(row=5, column=1, padx=5, pady=5)
        przycisk_uruchom.grid(row=6, column=0, columnspan=2, pady=10)
    else:
        etykieta_lw.grid_remove()
        menu_lw.grid_remove()
        przycisk_uruchom.grid(row=5, column=0, columnspan=2, pady=10)


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


etykieta_lw = tk.Label(okno, text="Wybierz liczbę węzłów:")
zmienna_lw = tk.StringVar(value="4")
opcje_wezlow = ["2", "3", "4", "5"]
menu_lw = tk.OptionMenu(okno, zmienna_lw, *opcje_wezlow)

# Ukryj je na starcie
etykieta_lw.grid_remove()
menu_lw.grid_remove()

przycisk_uruchom = tk.Button(okno, text="Uruchom obliczenia", command=uruchom_funkcje)
przycisk_uruchom.grid(row=5, column=0, columnspan=2, pady=10)

zmienna_metoda.trace_add("write", aktualizuj_gui)

okno.mainloop()
