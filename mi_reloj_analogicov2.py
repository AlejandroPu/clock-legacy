# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 04:25:25 2023

@author: retac

Reloj con Tkinter. Fuente: https://youtu.be/HDR3Xy6Zq2g
"""

from tkinter import Canvas, Tk, Frame, LAST
from time import strftime
from math import cos, sin, radians, pi

###### CONFIGURAR según el día

hora_levantarse = 5

###### ###### ###### ###### 

lista_horas = [ num for num in range(hora_levantarse, hora_levantarse+24)]
for index, num in enumerate(lista_horas):
    if num>23: lista_horas[index] = num - 24
lista_normal, lista_cierre, lista_dormir =\
    lista_horas[1:(1+12)], lista_horas[13:(13+3)], lista_horas[16:(16+8)]

# Centro(offset1, offset1) de la onda sinusoide para colocar elementos
extra_offset = 50   # min 0
offset1 = 200 + extra_offset

ventana = Tk()
ventana.title("Organizador de tareas")
ventana.geometry("534x534")
ventana.config( bg = "#031" )
ventana.minsize( width = 534, height = 534 )

ventana.columnconfigure( 0, weight = 1 )
ventana.rowconfigure( 0, weight = 1 )

frame = Frame( ventana, bg="black", relief="sunken" )
frame.grid( column=0, row=0 )

canvas = Canvas( frame, bg="#039", width=500, height=500, relief="raised", bd=10 )
canvas.grid( padx=5, pady=5 )


# Dibujo base del reloj, sin números, agujas, ni círculo central
def dibujar_reloj():
    # Círculo del reloj
    canvas.create_oval( 100, 100, 400, 400, fill="#16d", outline="black", width=4, activeoutline="dark violet", activefill="gray12")
    #círculos pequeños
    radio = 15  #del círculo pequeño
    wave_amp = 170
    for pos in range(3):
        canvas.create_oval(
            (offset1 - radio) + wave_amp*sin(pos*(2*pi/3)),
                (offset1 - radio) - wave_amp*cos(pos*(2*pi/3)),
            (offset1 + radio) + wave_amp*sin(pos*(2*pi/3)),
                (offset1 + radio) - wave_amp*cos(pos*(2*pi/3)),
            fill="green", outline="black", width=3 )
    #triángulo
    canvas.create_polygon(
            250,100,
            380,328,
            120,328,
            fill="#cd6155", outline="black", width=2, activeoutline="yellow", activefill="gray12"
        )
    for dot in range(60):
        canvas.create_text( offset1+140*sin((dot*2*pi)/60),
                           offset1-140*cos((dot*2*pi)/60),
                           text="-", font=( "Arial", 12, "bold" ),fill="deep sky blue")
    for main_dot in range(12):
        #pass
        canvas.create_text( (offset1-1)+140*sin((main_dot*2*pi)/12),
                           (offset1-2)-140*cos((main_dot*2*pi)/12),
                           text="-", font=("Arial", 25, "bold"), fill="#a00" )

def reloj( hour, minute, second, etapa ):
    
    #### colocación de los números en el reloj
    #### y configuración inicial para las agujas del reloj
    
    this_hora = hour # hora en reloj si aguja apuntara en reloj normal
    lista_horas = lista_normal
    cant_horas = 12
    fact_sec2 = 0
    # default es 1, se cambia más adelante para obtener un comportamiento
    # distinto en el segundero
    fact_sec = 1
    # Estilo de los números en el reloj
    font_style = ("Arial", 12, "bold")
    nums_color = "black"
    
    # 1 hora antes del inicio, a la hora de levantarse
    if etapa == "inicio":
        cant_horas = 1
        lista_horas = [hora_levantarse]
    # desde la hora de inicio hasta 12 horas después
    if etapa == "normal":
        fact_sec = 15
        fact_sec2 = minute/15
        this_hora = lista_normal.index(hour)
    # 12 horas después y durante 3 horas
    if etapa == "cierre":
        cant_horas = 3
        this_hora = lista_cierre.index(hour)
        lista_horas = lista_cierre
    # 3 horas después del transcurridas 12 horas desde el inicio
    if etapa == "dormir":
        cant_horas = 8
        lista_horas = lista_dormir
        this_hora = lista_dormir.index(hour)
        

    # Dibujo base del reloj, sin números, agujas, ni círculo central
    dibujar_reloj()
    
    #Colocación números en el reloj
    for i,num in enumerate(lista_horas):
        canvas.create_text( offset1+170*sin((i*2*pi)/cant_horas),
                           offset1-170*cos((i*2*pi)/cant_horas),
                           text=num,
                           font=font_style, fill=nums_color
                    )
    
    # Colocación agujas del reloj
    s_ang = (second/(60*fact_sec)+fact_sec2)*360
    m_ang = (minute/60)*360
    h_ang = ( (this_hora/cant_horas)*360 ) + m_ang/cant_horas

    l_hr = 100; l_min = 120; l_sec = 140
    canvas.create_line(
            250, 250,
                250 + l_hr*sin(radians(h_ang)), 250 - l_hr*cos(radians(h_ang)),
            fill="black", width=12, arrow=LAST
        )
    canvas.create_line(
            250, 250,
                250 + l_min*sin(radians(m_ang)), 250 - l_min*cos(radians(m_ang)),
            fill="#00f", width=6
        )
    canvas.create_line(
            250, 250,
                250 + l_sec*sin(radians(s_ang)), 250 - l_sec*cos(radians(s_ang)),
            fill="red", width=1
        )
    
    # Círculo central
    canvas.create_oval( 243, 243, 257, 257, fill="black", outline="white", width=1 )


def tiempo():

    h = int( strftime("%H") )
    m = int( strftime("%M") )
    s = int( strftime("%S") )
    
    
    if h == hora_levantarse: periodo = "inicio"
    if h in lista_normal: periodo = "normal"
    if h in lista_cierre: periodo = "cierre"
    if h in lista_dormir: periodo = "dormir"
    
    reloj( h, m, s, periodo )
    canvas.after( 1000, tiempo )

tiempo()
ventana.mainloop()
