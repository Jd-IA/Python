import os
import io
import base64
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from codigos_cadenas import Pixel

IMAGEN_BLANCO_B64 = "/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAFeAV4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9/KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/2Q=="

ventana = tk.Tk()
ventana.title("Code Chain")
mainframe = tk.Frame(ventana)
mainframe.pack(fill="both", expand=True)
mainframe.config(bg="#38403D")
ventana.state('zoomed')
ventana.resizable(False, False)
ventana.update()

fuente_arial = ("Arial", 10)

directorio_actual = os.path.dirname(__file__)

def cargar_imagen_b64(b64_string, ancho, alto):
    data = base64.b64decode(b64_string)
    img = Image.open(io.BytesIO(data)).resize((ancho, alto), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

ancho = int(ventana.winfo_width()  * 0.25)
alto  = int(ventana.winfo_height() * 0.45)

image  = cargar_imagen_b64(IMAGEN_BLANCO_B64, ancho, alto)
image2 = cargar_imagen_b64(IMAGEN_BLANCO_B64, ancho, alto)

label = ttk.Label(mainframe, image=image)
label.place(relx=0.02, rely=0.02)

label_2 = ttk.Label(mainframe, image=image2)
label_2.place(relx=0.02, rely=0.53)

pixeles = Pixel()

boton_abrir_imagen = tk.Button(mainframe, width=10, height=1, text="Abrir imagen", command=lambda: pixeles.cargar_imagen(label), font=fuente_arial)
boton_abrir_imagen.place(relx=0.1, rely=0.48)


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

boton_decodificar = tk.Button(mainframe,width=14,height=1, text="Abrir archivo",command=lambda: pixeles.decodificar_archivo(etiqueta_entry_codigo), font=fuente_arial)
boton_decodificar.place(relx=0.30,rely=0.23)

boton_decodificar = tk.Button(mainframe,width=14,height=1, text="Decodificar código",command=lambda: pixeles.decodificar_entry(etiqueta_entry_codigo, label_2), font=fuente_arial)
boton_decodificar.place(relx=0.39,rely=0.23)

etiqueta_label_histograma = tk.Label(mainframe, text="---------- Histograma ----------", font=fuente_arial)
etiqueta_label_histograma.place(relx=0.30,rely=0.29)

boton_histograma= tk.Button(mainframe,width=16,height=1, text="Generar histograma",command=lambda: pixeles.histograma(etiqueta_entry_codigo), font=fuente_arial)
boton_histograma.place(relx=0.30,rely=0.321)

etiqueta_label_entropia = tk.Label(mainframe, text="---------- Entropia de Shannon ----------", font=fuente_arial)
etiqueta_label_entropia.place(relx=0.30,rely=0.38)

boton_entropia = tk.Button(
    mainframe,
    width=16,
    height=1, 
    text="Calcular entropia",
    command=lambda:pixeles.entropia_shannon(etiqueta_entry_codigo, etiqueta_calculo_entropia), 
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
    command=lambda:pixeles.compresion_huffman(etiqueta_entry_codigo, etiqueta_calculo_huffman), 
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
    command=lambda:pixeles.comp_aritmetica(etiqueta_entry_codigo, etiqueta_calculo_aritmetica), 
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

boton_calcular_propiedades = tk.Button(mainframe,width=10,height=1, text="Calcular",command=lambda: pixeles.propiedades_geometricas(etiqueta_calculo_perimetro, 
                                                                                                                                    etiqueta_calculo_area, 
                                                                                                                                    etiqueta_calculo_perimetro_contacto, 
                                                                                                                                    etiqueta_calculo_euler, 
                                                                                                                                    etiqueta_calculo_discreta), font=fuente_arial)
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


while True:
    try:
        ventana.mainloop()
        break
    except KeyboardInterrupt:
        pass
