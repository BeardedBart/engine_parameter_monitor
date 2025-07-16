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


def cal_mean_val(da,step=60):
    # da -> numpy data array 
    output = []
    i = 0
    while i <= len(da):
        if i != len(da) - step:
            tl = [] #temporary list 
            for j in range(step):
                k = i + j
                tl.append(da[k])
            tvar = np.sum(tl)#temporary value
            calc = tvar/step
            output.append(calc)
            i += step
        else:
            tll = [] #temporary 2nd list
            for j in range(step - 1):
                k = i + j
                tll.append(da[k])
            tvar1 = np.sum(tll)
            calcc = tvar1/(step-1)
            output.append(calcc)
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

if __name__ == "__main__":
    print("Wrong direction")