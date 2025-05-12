# CORE responsible for merging code from engineering degree to graduate degree
from flask import Blueprint, render_template, redirect
from flask import g, request, url_for, Response


processing = Blueprint(__name__, "processing",
                  template_folder="templates",
                  static_folder='static', 
                  static_url_path='/')


import pandas as pd
import numpy as np
from lib.chartgen import *
import os 


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
        
        if file.content_type == 'text/csv':
            x,y = 5,3
            ftu = file
            df = pd.read_csv(ftu)
            path = os.getcwd()+r"\static"
            EGTchart(df,path,size_x=x,size_y=y)
            CHTchart(df,path,size_x=x,size_y=y)
            OilChart(df,path,size_x=x,size_y=y)
            
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheet.sheet' or file.content_type == 'application/vnd.ms-excel':
            df = pd.read_excel(file)
            
        return redirect(url_for("processingcore.chart"))

if __name__ == '__main__':
    print("UUUPSS, WRONG WAY!!")