# CORE responsible for merging code from engineering degree to graduate degree
from flask import Blueprint, render_template, redirect
from flask import g, request, url_for, flash, send_file


processing = Blueprint(__name__, "processing",
                  template_folder="templates",
                  static_folder='static', 
                  static_url_path='/')

PathToDB = 'engparamdb.db'


from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import io
from datetime import datetime

import sqlite3
import pandas as pd
# import numpy as np
from lib.chartgen import *
from lib.logic import *
from lib.pdfgen import *
from lib.alghoritms import *
import os

import matplotlib.pyplot as plt


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(PathToDB)
        print("DB connected")
    return db


def get_data(cursor):
    data = cursor.execute("""SELECT * FROM engpdb""").fetchall()
    return data


@processing.get("/chartTest")
def chart():
    return render_template("pc_chart.html")


@processing.route("/", methods=['GET', 'POST'])
def upload():
    """ 
        In this section has to be a code responsible
        for analyzing data
    """
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        file = request.files['workfile']
        global EB
        EB = io.StringIO()
        # with open('temp.txt','a+b') as temp:
        #     shutil.copyfileobj(file, temp)
        #     global EB
        #     EB = io.StringIO(temp.read().decode('utf-8'))
        
        temp = get_db() #Master Data Base
        mdb = pd.read_sql_query("SELECT * FROM engpdb",temp)
        eng = request.form.get("eng_name")     
                
        if eng in set(mdb["eng_name"]):
            #control row
            control_r = mdb.loc[mdb["eng_name"]==eng].to_numpy().tolist()[0][2:]
            flash("Podany silnik istnieje w bazie danych", "alert alert-success fade show")
        else:
            flash("Podany silnik nie istnieje w bazie danych", "alert alert-danger fade show")
            return redirect(url_for("processingcore.upload"))
        
        if file.content_type == 'text/csv':
            x,y = 11,7
            
            try:
                df = pd.read_csv(file, low_memory=False)
            except pd.errors.EmptyDataError:
                flash("Plik CSV jest pusty", "alert alert-danger fade show")
                return redirect(url_for("processingcore.upload"))
            
            df.to_csv(EB,sep=",",mode="w")
            path = os.getcwd()+r"\static"
            
            EGTchart(df,path,size_x=x,size_y=y,thr_val=control_r[2])
            CHTchart(df,path,size_x=x,size_y=y,thr_val=control_r[1])
            print(PSItoBAR(control_r[3]),PSItoBAR(control_r[4]))
            OilChart(df,path,size_x=x,size_y=y,t_val=control_r[0], 
                     p_min=PSItoBAR(control_r[3]), 
                     p_max=PSItoBAR(control_r[4])) #TypeError: 'float' object is not iterable
            #inicjacja wykresów pomocniczych
            alt_oat(df,path,size_x=x,size_y=y)
            rpm_ff(df,path,size_x=x,size_y=y)
            
            tmin = (control_r[0]-50)
            tmax = control_r[0]
            cOil = checkOil(df,p_val=[1,7],t_val=(tmin, tmax)) # p_val is a test value
            cCHT = checkCHT(df,control_r[1])
            cEGT = checkEGT(df,control_r[2])
            
            global tempCHT, tempEGT, tempO
            
            tempCHT = []  # temporary param of CHT
            for data in cCHT:
                if data != bool(0):
                    if len(data) != 0 or data == True:
                        tempCHT.append(1)
            if int(1) in tempCHT:
                tempCHT = 1
                WarningChartCombined(
                    cCHT,
                    "CHT",
                    "Temperatura [°C]",
                    path,
                    "AnomalieCHT",
                    "Wykres ponadnormatywnych temperatur CHT",
                    t_val=control_r[1]
                )
            else:
                tempCHT = 0
                
                
            tempEGT = []  # temporary param of EGT
            for data in cEGT:
                if data != bool(0):
                    if len(data) != 0 or data == True:
                        tempEGT.append(1)
            if int(1) in tempEGT:
                tempEGT = 1
                WarningChartCombined(
                    cEGT,
                    "EGT",
                    "Temperatura [°C]",
                    path,
                    "AnomalieEGT",
                    "Wykres ponadnormatywnych temperatur EGT",
                    thr_val=control_r[2]
                )
            else:
                tempEGT = 0


            tempO = []  # temporary param of Oil
            for data in cOil:
                if data != bool(0):
                    if len(data) != 0 or data == True:
                        tempO.append(1)
            if int(1) in tempO:
                tempO = 1
                WarningChart(
                    cOil[0], 
                    cOil[1],
                    "Ciśnienie [bar]", 
                    path, 
                    "AnomalieCiśnienia", 
                    "Wykres ciśnienia oleju"
                )
                WarningChart(
                    cOil[2],
                    cOil[3],
                    "Temperatura [°C]",
                    path,
                    "AnomalieTempOleju",
                    "Wykres temperatury oleju",
                    thr_val=control_r[0]
                )
            else:
                tempO = 0
            print(tempCHT, tempEGT, tempO)
        
        return redirect(url_for("processingcore.chart"))
    

@processing.route('/download',methods=['GET','POST'])
def download():
    buffer = io.BytesIO()
    if request.method == "POST":
        print(tempCHT, tempEGT, tempO)
        cv = Canvas(buffer, pagesize=A4)
        
        FirstPage(cv, saveName, tempCHT, tempEGT, tempO)
        ChartPage(cv, r"static\Wykres_CHT.png")
        ChartPage(cv, r"static\Wykres_EGT.png")
        ChartPage(cv, r"static\Wykres_Oil.png")
        ChartPage(cv, r"static\Wykres AnomalieCiśnienia.png")
        ChartPage(cv, r"static\Wykres AnomalieTempOleju.png")
        # dodanie dodatkowych wykresów do raportu
        ChartPage(cv, r"static\aux1.png")
        ChartPage(cv, r"static\aux2.png")
        
        cv.save() #NOTE: save where?!
        buffer.seek(0)
        
        now = datetime.now().strftime("%d-%m-%Y_%H-%M")
        return send_file(buffer, 
                         as_attachment=True,
                         mimetype="image/pdf",
                         download_name=f"Raport_{now}.pdf")
        
    return render_template("pc_output.html")


@processing.route("/nm", methods=['GET','POST'])
def new_menu():
    #test for a new menu of user wanted data input
    EB.seek(0)
    df = pd.read_csv(EB, low_memory=False)
    # print(df.head())
    df.columns=df.iloc[0,:]
    data = list(df.columns)
    data.insert(1, 'Czas [s]')
    options = (
        "nie",
        "Wartości średnie z okresu 1 min",
        "Gradient przyrostu/spadku"
    )
    if request.method == "POST":
        path = os.getcwd()+r"\static"
        x = request.form.get("paramx")
        y = request.form.get("paramy")
        ynd = request.form.get("param2y")
        optnvar = request.form.get("optnvar")
        step = request.form.get("krok",10, type=int)
        print(step)# zwróci 10, jeżeli nic nie będzie na wejściu
        lingraf = "linia" in request.form
        print(lingraf)
        # lingraf = bool(lingraf)
        mediumt = request.form.get("mediumt",60, type=int)
        # print(x,y)
        
        if x == 'Czas [s]':
            xtemp = dtc(df)
        else:
            xtemp = pdrow2array(df, x) #zmienne "lokalne"
        ytemp = pdrow2array(df, y)
       
        if ynd != "0":
            yndtemp = pdrow2array(df, ynd)
            # quick_chart(xtemp,ytemp,path,"wa.png", yndtemp)
            quick_chart(xtemp,
                        FtoC(ytemp),
                        path,
                        "wa.png",
                        yndtemp,
                        xlabel=x,
                        ylabel=y,
                        yndlabel=ynd)
        else:
            quick_chart(xtemp,
                        FtoC(ytemp),
                        path,
                        "wa.png", 
                        xlabel=x,
                        ylabel=y)

        # NOTE: tworzenie drugiego wykresu
        if optnvar == "Wartości średnie z okresu 1 min":
            sp = 300
            nytemp = FtoC(ytemp)
            nnytemp = tail_convert(ytemp) #nowa tymczasowa zmienna dodatkowa
            yd = cal_mean_val(nnytemp,sp) 
            time_step = np.arange(1,len(yd)+1)
            quick_chart(time_step,
                        yd,path,
                        "cc.png",
                        xlabel=f"Czas co {sp} s",
                        ylabel=y)
        elif optnvar == "Gradient przyrostu/spadku":
            # najpierw weźmy parametr z pierwszej osi y 
            # step - krok, co ile sekund ma być próbkowanie
            ytemp = FtoC(ytemp)
            res = grad_calc(ytemp,step)
            # filtr przeciw początkowym błędnym odczytom
            k = 0
            while k < 10:
                if res[k] > 1:
                    res.pop(k)
                    res.insert(k,np.float64(0))
                k += 1
            # rozpoczęcie lokalnego tworzenia wykresu
            fig, ax1 = plt.subplots()
            x = np.arange(1,len(res)+1,1)
            ax1.plot(x,res,"o")
            ax1.set_xlabel(f"Czas co {step} sek.")
            ax1.set_ylabel("Współczynnik kierunkowy [°F/min]")
            if lingraf == True:
                ax1.axhline(0.5, color="#ff1e00", linestyle='dashed')
                ax1.axhline(-0.5, color="#ff9933", linestyle='dashed')
            # wygląd wykresu
            fig.set_size_inches(11,8)
            fig.set_dpi(300)
            save_path = os.path.join(path,"cc.png")
            plt.savefig(save_path, dpi=600, format="png")
        else:
            print("brak drugiego wykresu")
            
        return render_template("pc_nm.html", 
                               tbl=data,
                               optn=options, 
                               cond=True, 
                               img1="wa.png",
                               img2="cc.png")
        
    return render_template("pc_nm.html", tbl=data, optn=options)
    
    
if __name__ == '__main__':
    print("UUUPSS, WRONG WAY!!")