# NOTE file with useful mathematical operations
import numpy as np


def FtoC(array, decimals=4):
    """
    Funkcja zmieniająca wartości temperatury
    z stopni [F] na stopnie [C]
    """
    newArray = []
    for val in array:
        tv = (val - 32) * (5 / 9)  # tv stands for temporary variable
        newArray.append(tv)
    newArray = np.array(newArray, dtype="float16")
    np.round(newArray, decimals)
    return newArray


def FTtoM(array, decimals=4):
    """
    Funkcja zmieniająca wartości dystansu z [ft] na [m]
    """
    newArray = []
    for val in array:
        tv = val * 0.3048
        newArray.append(tv)
    newArray = np.array(newArray, dtype="float16")
    np.round(newArray, decimals)
    return newArray


def PSItoBAR(array, decimals=4):
    """
    Funkcja zmieniająca wartości
    ciśnienia z [PSI] na [bar]
    """
    newArray = []
    for val in array:
        tv = val * 0.0689475729
        newArray.append(tv)
    newArray = np.array(newArray, dtype="float16")
    np.round(newArray, decimals)
    return newArray


def get_segments(X, Y):
    """
    Funkcja podająca segmenty
    w przerywanej linii danych na wykresie

    Argumenty:
        X (lista): wektor danych
        Y (lista): wektor danych

    Zwraca:
        Zwraca segmenty danych dla rysowanego wykresu
    """
    if X or Y != bool(0):
        if len(X) == 1 and len(Y) == 1:
            return X, Y
        else:
            X = np.array(X)
            Y = np.array(Y)
            diffs = np.abs(X[1:] - X[:-1])
            q075 = np.percentile(diffs, 75)
            valid_points = diffs[diffs <= q075]
            treshold = np.max(valid_points) + 2 * np.std(valid_points)
            split_points = np.concatenate(
                [[0], np.where(diffs > treshold)[0] + 1, [len(X)]]
            )

            xss = [
                X[split_points[i] : split_points[i + 1]]
                for i in range(len(split_points) - 1)
            ]
            yss = [
                Y[split_points[i] : split_points[i + 1]]
                for i in range(len(split_points) - 1)
            ]
            return xss, yss
    else:
        return [0, 0, 0], [0, 0, 0]
