import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date
from lib.imath import *
import os


def EGTchart(
            df,
            chartDir,
            not_SI=0,
            size_x=11,
            size_y=8,):
    """
    Funkcja tworząca wykres wartości EGT oraz Wysokości
    w jednostce czasu.
    """
    df.columns = df.iloc[0, :]
    # print(df.columns) # sprawdzenie, czy kolumny się przestawiły

    ### Definiowanie wartości

    # Dane wartości poszczególnych EGT
    EGT1 = df["E1 EGT1"].replace(np.nan, "0.0").tolist()
    EGT1.remove("E1 EGT1")
    EGT1 = np.array(EGT1, dtype="float16")
    if not_SI == 0:
        EGT1 = FtoC(EGT1)

    EGT2 = df["E1 EGT2"].replace(np.nan, "0.0").tolist()
    EGT2.remove("E1 EGT2")
    EGT2 = np.array(EGT2, dtype="float16")
    if not_SI == 0:
        EGT2 = FtoC(EGT2)

    EGT3 = df["E1 EGT3"].replace(np.nan, "0.0").tolist()
    EGT3.remove("E1 EGT3")
    EGT3 = np.array(EGT3, dtype="float16")
    if not_SI == 0:
        EGT3 = FtoC(EGT3)

    EGT4 = df["E1 EGT4"].replace(np.nan, "0.0").tolist()
    EGT4.remove("E1 EGT4")
    EGT4 = np.array(EGT4, dtype="float16")
    if not_SI == 0:
        EGT4 = FtoC(EGT4)

    # Dane wartości wysokości
    ALT = df["AltInd"].replace(np.nan, "0.0").tolist()
    ALT.remove("AltInd")
    ALT = np.array(ALT, dtype="float16")
    if not_SI == 0:
        ALT = FTtoM(ALT)

    # Obliczenia czasu
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
    ax1.set_xlabel("Czas [s]")
    ax1.plot(timeAxis, EGT1, label="EGT1")
    ax1.plot(timeAxis, EGT2, label="EGT2")
    ax1.plot(timeAxis, EGT3, label="EGT3")
    ax1.plot(timeAxis, EGT4, label="EGT4")

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
            size_y=8,):
    """
    Funkcja tworząca wykres wartości CHT oraz Wysokości
    w jednostce czasu.
    """
    # df = pd.read_csv(path, low_memory=False, sep=",", encoding="utf-8")
    

    df.columns = df.iloc[0, :]
    # print(df.columns) # sprawdzenie, czy kolumny się przestawiły

    ### Definiowanie wartości

    # Dane wartości poszczególnych CHT
    CHT1 = df["E1 CHT1"].replace(np.nan, "0.0").tolist()
    CHT1.remove("E1 CHT1")
    CHT1 = np.array(CHT1, dtype="float16")
    if not_SI == 0:
        CHT1 = FtoC(CHT1)

    CHT2 = df["E1 CHT2"].replace(np.nan, "0.0").tolist()
    CHT2.remove("E1 CHT2")
    CHT2 = np.array(CHT2, dtype="float16")
    if not_SI == 0:
        CHT2 = FtoC(CHT2)

    CHT3 = df["E1 CHT3"].replace(np.nan, "0.0").tolist()
    CHT3.remove("E1 CHT3")
    CHT3 = np.array(CHT3, dtype="float16")
    if not_SI == 0:
        CHT3 = FtoC(CHT3)

    CHT4 = df["E1 CHT4"].replace(np.nan, "0.0").tolist()
    CHT4.remove("E1 CHT4")
    CHT4 = np.array(CHT4, dtype="float16")
    if not_SI == 0:
        CHT4 = FtoC(CHT4)

    # Dane wartości wysokości
    ALT = df["AltInd"].replace(np.nan, "0.0").tolist()
    ALT.remove("AltInd")
    ALT = np.array(ALT, dtype="float16")
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
    ax1.set_xlabel("Czas [s]")
    ax1.plot(timeAxis, CHT1, label="CHT1")
    ax1.plot(timeAxis, CHT2, label="CHT2")
    ax1.plot(timeAxis, CHT3, label="CHT3")
    ax1.plot(timeAxis, CHT4, label="CHT4")

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
            size_y=8,):
    """
    Funkcja tworząca wykres wartości ciśnienia
    oraz temperatury oleju w jednostce czasu.
    """
    # df = pd.read_csv(path, low_memory=False, sep=",", encoding="utf-8")

    df.columns = df.iloc[0, :]
    # print(df.columns) # sprawdzenie, czy kolumny się przestawiły

    ### Definicja wartości

    # Dane wartości temperatury oleju.
    Temp = df["E1 OilT"].replace(np.nan, "0.0").tolist()
    Temp.remove("E1 OilT")
    Temp = np.array(Temp, dtype="float16")
    if not_SI == 0:
        TempC = FtoC(Temp)

    # Dane wartości ciśnienia oleju.
    Pressure = df["E1 OilP"].replace(np.nan, "0.0").tolist()
    Pressure.remove("E1 OilP")
    Pressure = np.array(Pressure, dtype="float16")
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

    fig.set_size_inches(size_x , size_y)
    fig.set_dpi(300)
    fig.legend()
    # plt.show()

    # basename = os.path.basename(path)
    # basename = basename[0:-4]
    save_path = os.path.join(chartDir,"Wykres_Oil.png")
    plt.title("Wykres temperatury oraz ciśnienia oleju w funkcji czasu.")
    plt.savefig((save_path), dpi=600, format="png")


def WarningChart(i1, dat1, ylabel, chartDir, name, title, xlabel="Czas[s]"):
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
    plt.title(title)
    plt.savefig(f"{chartDir}/Wykres {name}.png", dpi=600, format="png")


def WarningChartCombined(check_func, type, ylabel, chartDir, name, title):
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
    plt.legend()
    # plt.show()
    plt.title(title)
    plt.savefig(f"{chartDir}/Wykres {name}.png", dpi=600, format="png")
