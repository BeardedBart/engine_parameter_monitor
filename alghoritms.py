import pandas as pd 
import numpy as np



def pdrow2array(file, RowName):
    df = pd.read_csv(file, low_memory=False)
    df.columns=df.iloc[0,:]

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