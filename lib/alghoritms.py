import pandas as pd 
import numpy as np
from datetime import datetime, date



def pdrow2array(df, RowName):
    # df.columns=df.iloc[0,:]
    output = df[f'{RowName}'].replace(np.nan, "0.0").tolist()
    output.remove(f"{RowName}")
    output = np.array(output, dtype="float16")
    return output


def tail_convert(da):
    # da -> numpy data array
    # convert data array to make it easily divisible by time unit 
    tv = da[-1]
    step = 60
    t = 0 
    tl = []
    while t < step-(len(da)%step):
        tl.append(tv)
        t+=1
    nda = np.append(da, tl)
    return nda


def cal_mean_val(darr,step=60):
    # da -> numpy data array 
    da = darr.tolist()
    stop = len(da)
    output = []
    i = 0
    while i <= stop:
        if i != len(da) - step:
            tl = float()
            for j in range(step):
                try:
                    tl += da.pop(j)
                except IndexError:
                    k = 0
                    while k < len(da):
                        tl += da.pop(k)
                        k += 1
            calc = tl/step
            output.append(calc)
            i += step
        else:
            break
    return output


def dtc(df):
    # short from Duration Time Calculator
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
    return timeAxis


def grad_calc(data: np.array,step=10):
    i, arr = 0, []
    while i < len(data):
        # print(nCHT1[i])
        arr.append([data[i]])
        i += step

    res = []
    j = 0
    while j < len(arr):
        try:
            calc = (np.array(arr[j+1])-np.array(arr[j]))/step
            res.append(calc[0])
            j += 1
        except IndexError:
            tcalc = (np.array(arr[-1])-np.array(arr[-2]))/step
            res.append(tcalc[0])
            break
    return res

if __name__ == "__main__":
    print("Wrong direction")