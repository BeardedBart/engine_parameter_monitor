# NOTE Library about checking data for potentially dangerous deviation from correct values
import pandas as pd
from lib.imath import *
from lib.chartgen import *


def checkEGT(df, error_val=700):
    # df = pd.read_csv(file, low_memory=False, sep=",")
    # df.columns = df.iloc[0, :]

    EGT1 = df["E1 EGT1"].replace(np.nan, "0.0").tolist()
    EGT1.remove("E1 EGT1")
    EGT1 = np.array(EGT1, dtype="float16")
    EGT1 = FtoC(EGT1)

    EGT2 = df["E1 EGT2"].replace(np.nan, "0.0").tolist()
    EGT2.remove("E1 EGT2")
    EGT2 = np.array(EGT2, dtype="float16")
    EGT2 = FtoC(EGT2)

    EGT3 = df["E1 EGT3"].replace(np.nan, "0.0").tolist()
    EGT3.remove("E1 EGT3")
    EGT3 = np.array(EGT3, dtype="float16")
    EGT3 = FtoC(EGT3)

    EGT4 = df["E1 EGT4"].replace(np.nan, "0.0").tolist()
    EGT4.remove("E1 EGT4")
    EGT4 = np.array(EGT4, dtype="float16")
    EGT4 = FtoC(EGT4)

    # ALT = df["AltInd"].replace(np.nan, "0.0").tolist()
    # ALT.remove("AltInd")
    # ALT = np.array(ALT, dtype="float16")
    # ALT = FTtoM(ALT)

    egt1E = []  # niepożądane wartości EGT
    egt2E = []
    egt3E = []
    egt4E = []

    i1, i2, i3, i4 = [], [], [], []  # indeksy poszczególnych cylindrów

    for index, val in enumerate(EGT1):
        if val > error_val:
            egt1E.append(val)
            i1.append(index)

    for index, val in enumerate(EGT2):
        if val > error_val:
            egt2E.append(val)
            i2.append(index)

    for index, val in enumerate(EGT3):
        if val > error_val:
            egt3E.append(val)
            i3.append(index)

    for index, val in enumerate(EGT4):
        if val > error_val:
            egt4E.append(val)
            i4.append(index)

    if len(egt1E) == 0:
        egt1E = False
        i1 = False

    if len(egt2E) == 0:
        egt2E = False
        i2 = False

    if len(egt3E) == 0:
        egt3E = False
        i3 = False

    if len(egt4E) == 0:
        egt4E = False
        i4 = False

    return i1, egt1E, i2, egt2E, i3, egt3E, i4, egt4E


def checkCHT(df, error_val=170):
    # df = pd.read_csv(file, low_memory=False, sep=",")
    # df.columns = df.iloc[0, :]

    CHT1 = df["E1 CHT1"].replace(np.nan, "0.0").tolist()
    CHT1.remove("E1 CHT1")
    CHT1 = np.array(CHT1, dtype="float16")
    CHT1 = FtoC(CHT1)

    CHT2 = df["E1 CHT2"].replace(np.nan, "0.0").tolist()
    CHT2.remove("E1 CHT2")
    CHT2 = np.array(CHT2, dtype="float16")
    CHT2 = FtoC(CHT2)

    CHT3 = df["E1 CHT3"].replace(np.nan, "0.0").tolist()
    CHT3.remove("E1 CHT3")
    CHT3 = np.array(CHT3, dtype="float16")
    CHT3 = FtoC(CHT3)

    CHT4 = df["E1 CHT4"].replace(np.nan, "0.0").tolist()
    CHT4.remove("E1 CHT4")
    CHT4 = np.array(CHT4, dtype="float16")
    CHT4 = FtoC(CHT4)

    # ALT = df["AltInd"].replace(np.nan, "0.0").tolist()
    # ALT.remove("AltInd")
    # ALT = np.array(ALT, dtype="float16")
    # ALT = FTtoM(ALT)

    cht1E = []  # niepożądane wartości CHT
    cht2E = []
    cht3E = []
    cht4E = []

    i1, i2, i3, i4 = [], [], [], []  # indeksy poszczególnych cylindrów

    for index, val in enumerate(CHT1):
        if val > error_val:
            cht1E.append(val)
            i1.append(index)

    for index, val in enumerate(CHT2):
        if val > error_val:
            cht2E.append(val)
            i2.append(index)

    for index, val in enumerate(CHT3):
        if val > error_val:
            cht3E.append(val)
            i3.append(index)

    for index, val in enumerate(CHT4):
        if val > error_val:
            cht4E.append(val)
            i4.append(index)

    if len(cht1E) == 0:
        cht1E = False
        i1 = False

    if len(cht2E) == 0:
        cht2E = False
        i2 = False

    if len(cht3E) == 0:
        cht3E = False
        i3 = False

    if len(cht4E) == 0:
        cht4E = False
        i4 = False

    return i1, cht1E, i2, cht2E, i3, cht3E, i4, cht4E


def checkOil(df, p_val, t_val):
    # df = pd.read_csv(file, low_memory=False, sep=",")
    # df.columns = df.iloc[0, :]

    # Ciśnienie Oleju [bar]
    OP = df["E1 OilP"].replace(np.nan, "0.0").tolist()
    OP.remove("E1 OilP")
    OP = np.array(OP, dtype="float16")
    OP = PSItoBAR(OP)

    pi = []  # pressure index
    pe = []  # pressure error
    for index, val in enumerate(OP):
        if val > p_val[1] or val < p_val[0]:
            pe.append(val)
            pi.append(index)

    if len(pe) == 0:
        pi = False
        pe = False

    # Temperatura Oleju [C]
    OT = df["E1 OilT"].replace(np.nan, "0.0").tolist()
    OT.remove("E1 OilT")
    OT = np.array(OT, dtype="float16")
    OT = FtoC(OT)

    ti = []  # indeks temperatury
    te = []  # złe wartości temperatury
    for index, val in enumerate(OT):
        if val > t_val[1] or val < t_val[0]:
            te.append(val)
            ti.append(index)

    if len(te) == 0:
        te = False
        ti = False

    return pi, pe, ti, te


if __name__ == "__main__":
    # file = r"C:\Users\polsk\Desktop\Inżynierka\Program\DataMod\log_211221_065717_EPPG_modded.csv"
    # data = list(checkCHT(file))
    # dat2 = list(checkEGT(file))
    # d3 = list(checkOil(file, [1, 7], [50, 110]))
    # print(d3)
    # WarningChart(d3[2], d3[3], "Temperatura [C]")
    # WarningChart(
    #     data[0],
    #     data[1],
    #     "Temperatura [C]",
    #     r"C:\Users\polsk\Desktop\Inżynierka\Program\Charts",
    #     "TEST",
    # )
    # WarningChartCombined(dat2, "EGT", "Temperatura [C]")
    print("Import error")
