
import tkinter as tk
import os
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from codigos_cadenas import Pixel

ventana = tk.Tk()
ventana.title("Code Chain")
mainframe = tk.Frame(ventana)# se crea el frame
mainframe.pack() #se empaqueta para que se pueda mostrar, tiene mas parametros para personalziar
mainframe.config(bg="#38403D") #color del frame color gris
mainframe.config(width="1800", height="795")#alto y ancho de Frame

ventana.state('zoomed')


fuente_arial=("Arial", 10)

directorio_actual = os.path.dirname(__file__)

ruta_relativa = os.path.join(directorio_actual, "imagen_blanco.jpg")

img_open = Image.open(ruta_relativa)
image = ImageTk.PhotoImage(img_open)

# Mostrar la imagen en un Label (Tu código original)
label = ttk.Label(mainframe, image=image)
label.place(relx=0.02, rely=0.02)

img_open2 = Image.open(ruta_relativa)
image2 = ImageTk.PhotoImage(img_open2)

# Mostrar la imagen en un Label
label_2 = ttk.Label(mainframe, image=image2)
label_2.place(relx=0.02,rely=0.53)

pixeles = Pixel()

boton_abrir_imagen= tk.Button(mainframe,width=10,height=1, text="Abrir imagen", command=lambda: pixeles.cargar_imagen(label), font=fuente_arial)
boton_abrir_imagen.place(relx=0.1,rely=0.48)


#=============================== Seccion 1 =========================================================

etiqueta_label_contornos = tk.Label(mainframe, text="---------- Detectar contornos ----------", font=fuente_arial)
etiqueta_label_contornos.place(relx=0.30,rely=0.02)

boton_N4 = tk.Button(mainframe,width=5,height=2, text="N4",command=pixeles.vecindad_N4, font=fuente_arial)
boton_N4.place(relx=0.30,rely=0.05)

boton_N8 = tk.Button(mainframe,width=5,height=2, text="N8",command=pixeles.vecindad_N8, font=fuente_arial)
boton_N8.place(relx=0.34,rely=0.05)

etiqueta_label_codigos = tk.Label(mainframe, text="---------- Codigos de cadena ----------", font=fuente_arial)
etiqueta_label_codigos.place(relx=0.30,rely=0.11)

boton_F4 = tk.Button(mainframe,width=5,height=2, text="F4",command= lambda: pixeles.f4(etiqueta_entry_codigo), font=fuente_arial)
boton_F4.place(relx=0.30,rely=0.14)

boton_F8 = tk.Button(mainframe,width=5,height=2, text="F8",command= lambda: pixeles.f8(etiqueta_entry_codigo), font=fuente_arial)
boton_F8.place(relx=0.34,rely=0.14)

boton_AF8 = tk.Button(mainframe,width=5,height=2, text="AF8",command= lambda: pixeles.af8(etiqueta_entry_codigo), font=fuente_arial)
boton_AF8.place(relx=0.38,rely=0.14)

boton_VCC = tk.Button(mainframe,width=5,height=2, text="VCC",command= lambda: pixeles.vcc_3(etiqueta_entry_codigo), font=fuente_arial)
boton_VCC.place(relx=0.42,rely=0.14)

boton_3OT = tk.Button(mainframe,width=5,height=2, text="3OT",command= lambda: pixeles._3ot(etiqueta_entry_codigo), font=fuente_arial)
boton_3OT.place(relx=0.46,rely=0.14)

etiqueta_label_codigos = tk.Label(mainframe, text="---------- Decodificar ----------", font=fuente_arial)                               
etiqueta_label_codigos.place(relx=0.30,rely=0.2)

boton_decodificar = tk.Button(mainframe,width=14,height=1, text="Abrir archivo",command=pixeles.decodificar_archivo, font=fuente_arial)
boton_decodificar.place(relx=0.30,rely=0.23)

boton_decodificar = tk.Button(mainframe,width=14,height=1, text="Decodificar código",command=lambda: pixeles.decodificar_entry(etiqueta_entry_codigo, label_2), font=fuente_arial)
boton_decodificar.place(relx=0.39,rely=0.23)

etiqueta_label_histograma = tk.Label(mainframe, text="---------- Histograma ----------", font=fuente_arial)
etiqueta_label_histograma.place(relx=0.30,rely=0.29)

boton_histograma= tk.Button(mainframe,width=16,height=1, text="Generar histograma",command="", font=fuente_arial)
boton_histograma.place(relx=0.30,rely=0.321)

etiqueta_label_entropia = tk.Label(mainframe, text="---------- Entropia de Shannon ----------", font=fuente_arial)
etiqueta_label_entropia.place(relx=0.30,rely=0.38)

boton_entropia = tk.Button(
    mainframe,
    width=16,
    height=1, 
    text="Calcular entropia",
    command="", 
    font=fuente_arial,
    bd=1 
)
boton_entropia.place(relx=0.30, rely=0.41)


etiqueta_calculo_entropia = tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
) 
etiqueta_calculo_entropia.place(relx=0.40, rely=0.41)

#=============================== Seccion 2 =========================================================

etiqueta_label_huffman= tk.Label(mainframe, text="---------- Compresión de Huffman ----------", font=fuente_arial)
etiqueta_label_huffman.place(relx=0.53,rely=0.02)

boton_huffman = tk.Button(
    mainframe,
    width=11,
    height=1, 
    text="Comprimir",
    command=lambda:pixeles.compresion_huffman(etiqueta_calculo_huffman, etiqueta_entry_codigo), 
    font=fuente_arial,
    bd=1 
)
boton_huffman.place(relx=0.53,rely=0.05)


etiqueta_calculo_huffman = tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
) 
etiqueta_calculo_huffman.place(relx=0.6,rely=0.05)

etiqueta_label_aritmerica= tk.Label(mainframe, text="---------- Compresión de Aritmetica ----------", font=fuente_arial)
etiqueta_label_aritmerica.place(relx=0.53,rely=0.11)

boton_aritmetica = tk.Button(
    mainframe,
    width=11,
    height=1, 
    text="Comprimir",
    command="", 
    font=fuente_arial,
    bd=1 
)
boton_aritmetica.place(relx=0.53,rely=0.14)


etiqueta_calculo_aritmetica = tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
) 
etiqueta_calculo_aritmetica.place(relx=0.6,rely=0.14)

#=============================== Seccion 3 =========================================================
etiqueta_label_propiedades = tk.Label(mainframe, text="---------- Propiedades Geometricas ----------", font=fuente_arial)
etiqueta_label_propiedades.place(relx=0.76,rely=0.02)

boton_calcular_propiedades = tk.Button(mainframe,width=10,height=1, text="Calcular",command="", font=fuente_arial)
boton_calcular_propiedades.place(relx=0.76,rely=0.05)

etiqueta_label_perimetro = tk.Label(
    mainframe, 
    text="Perímetro:", 
    height=1, 
    font=("Arial",12) 
)
etiqueta_label_perimetro.place(relx=0.76, rely=0.11)


etiqueta_calculo_perimetro= tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
)
etiqueta_calculo_perimetro.place(relx=0.82,rely=0.11)


etiqueta_label_area = tk.Label(
    mainframe, 
    text="Área:", 
    height=1, 
    font=("Arial",12) 
)
etiqueta_label_area.place(relx=0.76, rely=0.15)


etiqueta_calculo_area= tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
)
etiqueta_calculo_area.place(relx=0.82,rely=0.15)

etiqueta_label_perimetro_contacto = tk.Label(
    mainframe, 
    text="P. Contacto:", 
    height=1, 
    font=("Arial",12) 
)
etiqueta_label_perimetro_contacto.place(relx=0.76, rely=0.19)

etiqueta_calculo_perimetro_contacto= tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
)
etiqueta_calculo_perimetro_contacto.place(relx=0.82,rely=0.19)

etiqueta_label_euler = tk.Label(
    mainframe, 
    text="C. Euler:", 
    height=1, 
    font=("Arial",12) 
)
etiqueta_label_euler.place(relx=0.76, rely=0.23)

etiqueta_calculo_euler= tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
)
etiqueta_calculo_euler.place(relx=0.82,rely=0.23)

etiqueta_label_discreta = tk.Label(
    mainframe, 
    text="C. Discreta:", 
    height=1, 
    font=("Arial",12) 
)
etiqueta_label_discreta.place(relx=0.76, rely=0.27)

etiqueta_calculo_discreta= tk.Label(
    mainframe, 
    text="0.0000",                  
    font=("Arial",12,"bold"), 
    bg="white", 
    fg="black",        
    width=13, 
    height=1,          
    anchor="center",   
    relief="sunken",   
    bd=2               
)
etiqueta_calculo_discreta.place(relx=0.82,rely=0.27)
# =============================== Seccion 4=====================================
etiqueta_label_codigo_cadena = tk.Label(mainframe, text="---------- Código de cadena ----------", font=fuente_arial)
etiqueta_label_codigo_cadena.place(relx=0.30, rely=0.53)

etiqueta_label_texto = tk.Label(
    mainframe, 
    text="Código de cadena:", 
    font=("Arial", 12) 
)
etiqueta_label_texto.place(relx=0.30, rely=0.57)

etiqueta_entry_codigo = tk.Entry(mainframe, font=("Arial", 12, "bold"))
etiqueta_entry_codigo.place(relx=0.40, rely=0.57, relwidth=0.35) 

scrollbar = tk.Scrollbar(
    mainframe, 
    orient="horizontal", 
    command=etiqueta_entry_codigo.xview,
    width=12  
)

scrollbar.place(relx=0.40, rely=0.61, relwidth=0.35)

etiqueta_entry_codigo.config(xscrollcommand=scrollbar.set)

etiqueta_entry_codigo.insert(0, "")

exportar = tk.Button(mainframe,width=7,height=2, text="Exportar",command=lambda: pixeles.formato_codificado(etiqueta_entry_codigo), font=fuente_arial)
exportar.place(relx=0.30, rely=0.62)



ventana.mainloop()