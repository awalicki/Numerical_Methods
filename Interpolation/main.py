import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd

def wybierz_funkcje(typ_funkcji):
    funkcje = {
        'f(x) = x': lambda x: x,
        'f(x) = |x|': lambda x: np.abs(x),
        'f(x) = x^3 - 2x^2 + 4x - 4': lambda x: x**3 - 2*x**2 + 4*x - 4,
        'f(x) = sin(x)': lambda x: np.sin(x),
        'f(x) = sin(x) + 0.5x': lambda x: np.sin(x) + 0.5*x
    }
    return funkcje[typ_funkcji]

def wezly_czebyszewa(n, poczatek, koniec):
    k = np.arange(n)
    wezly = np.cos((2 * k + 1) * np.pi / (2 * n + 1))
    return 0.5 * (koniec - poczatek) * wezly + 0.5 * (poczatek + koniec)

def interpolacja_newtona(x, wezly_x, wspolczynniki):
    n = len(wezly_x)
    wynik = wspolczynniki[n - 1]
    for i in range(n - 2, -1, -1):
        wynik = wynik * (x - wezly_x[i]) + wspolczynniki[i]
    return wynik

def roznice_dzielone(x, y):
    n = len(x)
    wspolczynniki = np.copy(y).astype(float)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            wspolczynniki[i] = (wspolczynniki[i] - wspolczynniki[i - 1]) / (x[i] - x[i - j])
    return wspolczynniki

def rysuj_interpolacje(f, wezly_x, wezly_y, poczatek, koniec, n):
    wartosci_x = np.linspace(poczatek, koniec, 1000)
    wartosci_y = f(wartosci_x)

    wspolczynniki = roznice_dzielone(wezly_x, wezly_y)
    wartosci_interpolowane = np.array([interpolacja_newtona(x, wezly_x, wspolczynniki) for x in wartosci_x])

    plt.figure(figsize=(10, 6))
    plt.plot(wartosci_x, wartosci_y, label="Funkcja oryginalna", color="blue")
    plt.plot(wartosci_x, wartosci_interpolowane, label="Wielomian interpolacyjny", color="red", linestyle="--")
    plt.scatter(wezly_x, wezly_y, color="green", zorder=5, label="Węzły interpolacyjne")

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Interpolacja Newtona na Węzłach Czebyszewa (n={n})')
    plt.grid(True)
    plt.show()

def uruchom_interpolacje():
    typ_funkcji = zmienna_funkcja.get()
    poczatek = float(pole_poczatek.get())
    koniec = float(pole_koniec.get())
    n = int(pole_n.get())

    if n <= 0:
        messagebox.showerror("Błąd", "Liczba węzłów musi być dodatnia!")
        return
    if poczatek >= koniec:
        messagebox.showerror("Błąd", "Początek przedziału musi być mniejszy niż koniec!")
        return

    f = wybierz_funkcje(typ_funkcji)
    wezly_x = wezly_czebyszewa(n, poczatek, koniec)
    wezly_y = f(wezly_x)
    rysuj_interpolacje(f, wezly_x, wezly_y, poczatek, koniec, n)

def wczytaj_i_interpoluj_dane():
    sciezka_pliku = filedialog.askopenfilename(
        title="Wybierz plik",
        filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
    )
    if not sciezka_pliku:
        return

    dane = pd.read_csv(sciezka_pliku, header=None)
    x = dane.iloc[:, 0].values.astype(float)
    y = dane.iloc[:, 1].values.astype(float)

    poczatek, koniec = min(x), max(x)
    n = len(x)
    wspolczynniki = roznice_dzielone(x, y)

    wartosci_x = np.linspace(poczatek, koniec, 1000)
    wartosci_interpolowane = np.array([interpolacja_newtona(xi, x, wspolczynniki) for xi in wartosci_x])

    plt.figure(figsize=(10, 6))
    plt.plot(wartosci_x, wartosci_interpolowane, label="Wielomian interpolacyjny", color="red", linestyle="--")
    plt.scatter(x, y, color="blue", label="Punkty danych")

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Interpolacja Newtona dla Danych z Pliku (n={n})')
    plt.grid(True)
    plt.show()

# GUI
okno = tk.Tk()
okno.title("Interpolacja Newtona na Węzłach Czebyszewa")

etykieta_funkcja = tk.Label(okno, text="Wybierz funkcję:")
etykieta_funkcja.grid(row=0, column=0, padx=5, pady=5)
zmienna_funkcja = tk.StringVar(value="f(x) = sin(x)")
opcje_funkcji = [
    'f(x) = x',
    'f(x) = |x|',
    'f(x) = x^3 - 2x^2 + 4x - 4',
    'f(x) = sin(x)',
    'f(x) = sin(x) + 0.5x'
]
menu_funkcji = tk.OptionMenu(okno, zmienna_funkcja, *opcje_funkcji)
menu_funkcji.grid(row=0, column=1, padx=5, pady=5)

etykieta_poczatek = tk.Label(okno, text="Początek przedziału (a):")
etykieta_poczatek.grid(row=1, column=0, padx=5, pady=5)
pole_poczatek = tk.Entry(okno)
pole_poczatek.grid(row=1, column=1, padx=5, pady=5)
pole_poczatek.insert(0, "-3")

etykieta_koniec = tk.Label(okno, text="Koniec przedziału (b):")
etykieta_koniec.grid(row=2, column=0, padx=5, pady=5)
pole_koniec = tk.Entry(okno)
pole_koniec.grid(row=2, column=1, padx=5, pady=5)
pole_koniec.insert(0, "3")

etykieta_n = tk.Label(okno, text="Liczba węzłów:")
etykieta_n.grid(row=3, column=0, padx=5, pady=5)
pole_n = tk.Entry(okno)
pole_n.grid(row=3, column=1, padx=5, pady=5)
pole_n.insert(0, "5")

przycisk_uruchom = tk.Button(okno, text="Uruchom Interpolację", command=uruchom_interpolacje)
przycisk_uruchom.grid(row=4, column=0, columnspan=2, pady=10)

przycisk_wczytaj = tk.Button(okno, text="Wczytaj Dane i Interpoluj", command=wczytaj_i_interpoluj_dane)
przycisk_wczytaj.grid(row=5, column=0, columnspan=2, pady=10)

okno.mainloop()