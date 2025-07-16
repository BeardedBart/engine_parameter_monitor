import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date
from lib.imath import *
from lib.alghoritms import pdrow2array
import os, re


def EGTchart(
            df,
            chartDir,
            not_SI=0,
            size_x=11,
            size_y=8,
            thr_val=0.0):
    """
    Funkcja tworząca wykres wartości EGT oraz Wysokości
    w jednostce czasu.
    """
    df.columns = df.iloc[0, :]
    
    reg = re.compile(r"egt\d", re.IGNORECASE)
    egtNames = list(filter(reg.search,df.columns))
    
    egtML = []
    for i in egtNames:
        tempvar = pdrow2array(df,i)
        egtML.append(tempvar)
    
    # Obliczenia czasu
    time = df["Lcl Time"].replace(np.nan, "00:00:00").tolist()
    time.remove("Lcl Time")
    time = np.array(time, dtype="str")

    begin = datetime.strptime(time[4], "%H:%M:%S").time()
    exit = datetime.strptime(time[-1], "%H:%M:%S").time()

    duration = datetime.combine(date.today(), exit) - datetime.combine(
        date.today(), begin)
    duration = duration.seconds
    step = duration / len(time)
    timeAxis = np.arange(0, duration, step)
    #koniec obliczeń czasu
    
    fig, ax1 = plt.subplots()
    # Tworzenie wszystkich linii danych parametrów
    j = 0
    while j < len(egtML):
        ax1.plot(timeAxis,egtML[j], label=f"{egtNames[j]}")
        j += 1
    #Tworzenie linii danych wysokości
    ALT = pdrow2array(df,"AltInd")
    if not_SI == 0:
            ALT = FTtoM(ALT)
    
    if thr_val != 0.0:
        plt.axhline(thr_val, color='r', label="Granica użytkowa")
    
    ax2 = ax1.twinx()
    ax2.plot(timeAxis, ALT, label="Wys.", color="cyan")

    if not_SI == 0:
        ax1.set_ylabel("Temperatura [°C]")
        ax2.set_ylabel("Wysokość [m]")
    else:
        ax1.set_ylabel("Temperatura [°F]")
        ax2.set_ylabel("Wysokość [ft]")

    fig.set_size_inches(size_x, size_y)
    fig.set_dpi(300)
    fig.legend()
    # saving procedure
    save_path = os.path.join(chartDir,"Wykres_EGT.png")
    plt.title("Wykres EGT cylindrów oraz wysokości w funkcji czasu.")
    plt.savefig(save_path, dpi=600, format="png")


def CHTchart(
            df, 
            chartDir, 
            not_SI=0, 
            size_x=11,
            size_y=8,
            thr_val=0.0):
    """
    Funkcja tworząca wykres wartości CHT oraz Wysokości
    w jednostce czasu.
    """
    df.columns = df.iloc[0, :]
    # Wyszukanie wszysktich kolumn parametru
    reg = re.compile(r"cht\d", re.IGNORECASE)
    chtNames = list(filter(reg.search, df.columns))
    # Tworzenie list danych wszystkich parametrów
    chtML = []
    for i in chtNames:
        tempvar = pdrow2array(df, i)
        chtML.append(tempvar)

    # Dane wartości wysokości
    ALT = pdrow2array(df, "AltInd")
    if not_SI == 0:
        ALT = FTtoM(ALT)

    # Obliczenie czasu
    time = df["Lcl Time"].replace(np.nan, "00:00:00").tolist()
    time.remove("Lcl Time")
    time = np.array(time, dtype="str")

    begin = datetime.strptime(time[4], "%H:%M:%S").time()
    exit = datetime.strptime(time[-1], "%H:%M:%S").time()

    duration = datetime.combine(date.today(), exit) - datetime.combine(
        date.today(), begin
    )
    duration = duration.seconds
    step = duration / len(time)
    timeAxis = np.arange(0, duration, step)

    # Inicjalizacja wykresu
    fig, ax1 = plt.subplots()
    # Tworzenie wszystkich linii danych parametru
    j = 0
    while j < len(chtML):
        ax1.plot(timeAxis,chtML[j], label=f"{chtNames[j]}")
        j += 1
    #linia tworzenia wartości granicznej parametru
    if thr_val != 0.0:
        plt.axhline(thr_val, color='r', label="Granica użytkowa")

    ax2 = ax1.twinx()
    ax2.plot(timeAxis, ALT, label="Wys.", color="cyan")

    if not_SI == 0:
        ax1.set_ylabel("Temperatura [°C]")
        ax2.set_ylabel("Wysokość [m]")
    else:
        ax1.set_ylabel("Temperatura [°F]")
        ax2.set_ylabel("Wysokość [ft]")

    fig.set_size_inches(size_x, size_y)
    fig.set_dpi(300)
    fig.legend()
    save_path = os.path.join(chartDir,"Wykres_CHT.png")
    plt.title("Wykres CHT cylindrów oraz wysokości w funkcji czasu.")
    plt.savefig(save_path, dpi=600, format="png")


def OilChart(df, 
            chartDir, 
            not_SI=0,
            size_x=11,
            size_y=8,
            thr_val=0.0):
    """
    Funkcja tworząca wykres wartości ciśnienia
    oraz temperatury oleju w jednostce czasu.
    """
    # df = pd.read_csv(path, low_memory=False, sep=",", encoding="utf-8")

    df.columns = df.iloc[0, :]
    # print(df.columns) # sprawdzenie, czy kolumny się przestawiły

    ### Definicja wartości

    # Dane wartości temperatury oleju.
    # Temp = df["E1 OilT"].replace(np.nan, "0.0").tolist()
    # Temp.remove("E1 OilT")
    # Temp = np.array(Temp, dtype="float16")
    Temp = pdrow2array(df, "E1 OilT")
    if not_SI == 0:
        TempC = FtoC(Temp)

    # Dane wartości ciśnienia oleju.
    # Pressure = df["E1 OilP"].replace(np.nan, "0.0").tolist()
    # Pressure.remove("E1 OilP")
    # Pressure = np.array(Pressure, dtype="float16")
    Pressure = pdrow2array(df, "E1 OilP")
    if not_SI == 0:
        Pressure = PSItoBAR(Pressure)

    # Obliczenia czasowe
    time = df["Lcl Time"].replace(np.nan, "00:00:00").tolist()
    time.remove("Lcl Time")
    time = np.array(time, dtype="str")

    begin = datetime.strptime(time[4], "%H:%M:%S").time()
    exit = datetime.strptime(time[-1], "%H:%M:%S").time()

    duration = datetime.combine(date.today(), exit) - datetime.combine(
        date.today(), begin
    )
    duration = duration.seconds
    step = duration / len(time)

    timeAxis = np.arange(0, duration, step)

    # Inicjalizowanie wykresu
    fig, ax1 = plt.subplots()
    if not_SI == 0:
        ax1.plot(timeAxis, TempC, label="Oil temp")
    else:
        ax1.plot(timeAxis, Temp, label="Oil temp")

    ax1.set_xlabel("Czas [s]")

    ax2 = ax1.twinx()
    ax2.plot(timeAxis, Pressure, color="Orange", label="Oil press")

    if not_SI == 0:
        ax2.set_ylabel("Ciśnienie [bar]")
        ax1.set_ylabel("Temperatura [°C]")
    else:
        ax2.set_ylabel("Ciśnienie [PSI]")
        ax1.set_ylabel("Temperatura [°F]")

    if thr_val != 0.0:
        ax1.axhline(thr_val, color='r', label="Granica użytkowa")

    fig.set_size_inches(size_x , size_y)
    fig.set_dpi(300)
    fig.legend()
    # plt.show()
    
    # basename = os.path.basename(path)
    # basename = basename[0:-4]
    save_path = os.path.join(chartDir,"Wykres_Oil.png")
    plt.title("Wykres temperatury oraz ciśnienia oleju w funkcji czasu.")
    plt.savefig((save_path), dpi=600, format="png")


def WarningChart(i1, 
                 dat1, 
                 ylabel, 
                 chartDir, 
                 name, 
                 title, 
                 xlabel="Czas[s]",
                 thr_val=0.0):
    """
    Kod odpowiadający za tworzenie wykresów zawierających odchylenia
    wartości od podanych zakresów danych (EGT, CHT itd.)

    Argumenty:
        i1 (lista wart. stałych (int)): Indeks/czas danych.
        dat1 (list wart. zmiennoprzecinkowych (float)): Wartości danych.
        not_SI (int, 0): Wybór pomiędzy jednostkami imperialnymi a układem SI.
            Domyślnie ustawione na 0; 1 -> jednoski SI.
    """
    fig, ax = plt.subplots()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.set_size_inches(10.5, 7.5)  # wym. A4 obrócone o 90°
    fig.set_dpi(300)

    if len(i1) == 1 and len(dat1) == 1:
        plt.plot(i1, dat1)
    else:
        for xs, ys in zip(*get_segments(i1, dat1)):
            plt.plot(xs, ys, color="orange")
    # plt.show()
    
    if thr_val != 0.0:
        plt.axhline(thr_val, color='r', label="Granica użytkowa")
    
    plt.title(title)
    plt.savefig(f"{chartDir}/Wykres {name}.png", dpi=600, format="png")


def WarningChartCombined(check_func, 
                         type, 
                         ylabel, 
                         chartDir, 
                         name, 
                         title,
                         thr_val=0.0):
    for i in check_func:
        if i == bool(0):
            i = 0
    i1, d1, i2, d2, i3, d3, i4, d4 = check_func
    fig, ax = plt.subplots()
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel(ylabel)
    fig.set_size_inches(10.5, 7.5)  # A4 rotated 90°
    fig.set_dpi(300)

    label = f"{type}1"
    for xs, ys in zip(*get_segments(i1, d1)):
        plt.plot(xs, ys, color="orange", label=label)
        label = None
    label = f"{type}2"
    for xs, ys in zip(*get_segments(i2, d2)):
        plt.plot(xs, ys, color="blue", label=label)
        label = None
    label = f"{type}3"
    for xs, ys in zip(*get_segments(i3, d3)):
        plt.plot(xs, ys, color="red", label=label)
        label = None
    label = f"{type}4"
    for xs, ys in zip(*get_segments(i4, d4)):
        plt.plot(xs, ys, color="green", label=label)
        label = None
        
    if thr_val != 0.0:
        plt.axhline(thr_val, color='r', label="Granica użytkowa")    
    
    plt.legend()
    # plt.show()
    plt.title(title)
    plt.savefig(f"{chartDir}/Wykres {name}.png", dpi=600, format="png")


def quick_chart(x,y,
                path,
                name,
                ynd=[],
                title=None,
                xlabel=None,
                ylabel=None,
                yndlabel=None,
                width=11,
                height=7,
                dpi=300,
                thr_val=0.0):
    # dodać labele
    fig, ax1 = plt.subplots()
    fig.set_size_inches(width, height)
    fig.set_dpi(dpi)
    
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    
    if thr_val != 0.0:
        plt.axhline(thr_val, color='r', label="Granica użytkowa")
        
    ax1.plot(x,y)
    if len(ynd) != 0:
        ax2 = ax1.twinx()
        ax2.plot(x,ynd)
        ax2.set_ylabel(yndlabel)

    save_path = os.path.join(path,name)
    plt.legend()
    plt.savefig(save_path, dpi=600, format="png")


if __name__ == "__main__":
    print("This is a 'chartgen' module, not a full app")
