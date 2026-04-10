import io
import base64
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from esquinas import Pixel

IMAGEN_BLANCO_B64 = "/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAFeAV4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9/KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/2Q=="

ventana = tk.Tk()
ventana.title("Polígono")
mainframe = tk.Frame(ventana)
mainframe.pack(fill="both", expand=True)
mainframe.config(bg="#38403D")
ventana.state('zoomed')
ventana.resizable(False, False)
ventana.update()

fuente_arial = ("Arial", 10)

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

boton_abrir_imagen = tk.Button(
    mainframe, width=10, height=1, text="Abrir imagen",
    command=lambda: pixeles.cargar_imagen(label),
    font=fuente_arial
)
boton_abrir_imagen.place(relx=0.1, rely=0.48)

etiqueta_label_poligono = tk.Label(
    mainframe, text="---------- Polígono ----------", font=fuente_arial
)
etiqueta_label_poligono.place(relx=0.30, rely=0.02)

boton_calcular = tk.Button(
    mainframe, width=7, height=2, text="Calcular",
    command=lambda: pixeles.esquinas(
        etiqueta_entry_puntos, label_2,
        etiqueta_calculo_perimetro,
        etiqueta_calculo_cr,
        etiqueta_calculo_ise,
        etiqueta_calculo_fom
    ),
    font=fuente_arial
)
boton_calcular.place(relx=0.30, rely=0.05)

etiqueta_label_texto = tk.Label(
    mainframe, text="Puntos de quiebre:", font=("Arial", 12)
)
etiqueta_label_texto.place(relx=0.30, rely=0.11)

etiqueta_entry_puntos = tk.Entry(
    mainframe, font=("Arial", 12, "bold"), width=6, state="readonly"
)
etiqueta_entry_puntos.place(relx=0.40, rely=0.11)

tk.Label(mainframe, text="Perímetro N4:", height=1,
         font=("Arial", 12)).place(relx=0.30, rely=0.15)

etiqueta_calculo_perimetro = tk.Label(
    mainframe, text="0.0000", font=("Arial", 12, "bold"),
    bg="white", fg="black", width=13, height=1,
    anchor="center", relief="sunken", bd=2
)
etiqueta_calculo_perimetro.place(relx=0.40, rely=0.15)

tk.Label(mainframe, text="CR:", height=1,
         font=("Arial", 12)).place(relx=0.30, rely=0.19)

etiqueta_calculo_cr = tk.Label(
    mainframe, text="0.0000", font=("Arial", 12, "bold"),
    bg="white", fg="black", width=13, height=1,
    anchor="center", relief="sunken", bd=2
)
etiqueta_calculo_cr.place(relx=0.40, rely=0.19)

tk.Label(mainframe, text="ISE:", height=1,
         font=("Arial", 12)).place(relx=0.30, rely=0.23)

etiqueta_calculo_ise = tk.Label(
    mainframe, text="0.0000", font=("Arial", 12, "bold"),
    bg="white", fg="black", width=13, height=1,
    anchor="center", relief="sunken", bd=2
)
etiqueta_calculo_ise.place(relx=0.40, rely=0.23)

tk.Label(mainframe, text="FOM:", height=1,
         font=("Arial", 12)).place(relx=0.30, rely=0.27)

etiqueta_calculo_fom = tk.Label(
    mainframe, text="0.0000", font=("Arial", 12, "bold"),
    bg="white", fg="black", width=13, height=1,
    anchor="center", relief="sunken", bd=2
)
etiqueta_calculo_fom.place(relx=0.40, rely=0.27)

while True:
    try:
        ventana.mainloop()
        break
    except KeyboardInterrupt:
        pass
