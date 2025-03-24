import math
import numpy as np
import matplotlib.pyplot as plt

def wybierz_funkcje(typ):
    if typ == "wielomian":
        wspolczynniki = [1, 2, -2, 4]  # Współczynniki dla: x^3 + 2*x^2 - 2*x + 4
        return lambda x: schemat_Hornera(wspolczynniki, x)
    elif typ == "trygonometryczna":
        return lambda x: np.sin(x + 3)
    elif typ == "wykladnicza":
        return lambda x: 2**x - 4
    elif typ == "zlozona":
        wspolczynniki = [1, 2, -2, 4]
        return lambda x: np.cos(schemat_Hornera(wspolczynniki, x))

def modul(x):
    if x<0:
        return -x
    return x

def schemat_Hornera(wspolczynniki, x):
    wynik = wspolczynniki[0]
    for i in range(1, len(wspolczynniki)):
        wynik = wynik * x + wspolczynniki[i]
    return wynik

#Wariant 0
def bisekcja(typ, a, b, war, iteracje, dokladnosc):
    f = wybierz_funkcje(typ)

    if f(a)*f(b)>0:
        return "Podano niepoprawny przedział"
    if f(a) == 0:
        return a
    if f(b) == 0:
        return b

    i = 0
    x0 = (a + b) / 2
    while not(war=="iteracja" and i==iteracje) and not(war=="dokladnosc" and modul(f(x0))<dokladnosc): #Warunki stopu
        x0 = (a+b)/2
        if(f(x0)==0):
            return x0
        elif (f(x0) * f(a) < 0):
            b = x0
        elif(f(x0) * f(b) < 0):
            a = x0
        i += 1

    return (a+b)/2

#Wariant 3
def falsi(typ, a, b, war, iteracje, dokladnosc):
    f = wybierz_funkcje(typ)

    if f(a)*f(b)>0:
        return "Podano niepoprawny przedział"
    if f(a) == 0:
        return a
    if f(b) == 0:
        return b

    i=0
    x0 = a - f(a)*(b-a)/(f(b)-f(a))
    while not (war == "iteracja" and i == iteracje) and not (war == "dokladnosc" and modul(f(x0)) < dokladnosc):  # Warunki stopu
        x0 = a - f(a) * (b - a) / (f(b) - f(a))
        if(f(x0)==0):
            return x0
        elif(f(x0)*f(a)<0):
            b = x0
        elif (f(x0) * f(b) < 0):
            a = x0
        i+=1
    return a - f(a)*(b-a)/(f(b)-f(a))


#Rysowanie wykresow
def rysuj_wykres(typ, a, b, x0, x0_2):
    f = wybierz_funkcje(typ)
    x = np.linspace(a, b, 100)
    y = f(x)


    plt.plot(x, y, color="purple")

    #Osie ukladu wspolrzednych
    plt.axhline(0, color='black', linewidth=0.75)
    plt.axvline(0, color='black', linewidth=0.75)

    #Pkt przeciecia
    if not (f(a) * f(b) > 0):
        plt.plot(x0, f(x0), 'rs', markersize="10")
        plt.plot(x0_2, f(x0_2), 'go', markersize="8")

    #Zakresy
    plt.xlim([a, b])
    plt.ylim([min(y) - 1, max(y) + 1])

    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.title("Wykres funkcji")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show()


#Menu
funkcje = {
    1: "wielomian",
    2: "trygonometryczna",
    3: "wykladnicza",
    4: "zlozona"
}
warunkiStopu = {
    1: "dokladnosc",
    2: "iteracja"
}
print("Podaj na jakiej funkcji chcesz wykonywać operacje: \n 1: x^3 + 2*x^2 - 2*x + 4\n 2: sin(x+3)\n 3: 2^x - 4 \n 4: cos(x^3 + 2*x^2 - 2*x + 4)")
wybor = int(input("Podaj wybor: "))

print("\nPodaj przedział [a,b]")
a = float(input("Podaj a: "))
b = float(input("Podaj b: "))

print("\nWybierz warunek stopu\n 1: Osiągnięcie dokładności obliczeń\n 2: Osięgnięcie określonej liczby iteracji")
stop = int(input("Warunek stopu: "))
if stop == 1:
    dokladnosc = float(input("Podaj dokladnosc: "))
    print("Wynik Bisekcji:", bisekcja(funkcje[wybor], a, b, warunkiStopu[stop], 0, dokladnosc))
    print("Wynik Falsi:", falsi(funkcje[wybor], a, b, warunkiStopu[stop], 0, dokladnosc))
    rysuj_wykres(funkcje[wybor], a, b, falsi(funkcje[wybor], a, b, warunkiStopu[stop], 0, dokladnosc), bisekcja(funkcje[wybor], a, b, warunkiStopu[stop], 0, dokladnosc))
elif stop == 2:
    iteracje = int(input("Podaj ilość iteracji: "))
    print("Wynik Bisekcji:", bisekcja(funkcje[wybor], a, b, warunkiStopu[stop], iteracje, 0))
    print("Wynik Falsi:", falsi(funkcje[wybor], a, b, warunkiStopu[stop], iteracje, 0))
    rysuj_wykres(funkcje[wybor], a, b, falsi(funkcje[wybor], a, b, warunkiStopu[stop], iteracje, 0), bisekcja(funkcje[wybor], a, b, warunkiStopu[stop], iteracje, 0))