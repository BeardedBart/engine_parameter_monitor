# CORE responsible for merging code from engineering degree to graduate degree
from flask import Blueprint, render_template, redirect
from flask import g, request, url_for, Response


processing = Blueprint(__name__, "processing",
                  template_folder="templates",
                  static_folder='static', 
                  static_url_path='/')

PathToDB = 'engparamdb.db'

import sqlite3
import pandas as pd
# import numpy as np
from lib.chartgen import *
from lib.logic import *
import os 

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(PathToDB)
        print("DB connected")
    return db

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
        
        temp = get_db() #Master Data Base
        mdb = pd.read_sql_query("SELECT * FROM engpdb",temp)
        eng = request.form.get("eng_name")
                
        if eng in set(mdb["eng_name"]):
            control_r = mdb.loc[mdb["eng_name"]==eng].to_numpy().tolist()#control row
            print(control_r) # Tu będzie pozytywne info zwrotne pop up
        else:
            print("Podany silnik nie istnieje w bazie danych") # Tu będzie negatywne info zwrotne pop up

        
        if file.content_type == 'text/csv':
            x,y = 11,7
            ftu = file
            df = pd.read_csv(ftu, low_memory=False)
            path = os.getcwd()+r"\static"
            
            EGTchart(df,path,size_x=x,size_y=y)
            CHTchart(df,path,size_x=x,size_y=y)
            OilChart(df,path,size_x=x,size_y=y)
            
            tmin = (control_r[0][2]-50)
            tmax = control_r[0][2]
            cOil = checkOil(df,p_val=[1,7],t_val=(tmin, tmax)) # p_val is a test value
            cCHT = checkCHT(df,control_r[0][3])
            cEGT = checkEGT(df,control_r[0][4])
            
            
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
            
            
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheet.sheet' or file.content_type == 'application/vnd.ms-excel':
            df = pd.read_excel(file)
            
        return redirect(url_for("processingcore.chart"))

if __name__ == '__main__':
    print("UUUPSS, WRONG WAY!!")