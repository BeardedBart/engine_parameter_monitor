from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os

ps = 0.20  # phrases vertical spacing
pt = 72

src = r"C:\Users\polsk\Desktop\Inżynierka\Program\DataMod\log_211221_065717_EPPG_modded.csv"
name = os.path.basename(src)
saveName = name[0:-11]

cv = Canvas(f"{saveName}.pdf", pagesize=A4)


def FirstPage(cv, name, cht, egt, oil):
    cv.setFont("Times-Bold", 20)
    cv.drawString(0.5 * pt, 10.5 * pt, f"Analiza pliku: {name}")

    if cht == 1:
        cht = "Tak"
    else:
        cht = "Nie"

    if egt == 1:
        egt = "Tak"
    else:
        egt = "Nie"

    if oil == 1:
        oil = "Tak"
    else:
        oil = "Nie"

    cv.setFont("Times-Roman", 12)
    cv.drawString(0.5 * pt, 10 * pt, f"Anomalie CHT: {cht}.")
    cv.drawString(0.5 * pt, (10 - 1 * ps) * pt, f"Anomalie EGT: {egt}.")
    cv.drawString(0.5 * pt, (10 - 2 * ps) * pt, f"Anomalie param. oleju: {oil}.")


def ChartPage(cv, chart):
    cv.showPage()
    cv.setPageSize((11 * inch, 8 * inch))
    cv.drawImage(chart, 0, 0, 11 * pt, 7.5 * pt)


if __name__ == "__main__":
    print("<pdfgen.py> Wywołano plik w zły sposób")
    # FirstPage(cv, name)
    # cv.save()
    # print("PDF rendered!")
