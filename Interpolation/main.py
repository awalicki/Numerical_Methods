import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import uuid

# Definicje funkcji
def funkcja_liniowa(x):
    return x

def funkcja_modul(x):
    return np.abs(x)

def funkcja_wielomian(x):
    return x**3 - 2*x**2 + 4*x - 4

def funkcja_trygonometryczna(x):
    return np.sin(x)

def funkcja_zlozona(x):
    return np.sin(x) + 0.5*x

def wybierz_funkcje(typ_funkcji):
    funkcje = {
        'f(x) = x': funkcja_liniowa,
        'f(x) = |x|': funkcja_modul,
        'f(x) = x^3 - 2x^2 + 4x - 4': funkcja_wielomian,
        'f(x) = sin(x)': funkcja_trygonometryczna,
        'f(x) = sin(x) + 0.5x': funkcja_zlozona
    }
    return funkcje[typ_funkcji]

def wezly_czebyszewa(n, poczatek, koniec):
    k = np.arange(n)
    wezly = np.cos((2 * k + 1) * np.pi / (2 * n))
    return 0.5 * (koniec - poczatek) * wezly + 0.5 * (poczatek + koniec)

def roznice_dzielone(x, y):
    n = len(x)
    wspolczynniki = np.copy(y).astype(float)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            wspolczynniki[i] = (wspolczynniki[i] - wspolczynniki[i - 1]) / (x[i] - x[i - j])
    return wspolczynniki

def interpolacja_newtona(x, wezly_x, wspolczynniki):
    n = len(wezly_x)
    wynik = wspolczynniki[n - 1]
    for i in range(n - 2, -1, -1):
        wynik = wynik * (x - wezly_x[i]) + wspolczynniki[i]
    return wynik

def rysuj_interpolacje(f, wezly_x, wezly_y, poczatek, koniec, n, tytul_dodatek=""):
    wartosci_x = np.linspace(poczatek, koniec, 1000)
    wartosci_y = f(wartosci_x)

    wspolczynniki = roznice_dzielone(wezly_x, wezly_y)
    wartosci_interpolowane = np.array([interpolacja_newtona(x, wezly_x, wspolczynniki) for x in wartosci_x])

    plt.figure(figsize=(10, 6))
    plt.plot(wartosci_x, wartosci_y, label="Funkcja oryginalna", color="blue")
    plt.plot(wartosci_x, wartosci_interpolowane, label="Wielomian interpolacyjny", color="red", linestyle="--")
    plt.scatter(wezly_x, wezly_y, color="green", zorder=5, label="Węzły interpolacyjne")

    # Dodaj linie pionowe w węzłach
    for x, y in zip(wezly_x, wezly_y):
        plt.plot([x, x], [min(min(wartosci_y), min(wartosci_interpolowane)), y], 'k--', linewidth=0.5, alpha=0.5)
        plt.plot(x, y, 'go', markersize=8)

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Interpolacja Newtona na Węzłach Czebyszewa (n={n}) {tytul_dodatek}')
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
    if dane.shape[1] < 2:
        messagebox.showerror("Błąd", "Plik CSV musi zawierać co najmniej dwie kolumny (x, y)!")
        return

    x = dane.iloc[:, 0].values.astype(float)
    y = dane.iloc[:, 1].values.astype(float)

    if len(x) < 2:
        messagebox.showerror("Błąd", "Wymagane są co najmniej dwa punkty danych!")
        return

    poczatek, koniec = min(x), max(x)
    n = len(x)
    wspolczynniki = roznice_dzielone(x, y)

    wartosci_x = np.linspace(poczatek, koniec, 1000)
    wartosci_interpolowane = np.array([interpolacja_newtona(xi, x, wspolczynniki) for xi in wartosci_x])

    plt.figure(figsize=(10, 6))
    plt.plot(wartosci_x, wartosci_interpolowane, label="Wielomian interpolacyjny", color="red", linestyle="--")
    plt.scatter(x, y, color="blue", label="Punkty danych")

    for xi, yi in zip(x, y):
        plt.plot([xi, xi], [min(y), yi], 'k--', linewidth=0.5, alpha=0.5)

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Interpolacja Newtona dla Danych z Pliku (n={n})')
    plt.grid(True)
    plt.show()

# GUI
okno = tk.Tk()
okno.title("Interpolacja Newtona na Węzłach Czebyszewa")

# Wybór funkcji
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

# Przedzial
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

# Wezly
etykieta_n = tk.Label(okno, text="Liczba węzłów:")
etykieta_n.grid(row=3, column=0, padx=5, pady=5)
pole_n = tk.Entry(okno)
pole_n.grid(row=3, column=1, padx=5, pady=5)
pole_n.insert(0, "5")

# Przyciski
przycisk_uruchom = tk.Button(okno, text="Uruchom Interpolację", command=uruchom_interpolacje)
przycisk_uruchom.grid(row=4, column=0, columnspan=2, pady=10)

przycisk_wczytaj = tk.Button(okno, text="Wczytaj Dane i Interpoluj", command=wczytaj_i_interpoluj_dane)
przycisk_wczytaj.grid(row=5, column=0, columnspan=2, pady=10)

okno.mainloop()