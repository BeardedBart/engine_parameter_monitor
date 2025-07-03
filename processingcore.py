# CORE responsible for merging code from engineering degree to graduate degree
from flask import Blueprint, render_template, redirect
from flask import g, request, url_for, flash, send_file
from werkzeug.datastructures import FileStorage


processing = Blueprint(__name__, "processing",
                  template_folder="templates",
                  static_folder='static', 
                  static_url_path='/')

PathToDB = 'engparamdb.db'


from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import io, shutil
from datetime import datetime

import sqlite3
import pandas as pd
import pandas.io.common
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
            control_r = mdb.loc[mdb["eng_name"]==eng].to_numpy().tolist()#control row
            # print(control_r) # Tu będzie pozytywne info zwrotne pop up
            flash("Podany silnik istnieje w bazie danych", "lert alert-success fade show")
        else:
            flash("Podany silnik nie istnieje w bazie danych", "alert alert-danger fade show")
            return redirect(url_for("processingcore.upload"))# Tu będzie negatywne info zwrotne pop up
        
        if file.content_type == 'text/csv':
            x,y = 11,7
            
            try:
                df = pd.read_csv(file, low_memory=False)
            except pandas.errors.EmptyDataError:
                flash("Plik CSV jest pusty", "alert alert-danger fade show")
                return redirect(url_for("processingcore.upload"))
            
            df.to_csv(EB,sep=",",mode="w")
            path = os.getcwd()+r"\static"
            
            EGTchart(df,path,size_x=x,size_y=y)
            CHTchart(df,path,size_x=x,size_y=y)
            OilChart(df,path,size_x=x,size_y=y)
            
            tmin = (control_r[0][2]-50)
            tmax = control_r[0][2]
            cOil = checkOil(df,p_val=[1,7],t_val=(tmin, tmax)) # p_val is a test value
            cCHT = checkCHT(df,control_r[0][3])
            cEGT = checkEGT(df,control_r[0][4])
            
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
    data.insert(0, 'czas')
    if request.method == "POST":
        path = os.getcwd()+r"\static"
        x = request.form.get("paramx")
        y = request.form.get("paramy")
        # print(x,y)
        
        if x == 'czas':
            xtemp = dtc(df)
        else:
            xtemp = pdrow2array(df, x) #temporary vars
        ytemp = pdrow2array(df, y)
        
        fig, ax1 = plt.subplots()
        fig.set_size_inches(11, 7)
        fig.set_dpi(300)
        ax1.plot(xtemp, ytemp)
        
        save_path = os.path.join(path,"wa.png")
        plt.savefig(save_path, dpi=600, format="png")
        
        return render_template("pc_nm.html", 
                               tbl=data, 
                               cond=True, 
                               imgg="wa.png")
        
    return render_template("pc_nm.html", tbl=data)
    
    
if __name__ == '__main__':
    print("UUUPSS, WRONG WAY!!")