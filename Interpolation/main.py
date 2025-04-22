import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def f1(x):
    return x

def f2(x):
    return np.abs(x)

def f3(x):
    return x ** 3 - x

def f4(x):
    return np.sin(x)

def wybierz_funkcje(typ_funkcji):
    if typ_funkcji == 'f(x) = x':
        return f1
    elif typ_funkcji == 'f(x) = |x|':
        return f2
    elif typ_funkcji == 'f(x) = x^3 - x':
        return f3
    elif typ_funkcji == 'f(x) = sin(x)':
        return f4
    else:
        raise ValueError("Nieznany typ funkcji")

def wezly_czebyszewa(n, a, b):
    wezly = np.cos((2 * np.arange(1, n + 1) - 1) / (2 * n) * np.pi)
    return 0.5 * (b - a) * (wezly + 1) + a

def dzielone_roznice(x, y):
    n = len(x)
    wspolczynniki = np.copy(y)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            wspolczynniki[i] = (wspolczynniki[i] - wspolczynniki[i - 1]) / (x[i] - x[i - j])
    return wspolczynniki

def interpolacja_newtona(x, wezly_x, wspolczynniki):
    n = len(wezly_x)
    wynik = wspolczynniki[-1]
    for i in range(n - 2, -1, -1):
        wynik = wynik * (x - wezly_x[i]) + wspolczynniki[i]
    return wynik

def rysuj_interpolacje(funkcja, wezly_x, wezly_y, a, b, n):
    x_wartosci = np.linspace(a, b, 1000)
    y_wartosci = funkcja(x_wartosci)

    wspolczynniki = dzielone_roznice(wezly_x, wezly_y)
    wartosci_interp = np.array([interpolacja_newtona(x, wezly_x, wspolczynniki) for x in x_wartosci])

    plt.figure(figsize=(10, 6))
    plt.plot(x_wartosci, y_wartosci, label="Funkcja oryginalna", color="blue")
    plt.plot(x_wartosci, wartosci_interp, label="Wielomian interpolacyjny", color="red")
    plt.scatter(wezly_x, wezly_y, color="green", zorder=5, label="Węzły interpolacyjne")

    for x, y in zip(wezly_x, wezly_y):
        plt.plot([x, x], [0, y], 'k--', linewidth=0.5, alpha=0.5)
        plt.plot(x, y, 'go', markersize=8)

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Interpolacja Newtona ({n} węzłów)')
    plt.grid(True)
    plt.show()

# Interpolacja i rysowanie
def uruchom_interpolacje():
    try:
        typ_funkcji = zmienna_funkcja.get()
        a = float(pole_a.get())
        b = float(pole_b.get())
        n = int(pole_n.get())

        if n <= 0:
            messagebox.showerror("Błąd", "Liczba węzłów musi być dodatnia!")
            return
        if a >= b:
            messagebox.showerror("Błąd", "Początek przedziału musi być mniejszy niż koniec!")
            return

        funkcja = wybierz_funkcje(typ_funkcji)

        wezly_x = wezly_czebyszewa(n, a, b)
        wezly_y = funkcja(wezly_x)
        rysuj_interpolacje(funkcja, wezly_x, wezly_y, a, b, n)

    except ValueError as e:
        messagebox.showerror("Błąd", f"Niepoprawne dane wejściowe: {e}")

# GUI
root = tk.Tk()
root.title("Interpolacja Newtona na węzłach Czebyszewa")

etykieta_funkcji = tk.Label(root, text="Wybierz funkcję:")
etykieta_funkcji.grid(row=0, column=0)

zmienna_funkcja = tk.StringVar(value="f(x) = sin(x)")
opcja_funkcji = ["f(x) = x", "f(x) = |x|", "f(x) = x^3 - x", "f(x) = sin(x)"]
menu_funkcji = tk.OptionMenu(root, zmienna_funkcja, *opcja_funkcji)
menu_funkcji.grid(row=0, column=1)

etykieta_a = tk.Label(root, text="Początek przedziału (a):")
etykieta_a.grid(row=1, column=0)
pole_a = tk.Entry(root)
pole_a.grid(row=1, column=1)
pole_a.insert(0, "-1")

etykieta_b = tk.Label(root, text="Koniec przedziału (b):")
etykieta_b.grid(row=2, column=0)
pole_b = tk.Entry(root)
pole_b.grid(row=2, column=1)
pole_b.insert(0, "1")

etykieta_n = tk.Label(root, text="Liczba węzłów:")
etykieta_n.grid(row=3, column=0)
pole_n = tk.Entry(root)
pole_n.grid(row=3, column=1)
pole_n.insert(0, "5")

przycisk_uruchom = tk.Button(root, text="Uruchom interpolację", command=uruchom_interpolacje)
przycisk_uruchom.grid(row=4, columnspan=2)

root.mainloop()