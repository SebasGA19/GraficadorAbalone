# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 13:59:27 2022

@author: Repre
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas
from matplotlib import pyplot
import numpy as np
import scipy.stats
import statistics
from scipy.stats import skew

root = tk.Tk()
abalone = pandas.read_csv("./abalone.csv")
columnas = (
    "sex",
    "length",
    "diameter",
    "height",
    "whole weight",
    "shucked weight",
    "viscera weight",
    "shell weight",
    "rings"
)
columnas_numericas = (
    "length",
    "diameter",
    "height",
    "whole weight",
    "shucked weight",
    "viscera weight",
    "shell weight",
    "rings"
)
columnas_dispersion = (
    "length",
    "diameter",
    "height"
)
columnas_dispersion_vs = (
    "whole weight",
    "shucked weight",
    "viscera weight",
    "shell weight",
    "rings"
)

def sin_atipicos():
    abalone_limpio = abalone.copy()
    filas_atipicas = set()
    for columna in columnas_numericas:
        datos = abalone[columna]
        q1 = np.percentile(datos, 25)
        q3 = np.percentile(datos, 75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        for index, value in enumerate(datos):
            if value < limite_inferior or limite_superior < value:
                filas_atipicas.add(index)
    filas_atipicas = list(filas_atipicas)
    filas_atipicas.sort()
    abalone_limpio = abalone_limpio.drop(index=filas_atipicas)
    return abalone_limpio

abalone_limpio = sin_atipicos()
# Variables

histograma_v = tk.StringVar()
boxplot_v = tk.StringVar()
normal_v = tk.StringVar()
probplot_v = tk.StringVar()
scatter_v = tk.StringVar()
scatter_vs_v = tk.StringVar()

# 
def histograma(atipicos):
    nombre_columna = histograma_v.get()
    if(atipicos==False):
        column = abalone[nombre_columna]
    else:
        column = abalone_limpio[nombre_columna]
    pyplot.hist(column)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()
    
def boxplot(atipicos):
    nombre_columna = boxplot_v.get()
    if(atipicos==False):
        column = abalone[nombre_columna]
    else:
        column = abalone_limpio[nombre_columna]
    pyplot.boxplot(column)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()
    
def prob_plot(atipicos):
    nombre_columna = probplot_v.get()
    if(atipicos==False):
        column = abalone[nombre_columna]
    else:
        column = abalone_limpio[nombre_columna]
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    scipy.stats.probplot(column, dist=scipy.stats.norm,plot=ax)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()
    
def dist_normal(atipicos):
    nombre_columna = normal_v.get()
    if(atipicos==False):
        column = abalone[nombre_columna]
    else:
        column = abalone_limpio[nombre_columna]
    media = np.mean(column)
    desv_std = np.std(column)
    lista = sorted(list(set(column)))
    normal = scipy.stats.norm.pdf(lista, media, desv_std)
    pyplot.plot(lista, normal, )
    pyplot.show()
    pyplot.cla()
    pyplot.clf()
    
def scatter_plot(atipicos):
    nombre_columna = scatter_v.get()
    nombre_columna_vs = scatter_vs_v.get()
    if(atipicos==False):
        datos = abalone
        
    else:
        datos = abalone_limpio
        
    column = datos[nombre_columna]
    column_vs = datos[nombre_columna_vs]
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    pyplot.scatter(column, column_vs)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()
    

media_mediana_etc = tk.StringVar()
media_v = tk.StringVar()
mediana_v = tk.StringVar()
moda_v = tk.StringVar()
kurtosis_v = tk.StringVar()
sesgo_v = tk.StringVar()
kurtosis_c_v = tk.StringVar()
asimetria_v = tk.StringVar()
def datos_estadisticos(atipicos):
    nombre_columna = media_mediana_etc.get()
    if(atipicos==False):
        column=abalone[nombre_columna]
    else:
        column=abalone_limpio[nombre_columna]
    
    media = np.mean(column)
    mediana = np.median(column)
    moda = statistics.mode(column)
    kurtosis = scipy.stats.kurtosis(column)
    asimetria = column.skew()
    
    media_v.set(f"{media}")
    mediana_v.set(f"{mediana}")
    moda_v.set(f"{moda}")
    kurtosis_v.set(f"{kurtosis}")
    asimetria_v.set(f"{asimetria}")
    
    if(moda < mediana < media):
        sesgo_v.set("Sesgada a la izquierda")
    elif(moda > mediana > media):
        sesgo_v.set("Sesgada a la derecha")
        
    if(kurtosis ==0):
        kurtosis_c_v.set("Mesocurtica")
    elif(kurtosis >0):
        kurtosis_c_v.set("Leptocurtica")
    elif(kurtosis <0):
        kurtosis_c_v.set("Platicurtica")
    

root.title("Regresion de abalones")
root.geometry("1080x1600")

#Graficas datos normales
#Histograma


tk.Label(root, text="Datos normales").place(x=10,y=10)
tk.Label(root, text="Histograma").place(x=10,y=40)
ttk.Combobox(root, values=columnas, textvariable=histograma_v).place(x=10,y=70)
tk.Button(root, text="Graficar", command= lambda: histograma(False)).place(x=10,y=100)


tk.Label(root, text="Boxplot").place(x=10,y=130)
ttk.Combobox(root, values=columnas, textvariable=boxplot_v).place(x=10,y=160)
tk.Button(root, text="Graficar", command= lambda: boxplot(False)).place(x=10,y=190)


tk.Label(root, text="Probability plot").place(x=10,y=220)
ttk.Combobox(root, values=columnas, textvariable=probplot_v).place(x=10,y=250)
tk.Button(root, text="Graficar", command= lambda: prob_plot(False)).place(x=10,y=280)


tk.Label(root, text="Distribución normal").place(x=10,y=310)
ttk.Combobox(root, values=columnas, textvariable=normal_v).place(x=10,y=340)
tk.Button(root, text="Graficar", command= lambda: dist_normal(False)).place(x=10,y=370)


tk.Label(root, text="Scatter").place(x=10,y=460)
ttk.Combobox(root, values=columnas_dispersion, textvariable=scatter_v).place(x=10,y=490)
tk.Label(root, text="VS:").place(x=10,y=520)
ttk.Combobox(root, values=columnas_dispersion_vs, textvariable=scatter_vs_v).place(x=10,y=550)
tk.Button(root, text="Graficar", command=lambda: scatter_plot(False)).place(x=10,y=580)


ttk.Combobox(root, values=columnas_numericas, textvariable=media_mediana_etc).place(x=10,y=610)
tk.Button(root, text="Calcular", command= lambda: datos_estadisticos(False)).place(x=10,y=640)

tk.Label(root,text= "Media").place(x=10,y=670)
tk.Label(root,textvariable=media_v).place(x=10,y=700)
tk.Label(root,text= "Mediana").place(x=10,y=730)
tk.Label(root,textvariable=mediana_v).place(x=10,y=760)
tk.Label(root,text= "Moda").place(x=10,y=790)
tk.Label(root,textvariable=moda_v).place(x=10,y=820)
tk.Label(root,text= "Kurtosis").place(x=10,y=850)
tk.Label(root,textvariable=kurtosis_v).place(x=10,y=880)
tk.Label(root,text= "Asimetria").place(x=400,y=910)
tk.Label(root,textvariable=asimetria_v).place(x=400,y=940)
tk.Label(root,text= "Sesgo y Kurtosis").place(x=10,y=970)
tk.Label(root,textvariable=sesgo_v).place(x=10,y=1000)
tk.Label(root,textvariable=kurtosis_c_v).place(x=200,y=1000)


# Datos sin atipicos
tk.Label(root, text="Datos sin atipicos").place(x=400,y=10)
tk.Label(root, text="Histograma").place(x=400,y=40)
ttk.Combobox(root, values=columnas, textvariable=histograma_v).place(x=400,y=70)
tk.Button(root, text="Graficar", command= lambda: histograma(True)).place(x=400,y=100)


tk.Label(root, text="Boxplot").place(x=400,y=130)
ttk.Combobox(root, values=columnas, textvariable=boxplot_v).place(x=400,y=160)
tk.Button(root, text="Graficar", command= lambda: boxplot(True)).place(x=400,y=190)


tk.Label(root, text="Probability plot").place(x=400,y=220)
ttk.Combobox(root, values=columnas, textvariable=probplot_v).place(x=400,y=250)
tk.Button(root, text="Graficar", command= lambda: prob_plot(True)).place(x=400,y=280)


tk.Label(root, text="Distribución normal").place(x=400,y=310)
ttk.Combobox(root, values=columnas, textvariable=normal_v).place(x=400,y=340)
tk.Button(root, text="Graficar", command= lambda: dist_normal(True)).place(x=400,y=370)


tk.Label(root, text="Scatter").place(x=400,y=460)
ttk.Combobox(root, values=columnas_dispersion, textvariable=scatter_v).place(x=400,y=490)
tk.Label(root, text="VS:").place(x=400,y=520)
ttk.Combobox(root, values=columnas_dispersion_vs, textvariable=scatter_vs_v).place(x=400,y=550)
tk.Button(root, text="Graficar", command=lambda: scatter_plot(True)).place(x=400,y=580)


ttk.Combobox(root, values=columnas_numericas, textvariable=media_mediana_etc).place(x=400,y=610)
tk.Button(root, text="Calcular", command= lambda: datos_estadisticos(True)).place(x=400,y=640)

tk.Label(root,text= "Media").place(x=400,y=670)
tk.Label(root,textvariable=media_v).place(x=400,y=700)
tk.Label(root,text= "Mediana").place(x=400,y=730)
tk.Label(root,textvariable=mediana_v).place(x=400,y=760)
tk.Label(root,text= "Moda").place(x=400,y=790)
tk.Label(root,textvariable=moda_v).place(x=400,y=820)
tk.Label(root,text= "Kurtosis").place(x=400,y=850)
tk.Label(root,textvariable=kurtosis_v).place(x=400,y=880)
tk.Label(root,text= "Asimetria").place(x=400,y=910)
tk.Label(root,textvariable=asimetria_v).place(x=400,y=940)
tk.Label(root,text= "Sesgo y Kurtosis").place(x=400,y=970)
tk.Label(root,textvariable=sesgo_v).place(x=400,y=1000)
tk.Label(root,textvariable=kurtosis_c_v).place(x=600,y=1000)


root.mainloop()