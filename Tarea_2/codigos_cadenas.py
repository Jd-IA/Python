import math
import tkinter as tk
import heapq
import os
import numpy as np
from collections import Counter
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from scipy.ndimage import binary_fill_holes
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Pixel:
    def __init__(self):
        self.fila = 0
        self.columna = 0
        self.matriz_binaria = []
        self.nombre_imagen = ""
        self.matriz_N4 = []
        self.perimetro_N4 = 0
        self.ventana_N4 = None
        self.matriz_N8 = []
        self.perimetro_N8 = 0
        self.ventana_N8 = None
        self.matriz_rep_pixeles = []
        self.x_rp=""
        self.y_rp=""
        self.codigo_F4 = []
        self.codigo_F4_2 = []
        self.codigo_F8 = []
        self.codigo_AF8 = []
        self.codigo_VCC3 = []
        self.codigo_3OT = []
        self.ruta_archivo_og = ""
        self.x_inicio = 0
        self.y_inicio = 0
        self.resultado_huffman = 0

    def set_fila(self, fila):
        self.fila = fila

    def set_columna(self, columna):
        self.columna = columna
    
    def set_matriz_binaria(self, matriz):
        self.matriz_binaria = matriz

    def set_matriz_N4(self, matriz, perimetro):
        self.matriz_N4 = matriz
        self.perimetro_N4=perimetro

    def set_matriz_N8(self, matriz, perimetro):
        self.matriz_N8 = matriz
        self.perimetro_N8 = perimetro

    def cargar_imagen(self, label):
        ruta_imagen_og = filedialog.askopenfilename(
            filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif")]
        )

        if not ruta_imagen_og:
            messagebox.showwarning("Aviso", "No se seleccionó ningún archivo.")
            return

        extensiones_validas = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")
        if not ruta_imagen_og.lower().endswith(extensiones_validas):
            messagebox.showwarning("Aviso", "El archivo seleccionado no es una imagen válida.")
            return

        imagen_og = Image.open(ruta_imagen_og).convert("RGB")
        img_og_array = np.array(imagen_og)

        self.nombre_imagen = os.path.splitext(os.path.basename(ruta_imagen_og))[0]

        fila_real = img_og_array.shape[0]
        columna_real = img_og_array.shape[1]
        self.set_fila(fila_real)
        self.set_columna(columna_real)

        print(f"Datos originales guardados: {fila_real}x{columna_real}")

        matriz = np.zeros((fila_real, columna_real))
        for i in range(fila_real):
            for j in range(columna_real):
                if (img_og_array[i, j, 0] != 0):
                    matriz[i, j] = 1
        
        self.set_matriz_binaria(matriz)
        print("Matriz binaria generada con éxito.")
                    
        imagen_display = imagen_og.copy()
        imagen_display.thumbnail((350, 350), Image.Resampling.LANCZOS)
        
        nueva_img_tk = ImageTk.PhotoImage(imagen_display)
        label.config(image=nueva_img_tk)
        label.image = nueva_img_tk 
        
        print("Imagen actualizada en la interfaz y datos cargados.")


    def cargar_matriz(self):

        self.ruta_archivo_og = filedialog.askopenfilename()

        if self.ruta_archivo_og:

            matriz = np.genfromtxt(self.ruta_archivo_og, delimiter=',')

            self.set_matriz_binaria(matriz)
            print(matriz.shape)

            fila = matriz.shape[0]

            self.set_fila(fila)

            columna = matriz.shape[1]

            self.set_columna(columna)

            print(matriz)

            encontrado = False
            for i in range(fila):
                for j in range(columna):
                    if matriz[i, j] == 1:
                        self.x_inicio = i 
                        self.y_inicio = j
                        encontrado = True
                        break  
                if encontrado:
                    break  
 
        else:
            print("No se abrio un arhcivo txt")
        
    def vecindad_N4(self):
        if self.ventana_N4 is not None and self.ventana_N4.winfo_exists():
            self.ventana_N4.lift() 
            return
        if len(self.matriz_binaria) != 0:

            perimetro = 0 
            matriz_perimetro = np.zeros_like(self.matriz_binaria)
            matriz = self.matriz_binaria
            
            for i in range(0, self.fila):
                for j in range(0, self.columna):
                    if matriz[i, j] == 1:
                        if (i == 0 or i == self.fila - 1 or 
                            j == 0 or j == self.columna - 1):
                            perimetro += 1
                            matriz_perimetro[i, j] = 1
                        else:
                            if (matriz[i-1, j] == 0 or matriz[i, j-1] == 0 or 
                                matriz[i+1, j] == 0 or matriz[i, j+1] == 0):
                                perimetro += 1
                                matriz_perimetro[i, j] = 1
            
            print(f"Perimetro N4: {perimetro}")
            self.set_matriz_N4(matriz_perimetro, perimetro)

            alto, ancho = matriz_perimetro.shape
            img_color = np.zeros((alto, ancho, 3), dtype=np.uint8)
            img_color[matriz_perimetro == 1] = [255, 0, 0]

            self.ventana_N4 = tk.Toplevel()
            self.ventana_N4.title("Visualización Vecindad N4")
            self.ventana_N4.config(bg="#38403D")

            imagen_pil = Image.fromarray(img_color)
            imagen_pil.thumbnail((500, 500), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(imagen_pil)

            lbl_img = tk.Label(self.ventana_N4, image=img_tk, bg="#38403D")
            lbl_img.image = img_tk 
            lbl_img.pack(padx=20, pady=20)

            tk.Label(
                self.ventana_N4, 
                text=f"Píxeles en el perímetro N4: {perimetro}",
                fg="white", bg="#38403D", font=("Arial", 12, "bold")
            ).pack(pady=10)
        else:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
        

    def vecindad_N8(self):
        if self.ventana_N8 is not None and self.ventana_N8.winfo_exists():
            self.ventana_N8.lift()
            return
        if len(self.matriz_binaria) != 0:
            perimetro = 0
            matriz_perimetro = np.zeros_like(self.matriz_binaria)
            matriz = self.matriz_binaria
            for i in range(1, self.fila - 1):
                for j in range(1, self.columna - 1):
                    if matriz[i, j] == 1:
                        aux = i
                        aux_2 = j
                        if (matriz[aux-1, aux_2] == 0 or   
                            matriz[aux+1, aux_2] == 0 or   
                            matriz[aux, aux_2-1] == 0 or   
                            matriz[aux, aux_2+1] == 0 or   
                            matriz[aux-1, aux_2-1] == 0 or 
                            matriz[aux-1, aux_2+1] == 0 or 
                            matriz[aux+1, aux_2-1] == 0 or 
                            matriz[aux+1, aux_2+1] == 0):  
                            
                            perimetro += 1
                            matriz_perimetro[i, j] = 1

            print(f"Perimetro N8: {perimetro}")
            self.set_matriz_N8(matriz_perimetro, perimetro)

            alto, ancho = matriz_perimetro.shape
            img_color = np.zeros((alto, ancho, 3), dtype=np.uint8)
            img_color[matriz_perimetro == 1] = [255, 0, 0]

            self.ventana_N8 = tk.Toplevel()
            self.ventana_N8.title("Vecindad N8")
            self.ventana_N8.config(bg="#38403D")

            imagen_pil_2 = Image.fromarray(img_color)
            imagen_pil_2.thumbnail((500, 500), Image.Resampling.LANCZOS)
            img_tk_2 = ImageTk.PhotoImage(imagen_pil_2)

            lbl_img_2 = tk.Label(self.ventana_N8, image=img_tk_2, bg="#38403D")
            lbl_img_2.image = img_tk_2 
            lbl_img_2.pack(padx=20, pady=20)

            tk.Label(
                self.ventana_N8, 
                text=f"Píxeles en el perímetro N8: {perimetro}",
                fg="white", bg="#38403D", font=("Arial", 12, "bold")
            ).pack(pady=10)
        else:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
    def representar_pixeles(self):

        filas_rep = self.fila * 2 + 1
        cols_rep = self.columna * 2 + 1
        matriz_representacion = np.zeros((filas_rep, cols_rep))

        for i in range(self.fila):
            for j in range(self.columna): 
                if self.matriz_binaria[i, j] == 1:
                    ni = i * 2 + 1
                    nj = j * 2 + 1

                    matriz_representacion[ni, nj] = 1       
                    matriz_representacion[ni-1, nj] = 1     # Arista arriba
                    matriz_representacion[ni+1, nj] = 1     # Arista abajo
                    matriz_representacion[ni, nj-1] = 1     # Arista izquierda
                    matriz_representacion[ni, nj+1] = 1     # Arista derecha
                    matriz_representacion[ni-1, nj-1] = 1   # Vértice v1
                    matriz_representacion[ni-1, nj+1] = 1   # Vértice v2
                    matriz_representacion[ni+1, nj-1] = 1   # Vértice v3
                    matriz_representacion[ni+1, nj+1] = 1   # Vértice v4
        
        self.matriz_rep_pixeles=matriz_representacion

    def recuperar_tamaño_original(self, matriz_escalada):
        filas_rep, cols_rep = matriz_escalada.shape
        
        original_filas = (filas_rep - 1) // 2
        original_cols = (cols_rep - 1) // 2
        
        matriz_original = np.zeros((original_filas, original_cols), dtype=np.uint8)
        
        for i in range(original_filas):
            for j in range(original_cols):
                ni = i * 2 + 1
                nj = j * 2 + 1
                matriz_original[i, j] = int(matriz_escalada[ni, nj])
                
        return matriz_original

    def verificar_vecidnad_N8(self, i, j, matriz):
        if matriz[i, j] == 0:
            return False

        if (i == 0 or i == self.fila - 1 or 
            j == 0 or j == self.columna - 1):
            return True

        if (matriz[i-1, j] == 0 or   
            matriz[i+1, j] == 0 or   
            matriz[i, j-1] == 0 or   
            matriz[i, j+1] == 0 or   
            matriz[i-1, j-1] == 0 or 
            matriz[i-1, j+1] == 0 or 
            matriz[i+1, j-1] == 0 or 
            matriz[i+1, j+1] == 0):
            
            return True

        return False
    
    def verificar_vecidnad_N4(self, i, j, matriz):
        if matriz[i, j] == 0:
            return False

        if (i == 0 or i == self.fila - 1 or 
            j == 0 or j == self.columna - 1):
            return True

        if (matriz[i-1, j] == 0 or   # Arriba
            matriz[i+1, j] == 0 or   # Abajo
            matriz[i, j-1] == 0 or   # Izquierda
            matriz[i, j+1] == 0):    # Derecha
            
            return True

        return False
    
    def formato_codificado(self, entry):
        if entry.get() == "":
            messagebox.showwarning("Aviso", "Código de cadena vacío.")
            return

        if " - " not in entry.get():
            messagebox.showwarning("Aviso", "Formato inválido. Debe ser: TIPO - [codigo]")
            return

        
        codigo = (str(entry.get()).split(" - "))
        tipo   = codigo[0]

        if tipo == "3OT":
            texto = (f"{tipo} {self.fila}x{self.columna} "
                    f"{self.x_inicio},{self.y_inicio} "
                    f"{codigo[1]} "
                    f"{self.codigo_F4_2[0]}")   
        else:
            texto = f"{tipo} {self.fila}x{self.columna} {self.x_inicio},{self.y_inicio} {codigo[1]}"

        nombre = f"codigo {self.nombre_imagen} {tipo}"
        carpeta_destino = os.path.dirname(__file__)
        
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        nombre_archivo = os.path.join(carpeta_destino, nombre)

        with open(nombre_archivo, "w") as archivo:
            archivo.write(texto)
        
        messagebox.showinfo("Exportar", f"Archivo generado correctamente \n {nombre}")

    def decodificar_archivo(self, entry):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de código",
            filetypes=[("Archivos de texto", "*.txt")]
        )

        if not ruta:
            messagebox.showwarning("Aviso", "No se seleccionó ningún archivo.")
            return

        if not ruta.lower().endswith(".txt"):
            messagebox.showwarning("Aviso", "El archivo seleccionado no es válido.\nSolo se admiten archivos .txt")
            return

        with open(ruta, "r") as archivo:
            linea = archivo.read().strip()

        if not linea:
            messagebox.showwarning("Aviso", "El archivo está vacío.")
            return

        tipos_validos = ["F4", "F8", "AF8", "VCC", "3OT"]
        partes = linea.split(" ", 3)
        if (len(partes) < 4 or
            partes[0] not in tipos_validos or
            "x" not in partes[1] or
            "," not in partes[2] or
            not partes[3].startswith("[") or
            not partes[3].strip().endswith("]")):
            messagebox.showwarning("Aviso", "Formato inválido.\nDebe ser: TIPO FILASxCOLUMNAS X,Y [codigo]")
            return

        tipo         = partes[0]
        dims         = partes[1].split("x")
        inicio       = partes[2].split(",")
        texto_cadena = partes[3]

        self.fila     = int(dims[0])
        self.columna  = int(dims[1])
        self.x_inicio = int(inicio[0])
        self.y_inicio = int(inicio[1])

        if tipo == "3OT" and len(partes) > 4:
            f4_inicial = int(partes[4])
            self.codigo_F4_2 = [f4_inicial, f4_inicial]

        entry.delete("0", tk.END)
        entry.insert("end", f"{tipo} - {texto_cadena}")

        messagebox.showinfo("Aviso", f"Código {tipo} importado correctamente.\nPresiona el botón Decodificar para continuar.")


    def decodificar_entry(self, entry, label):
        
        if entry.get() == "":
            messagebox.showwarning("Aviso", "Código de cadena vacío.")
            return

        if " - " not in entry.get():
            messagebox.showwarning("Aviso", "Formato inválido. Debe ser: TIPO - [codigo]")
            return

        partes = entry.get().split(" - ")
        if len(partes) < 2 or not partes[0].strip() or not partes[1].strip().startswith("[") or not partes[1].strip().endswith("]"):
            messagebox.showwarning("Aviso", "Formato inválido. Debe ser: TIPO - [codigo]")
            return

        codigo = str(entry.get()).split(" - ")
        tipo = codigo[0]
        texto_cadena = codigo[1]

        tipos_validos = ["F4", "F8", "AF8", "VCC", "3OT"]
        if tipo not in tipos_validos:
            messagebox.showwarning("Aviso", f"Tipo '{tipo}' no reconocido.")
            return

        if tipo=="F4":

            filas    = self.fila * 2 + 1
            columnas = self.columna * 2 + 1
            x        = self.x_inicio * 2 + 1
            y        = self.y_inicio * 2 + 1

            paso1 = texto_cadena.strip("[]") 

            paso2 = paso1.split(",") 

            cadena = []
            for i in paso2:
                numero = int(i) 
                cadena.append(numero)

            

            matriz_perimetro = np.zeros((filas, columnas))

            n=0
            matriz_perimetro[x, y]=1

            while (n < len(cadena)):

                if cadena[n] == 0:
                    matriz_perimetro[x, y+1]=1
                    matriz_perimetro[x, y+2]=1
                    y += 2

                elif cadena[n]==1:
                    matriz_perimetro[x+1, y] = 1 
                    matriz_perimetro[x+2, y] = 1 
                    x += 2

                elif cadena[n]==2:
                    matriz_perimetro[x, y-1] = 1 
                    matriz_perimetro[x, y-2] = 1 
                    y -= 2

                elif cadena[n]==3:
                    matriz_perimetro[x-1, y] = 1
                    matriz_perimetro[x-2, y] = 1
                    x -= 2 
                else:
                    print("Termine")

                n += 1
            
            print(matriz_perimetro)
    
            matriz_rellena = binary_fill_holes(matriz_perimetro).astype(int)
            matriz_og = self.recuperar_tamaño_original(matriz_rellena)

            img_bw = (matriz_og * 255).astype(np.uint8)
            imagen_pil = Image.fromarray(img_bw, mode='L')

            imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)

            nueva_img_tk = ImageTk.PhotoImage(imagen_pil)

            label.config(image=nueva_img_tk)
            label.image = nueva_img_tk

        elif tipo=="F8":

    
            paso1 = texto_cadena.strip("[]") 

            paso2 = paso1.split(",") 

            cadena = []
            for i in paso2:
                numero = int(i) 
                cadena.append(numero)

            filas=self.fila
            columnas=self.columna
            x=self.x_inicio
            y=self.y_inicio

            matriz_perimetro = np.zeros((filas, columnas))

            n=0
            matriz_perimetro[x, y]=1

            while (n < len(cadena)):

                if cadena[n] == 0:
                    matriz_perimetro[x, y+1]=1
                    y += 1

                elif cadena[n]==1:
                    matriz_perimetro[x+1, y+1] = 1 
                    x += 1;  y+=1

                elif cadena[n]==2:
                    matriz_perimetro[x+1, y] = 1 
                    x += 1

                elif cadena[n]==3:
                    matriz_perimetro[x+1, y-1] = 1
                    x += 1; y -= 1

                elif cadena[n]==4:
                    matriz_perimetro[x, y-1] = 1
                    y -= 1

                elif cadena[n]==5:
                    matriz_perimetro[x-1, y-1] = 1 
                    x -= 1; y -= 1

                elif cadena[n]==6:
                    matriz_perimetro[x-1, y] = 1 
                    x -= 1
                elif cadena[n]==7:
                    matriz_perimetro[x-1, y+1] = 1 
                    x -= 1; y += 1
                else:
                    print("Termine")

                n += 1
            
            print(matriz_perimetro)

            #matriz_horizontal = matriz_perimetro.copy()
            #matriz_vertical = matriz_perimetro.copy()

            #for i in range(self.fila):
                #   pos_1, pos_2 = -1, -1
                #   for j in range(self.columna):
                #       if matriz_horizontal[i, j] == 1:
                #           if pos_1 == -1: pos_1 = j
                #           pos_2 = j    
                #   if pos_1 != -1 and pos_2 != -1:
                #       for k in range(pos_1 + 1, pos_2):
                #           matriz_horizontal[i, k] = 1

            #for j in range(self.columna): 
                #   pos_1, pos_2 = -1, -1
                #   for i in range(self.fila):
                #       if matriz_vertical[i, j] == 1:
                #           if pos_1 == -1: pos_1 = i
                #           pos_2 = i    
                #   if pos_1 != -1 and pos_2 != -1:
                #       for k in range(pos_1 + 1, pos_2):
                #           matriz_vertical[k, j] = 1 

            #matriz_rellena = np.zeros((self.fila, self.columna))
            matriz_rellena = binary_fill_holes(matriz_perimetro).astype(int)

            print(matriz_rellena)

            img_bw = (matriz_rellena * 255).astype(np.uint8)
            imagen_pil = Image.fromarray(img_bw, mode='L')

            imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)

            nueva_img_tk = ImageTk.PhotoImage(imagen_pil)

            # 6. Actualizar el label
            label.config(image=nueva_img_tk)
            label.image = nueva_img_tk

        elif tipo == "AF8":
        
            paso1 = texto_cadena.strip("[]") 
            paso2 = paso1.split(",") 
            cadena = [int(i) for i in paso2]

            filas, columnas = self.fila, self.columna
            x, y = self.x_inicio, self.y_inicio
            
            matriz_perimetro = np.zeros((filas, columnas))
            matriz_perimetro[x, y] = 1 

            dir_actual = 0 

            for i in range(len(cadena)):
   
                dir_actual = (dir_actual + cadena[i]) % 8
                
                if dir_actual == 0:   y += 1            
                elif dir_actual == 1: x += 1; y += 1      
                elif dir_actual == 2: x += 1            
                elif dir_actual == 3: x += 1; y -= 1      
                elif dir_actual == 4: y -= 1             
                elif dir_actual == 5: x -= 1; y -= 1     
                elif dir_actual == 6: x -= 1             
                elif dir_actual == 7: x -= 1; y += 1      
                
                if 0 <= x < filas and 0 <= y < columnas:
                    matriz_perimetro[x, y] = 1


            matriz_rellena = binary_fill_holes(matriz_perimetro).astype(int)

            img_bw = (matriz_rellena * 255).astype(np.uint8)
            imagen_pil = Image.fromarray(img_bw, mode='L')
            imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)
            
            nueva_img_tk = ImageTk.PhotoImage(imagen_pil)
            label.config(image=nueva_img_tk)
            label.image = nueva_img_tk

        elif tipo == "VCC":
            
            filas    = self.fila * 2 + 1
            columnas = self.columna * 2 + 1
            x        = self.x_inicio * 2 + 1
            y        = self.y_inicio * 2 + 1

            limpio = texto_cadena.strip("[]")
            cadena = [int(i.strip()) for i in limpio.split(",") if i.strip()]

            matriz_perimetro = np.zeros((filas, columnas))

            dx, dy = 0, 2
            
            matriz_perimetro[x, y] = 1
            n=0
            for giro in cadena:
                print(giro)


                if giro == 0:
                    pass  
                elif giro == 1: 
                    dx, dy = dy, -dx
                elif giro == 2:  
                    dx, dy = -dy, dx

                mid_x = x + dx // 2
                mid_y = y + dy // 2

                x += dx
                y += dy

                if 0 <= x < filas and 0 <= y < columnas:
                    matriz_perimetro[mid_x, mid_y] = 1
                    matriz_perimetro[x, y] = 1
                else:
                    break
                print(matriz_perimetro)
                n=n+1

            matriz_rellena = binary_fill_holes(matriz_perimetro).astype(int)
            
            matriz_og = self.recuperar_tamaño_original(matriz_rellena)

            img_bw = (matriz_og * 255).astype(np.uint8)
            imagen_pil = Image.fromarray(img_bw, mode='L')
            imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)

            nueva_img_tk = ImageTk.PhotoImage(imagen_pil)
            label.config(image=nueva_img_tk)
            label.image = nueva_img_tk
        elif tipo == "3OT":


            filas    = self.fila * 2 + 1
            columnas = self.columna * 2 + 1
            x        = self.x_inicio * 2 + 1
            y        = self.y_inicio * 2 + 1

            paso1 = texto_cadena.strip("[]")
            paso2 = paso1.split(",")
            c_3ot = []
            for i in paso2:
                c_3ot.append(int(i.strip()))


            f4_inicial = self.codigo_F4_2[0]
            cadena = [f4_inicial]

            for i in range(len(c_3ot)):
                current = cadena[i]

                k = None
                for j in range(i - 1, -1, -1):
                    if cadena[j] != current:
                        k = cadena[j]
                        break
                
                if k is None:
                    k = int(self.codigo_F4_2[-1])

                val = c_3ot[i]
                if val == 0:
                    next_dir = current
                elif val == 1:
                    next_dir = k          
                elif val == 2:
                    next_dir = (k + 2) % 4  
                else:
                    print("Valor 3OT inesperado:", val)
                    break

                cadena.append(next_dir)

            cadena = cadena[:-1]

            matriz_perimetro = np.zeros((filas, columnas))
            n = 0
            matriz_perimetro[x, y] = 1

            while n < len(cadena):
                if cadena[n] == 0:
                    matriz_perimetro[x, y+1] = 1
                    matriz_perimetro[x, y+2] = 1
                    y += 2
                elif cadena[n] == 1:
                    matriz_perimetro[x+1, y] = 1
                    matriz_perimetro[x+2, y] = 1
                    x += 2
                elif cadena[n] == 2:
                    matriz_perimetro[x, y-1] = 1
                    matriz_perimetro[x, y-2] = 1
                    y -= 2
                elif cadena[n] == 3:
                    matriz_perimetro[x-1, y] = 1
                    matriz_perimetro[x-2, y] = 1
                    x -= 2
                else:
                    print("Termine")
                n += 1

            print(matriz_perimetro)

            matriz_rellena = binary_fill_holes(matriz_perimetro).astype(int)
            matriz_og = self.recuperar_tamaño_original(matriz_rellena)
            img_bw = (matriz_og * 255).astype(np.uint8)
            imagen_pil = Image.fromarray(img_bw, mode='L')
            imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)
            nueva_img_tk = ImageTk.PhotoImage(imagen_pil)
            label.config(image=nueva_img_tk)
            label.image = nueva_img_tk

    def vecindad_N8_perimetro(self, matriz_1):
        
        matriz = np.zeros_like(matriz_1)
        fila = matriz.shape[0]
        columna = matriz.shape[1]

        for i in range(1, fila - 1):
            for j in range(1, columna - 1):
                if matriz_1[i, j] == 1:
                    aux = i
                    aux_2 = j
                    if (matriz_1[aux-1, aux_2] == 0 or   
                        matriz_1[aux+1, aux_2] == 0 or   
                        matriz_1[aux, aux_2-1] == 0 or   
                        matriz_1[aux, aux_2+1] == 0 or   
                        matriz_1[aux-1, aux_2-1] == 0 or 
                        matriz_1[aux-1, aux_2+1] == 0 or 
                        matriz_1[aux+1, aux_2-1] == 0 or 
                        matriz_1[aux+1, aux_2+1] == 0):  
                        
                        matriz[i, j] = 1
        return matriz
    
    def f4(self, entry):
        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return

        encontrado = False
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    self.x_inicio=i
                    self.y_inicio=j
                    encontrado = True

                    break  
            if encontrado:
                break  

        self.representar_pixeles()

        fila = self.matriz_rep_pixeles.shape[0]
        columna = self.matriz_rep_pixeles.shape[1]

        self.matriz_rep_pixeles=self.vecindad_N8_perimetro(self.matriz_rep_pixeles)

        print(self.matriz_rep_pixeles)

        codigo = []
        x = 0
        y = 0
        
        encontrado = False
        for i in range(fila):
            for j in range(columna):
                if self.matriz_rep_pixeles[i, j] == 1:
                    x = i 
                    y = j
                    encontrado = True
                    break  
            if encontrado:
                break  
        inicio_x = x
        inicio_y = y

        pos_recorridas = []

        n = 0
        pos_recorridas.append((x, y))
        while (n < fila*columna):
            
            if self.matriz_rep_pixeles[x, y+2]==1 and self.matriz_rep_pixeles[x, y+1]==1 and ((x, y+2) not in pos_recorridas or (x, y+2) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x, y+2, self.matriz_rep_pixeles) :
                codigo.append(0)
                y += 2
                pos_recorridas.append((x, y))
            elif self.matriz_rep_pixeles[x+2, y] == 1 and self.matriz_rep_pixeles[x+1, y]==1  and ((x+2, y) not in pos_recorridas or (x+2, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x+2, y, self.matriz_rep_pixeles):
                codigo.append(1) 
                x += 2
                pos_recorridas.append((x, y))
            elif self.matriz_rep_pixeles[x, y-2] == 1 and self.matriz_rep_pixeles[x, y-1]==1  and ((x, y-2) not in pos_recorridas or (x, y-2) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x, y-2, self.matriz_rep_pixeles):
                codigo.append(2) 
                y -= 2
                pos_recorridas.append((x, y))
            elif self.matriz_rep_pixeles[x-2, y] == 1 and self.matriz_rep_pixeles[x-1, y]==1 and ((x-2, y) not in pos_recorridas or (x-2, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x-2, y, self.matriz_rep_pixeles):
                codigo.append(3)
                x -= 2
                pos_recorridas.append((x, y))
            else:
                if len(pos_recorridas) > 1:

                    pos_anterior = pos_recorridas[-2]
                    ant_x, ant_y = pos_anterior
                    
                    if ant_y > y: 
                        codigo.append(0)
                    elif ant_x > x: 
                        codigo.append(1)
                    elif ant_y < y:
                        codigo.append(2)
                    elif ant_x < x:
                        codigo.append(3)
                    
                
                    x, y = ant_x, ant_y
                    
                    
                else:
                    break
            
            if x == inicio_x and y == inicio_y:
                break
            
            n += 1

  
        print(f"Código F4 Final: {codigo} (Longitud: {len(codigo)})")
        n=0
        self.codigo_F4 = codigo
        
        entry.delete("0", "end")
        entry.insert("end", "F4 - ")
        entry.insert("end", str(codigo))

        return self.codigo_F4
    
    def f4_2(self):
        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return
                
        encontrado = False
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    self.x_inicio=i
                    self.y_inicio=j
                    encontrado = True

                    break  
            if encontrado:
                break  

        self.representar_pixeles()

        fila = self.matriz_rep_pixeles.shape[0]
        columna = self.matriz_rep_pixeles.shape[1]

        self.matriz_rep_pixeles=self.vecindad_N8_perimetro(self.matriz_rep_pixeles)

        print(self.matriz_rep_pixeles)

        codigo = []
        x = 0
        y = 0
        
        encontrado = False
        for i in range(fila):
            for j in range(columna):
                if self.matriz_rep_pixeles[i, j] == 1:
                    x = i 
                    y = j
                    encontrado = True
                    break  
            if encontrado:
                break  
        inicio_x = x
        inicio_y = y

        pos_recorridas = []

        n = 0
        pos_recorridas.append((x, y))
        while (n < fila*columna):
            
            if self.matriz_rep_pixeles[x, y+2]==1 and self.matriz_rep_pixeles[x, y+1]==1 and ((x, y+2) not in pos_recorridas or (x, y+2) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x, y+2, self.matriz_rep_pixeles) :
                codigo.append(0)
                y += 2
                pos_recorridas.append((x, y))
            elif self.matriz_rep_pixeles[x+2, y] == 1 and self.matriz_rep_pixeles[x+1, y]==1  and ((x+2, y) not in pos_recorridas or (x+2, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x+2, y, self.matriz_rep_pixeles):
                codigo.append(1) 
                x += 2
                pos_recorridas.append((x, y))
            elif self.matriz_rep_pixeles[x, y-2] == 1 and self.matriz_rep_pixeles[x, y-1]==1  and ((x, y-2) not in pos_recorridas or (x, y-2) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x, y-2, self.matriz_rep_pixeles):
                codigo.append(2) 
                y -= 2
                pos_recorridas.append((x, y))
            elif self.matriz_rep_pixeles[x-2, y] == 1 and self.matriz_rep_pixeles[x-1, y]==1 and ((x-2, y) not in pos_recorridas or (x-2, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N8(x-2, y, self.matriz_rep_pixeles):
                codigo.append(3)
                x -= 2
                pos_recorridas.append((x, y))
            else:
                if len(pos_recorridas) > 1:

                    pos_anterior = pos_recorridas[-2]
                    ant_x, ant_y = pos_anterior
                    
                    if ant_y > y: 
                        codigo.append(0)
                    elif ant_x > x: 
                        codigo.append(1)
                    elif ant_y < y:
                        codigo.append(2)
                    elif ant_x < x:
                        codigo.append(3)
                    
                
                    x, y = ant_x, ant_y
                    
                    
                else:
                    break
            
            if x == inicio_x and y == inicio_y:
                break
            
            n += 1
        n=0
        self.codigo_F4 = codigo
        self.codigo_F4_2 = codigo
    
        return self.codigo_F4

    def f8(self, entry):
        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return
        codigo = []
        x, y = 0, 0
        encontrado = False

        # 1. Búsqueda del primer punto
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    x, y = i, j
                    self.x_inicio, self.y_inicio = i, j
                    encontrado = True
                    break
            if encontrado: break

        inicio_x, inicio_y = x, y
        

        pos_recorridas = set() 
        
        n = 0
        max_pasos = self.fila * self.columna 

        pos_recorridas.add((x, y))
        while n < max_pasos:

            if self.matriz_binaria[x, y+1] == 1 and ((x, y+1) not in pos_recorridas or (x, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y+1, self.matriz_binaria):
                codigo.append(0); y += 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x+1, y+1] == 1 and ((x+1, y+1) not in pos_recorridas or (x+1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y+1, self.matriz_binaria):
                codigo.append(1); x += 1; y += 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x+1, y] == 1 and ((x+1, y) not in pos_recorridas or (x+1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y, self.matriz_binaria):
                codigo.append(2); x += 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x+1, y-1] == 1 and ((x+1, y-1) not in pos_recorridas or (x+1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y-1, self.matriz_binaria):
                codigo.append(3); x += 1; y -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x, y-1] == 1 and ((x, y-1) not in pos_recorridas or (x, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y-1, self.matriz_binaria):
                codigo.append(4); y -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x-1, y-1] == 1 and ((x-1, y-1) not in pos_recorridas or (x-1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y-1, self.matriz_binaria):
                codigo.append(5); x -= 1; y -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x-1, y] == 1 and ((x-1, y) not in pos_recorridas or (x-1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y, self.matriz_binaria):
                codigo.append(6); x -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x-1, y+1] == 1 and ((x-1, y+1) not in pos_recorridas or (x-1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y+1, self.matriz_binaria):
                codigo.append(7); x -= 1; y += 1
                pos_recorridas.add((x, y))
            else:
                break

            if (x, y) == (inicio_x, inicio_y):
                print("¡Contorno cerrado con el último paso!")
                break
                
            n += 1
        print(f"Código F8 Final: {codigo} (Longitud: {len(codigo)})")
        n=0

        self.codigo_F8 = codigo
        entry.delete("0", tk.END)  
        entry.insert("end", f"F8 - {codigo}")

        return self.codigo_F8
    
    def f8_2(self):
        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return
        codigo = []
        x, y = 0, 0
        encontrado = False

        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    x, y = i, j
                    self.x_inicio, self.y_inicio = i, j
                    encontrado = True
                    break
            if encontrado: break

        inicio_x, inicio_y = x, y
        

        pos_recorridas = set() 
        
        n = 0
        max_pasos = self.fila * self.columna 

        pos_recorridas.add((x, y))
        while n < max_pasos:

            if self.matriz_binaria[x, y+1] == 1 and ((x, y+1) not in pos_recorridas or (x, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y+1, self.matriz_binaria):
                codigo.append(0); y += 1
                pos_recorridas.add((x, y))
            
            elif self.matriz_binaria[x+1, y+1] == 1 and ((x+1, y+1) not in pos_recorridas or (x+1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y+1, self.matriz_binaria):
                codigo.append(1); x += 1; y += 1
                pos_recorridas.add((x, y))
            
            elif self.matriz_binaria[x+1, y] == 1 and ((x+1, y) not in pos_recorridas or (x+1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y, self.matriz_binaria):
                codigo.append(2); x += 1
                pos_recorridas.add((x, y))
            
            elif self.matriz_binaria[x+1, y-1] == 1 and ((x+1, y-1) not in pos_recorridas or (x+1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y-1, self.matriz_binaria):
                codigo.append(3); x += 1; y -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x, y-1] == 1 and ((x, y-1) not in pos_recorridas or (x, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y-1, self.matriz_binaria):
                codigo.append(4); y -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x-1, y-1] == 1 and ((x-1, y-1) not in pos_recorridas or (x-1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y-1, self.matriz_binaria):
                codigo.append(5); x -= 1; y -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x-1, y] == 1 and ((x-1, y) not in pos_recorridas or (x-1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y, self.matriz_binaria):
                codigo.append(6); x -= 1
                pos_recorridas.add((x, y))

            elif self.matriz_binaria[x-1, y+1] == 1 and ((x-1, y+1) not in pos_recorridas or (x-1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y+1, self.matriz_binaria):
                codigo.append(7); x -= 1; y += 1
                pos_recorridas.add((x, y))
            else:
                break

            if (x, y) == (inicio_x, inicio_y):
                print("¡Contorno cerrado con el último paso!")
                break
                
            n += 1
        print(f"Código F8 Final: {codigo} (Longitud: {len(codigo)})")
        n=0

        self.codigo_F8 = codigo

        return self.codigo_F8

    def af8(self, entry):
        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return
        codigo = self.f8_2() # Obtiene F8 absoluto
        if not codigo: return []
        
        a_f8 = [int(codigo[0])] 
        
        for i in range(len(codigo) - 1):
            aux = (int(codigo[i+1]) - int(codigo[i])) % 8
            a_f8.append(aux)
            
        self.codigo_AF8 = a_f8
        
        print(f"Código AF8 Final: {a_f8} (Longitud: {len(a_f8)})")

        entry.delete("0",tk.END) 
        entry.insert("end","AF8 - ")   
        entry.insert("end",str(a_f8))

        return self.codigo_AF8

    def vcc_3(self, entry):

        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return
        self.representar_pixeles()
        filas, columnas = self.matriz_rep_pixeles.shape

        encontrado = False
        for i in range(filas):
            for j in range(columnas):
                if self.matriz_rep_pixeles[i, j] == 1:
                    x, y = i, j
                    encontrado = True
                    break
            if encontrado:
                break

        start_x, start_y = x, y

        pos_recorridas = [(x, y)]
        codigo = []

        dir_anterior = (0, 2)

        max_iter = filas * columnas
        n = 0

        while n < max_iter:
            movido = False

            dx, dy = dir_anterior

            opciones = [
                (-dy, dx),   
                (dx, dy),    
                (dy, -dx)    
            ]
            for ndx, ndy in opciones:

                nx, ny = x + ndx, y + ndy

                if (0 <= nx < filas and 0 <= ny < columnas and
                    self.matriz_rep_pixeles[nx, ny] == 1 and
                    ((nx, ny) not in pos_recorridas or (nx, ny) == (start_x, start_y))):

                    x1, y1 = dir_anterior
                    x2, y2 = ndx, ndy

                    giro_val = x1 * y2 - y1 * x2

                    if giro_val == 0:
                        codigo.append(0)  # recto
                    elif giro_val < 0:
                        codigo.append(1)  # derecha
                    else:
                        codigo.append(2)  # izquierda

                    x += ndx
                    y += ndy

                    dir_anterior = (ndx, ndy)
                    pos_recorridas.append((x, y))

                    if (x, y) == (start_x, start_y):
                        movido = True
                        break

                    movido = True
                    break

            if not movido:
                break

            n += 1

        self.codigo_VCC3 = codigo
        entry.delete("0", "end")
        entry.insert("end", f"VCC - {codigo}")

        return codigo
    
    def _3ot(self, entry):

        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return
        
        codigo = self.f4_2() 
        n = len(codigo)
        c_3ot = []
        
        codigo_extendido = codigo + [codigo[0]]
        
        for i in range(n):
            actual = int(codigo_extendido[i])
            siguiente = int(codigo_extendido[i+1])
            
            if siguiente == actual:
                c_3ot.append(0)
            else:
                k = None
                for j in range(i - 1, -1, -1):
                    if int(codigo[j]) != actual:
                        k = int(codigo[j])
                        break
                
                if k is None:
                    k = int(codigo[-1])
                
                if siguiente == k:
                    c_3ot.append(1)
                elif siguiente == (k + 2) % 4:
                    c_3ot.append(2)
                else:
                    pass

        self.codigo_3OT = c_3ot
        self.codigo_seleccionado = c_3ot

        print(f"Código 3OT Final: {c_3ot} (Longitud: {len(c_3ot)})")

        entry.delete("0",tk.END)  
        entry.insert("end","3OT - ")  
        entry.insert("end", str(c_3ot))
        return self.codigo_3OT
    
    def compresion_huffman(self, entry, label):
        if entry.get() == "":
            messagebox.showwarning("Aviso", "Código de cadena vacío.")
            return

        if " - " not in entry.get():
            messagebox.showwarning("Aviso", "Formato inválido. Debe ser: TIPO - [codigo]")
            return

        codigo=(str(entry.get()).split(" - "))
        tipo=codigo[0]
        texto_cadena=codigo[1]

        paso1 = texto_cadena.strip("[]") 

        paso2 = paso1.split(",") 

        codigo = []
        for i in paso2:
            numero = int(i) 
            codigo.append(numero)
    
        n = len(codigo) 
        frecuencias = Counter(codigo)
        
        heap = [[f, [s, ""]] for s, f in frecuencias.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            bajo = heapq.heappop(heap)
            alto = heapq.heappop(heap)
            for par in bajo[1:]:
                par[1] = '0' + par[1]
            for par in alto[1:]:
                par[1] = '1' + par[1]
            heapq.heappush(heap, [bajo[0] + alto[0]] + bajo[1:] + alto[1:])

        nodos_finales = heapq.heappop(heap)[1:]
        longitud_promedio = 0
        total_bits_acumulados = 0
        
        for simbolo, bits in nodos_finales:
            #prob_i = frecuencias[simbolo] / n
            #long_bits_i = len(bits)
            #longitud_promedio += prob_i * long_bits_i
            cuenta = frecuencias[simbolo]
            bits_simbolo = cuenta * len(bits)
            total_bits_acumulados += bits_simbolo
        longitud_promedio = total_bits_acumulados / n
        print(total_bits_acumulados)
        print(n)
        label.config(text=f"{longitud_promedio:.4f}")
     
    def tabla(self, codigo):
        frecuencia = Counter(codigo)
        N = len(codigo)
        datos = pd.DataFrame({
            'Simbolo': list(frecuencia.keys()),
            'Frecuencia': list(frecuencia.values())
        })
        datos['Probabilidad'] = datos['Frecuencia'] / N
        datos = datos.sort_values(by='Simbolo')
        return datos 

    def histograma(self, entry):
        if entry.get() == "":
            messagebox.showwarning("Aviso", "Código de cadena vacío.")
            return

        if " - " not in entry.get():
            messagebox.showwarning("Aviso", "Formato inválido. Debe ser: TIPO - [codigo]")
            return

        codigo_str   = str(entry.get()).split(" - ")
        tipo         = codigo_str[0]
        texto_cadena = codigo_str[1]

        codigo = [int(i) for i in texto_cadena.strip("[]").split(",")]

        datos = self.tabla(codigo)

        fig, axf = plt.subplots(facecolor="white")  
        axf.set_facecolor("white")                 

        axf.bar(datos['Simbolo'], datos['Frecuencia'],
                width=0.9,
                facecolor="#CC785C",  
                linewidth=0.1)

        axf.set(
            xlim=(-0.5, np.max(codigo) + 0.5),
            xticks=np.arange(0, np.max(codigo) + 1),
            ylim=(0, np.max(datos['Frecuencia']) + max(0.5, np.max(datos['Frecuencia']) // 10)),
            yticks=np.arange(0, np.max(datos['Frecuencia']) + 1, max(1, np.max(datos['Frecuencia']) // 10))
        )
        axf.set_xlabel("Elemento del código")
        axf.set_ylabel("Frecuencia", color="#CC785C")  

        ventana_hist = tk.Toplevel()
        ventana_hist.title(f"Histograma — {tipo}")
        ventana_hist.configure(bg="#38403D")           

        canvas = FigureCanvasTkAgg(fig, master=ventana_hist)
        canvas.get_tk_widget().configure(bg="#38403D") 
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def propiedades_geometricas(self, label_perimetro, label_area, label_perimetro_c, label_euler, label_com_discreta):
        if len(self.matriz_binaria) != 0:

            perimetro = 0
            area = 0
            perimetro_contacto = 0
            caracteristica_euler = 0
            com_discreta = 0
            matriz = self.matriz_binaria

            for i in range(self.fila):
                for j in range(self.columna):
                    if matriz[i, j] == 1:
                        area += 1
                        if (i == 0 or i == self.fila - 1 or j == 0 or j == self.columna - 1):
                            if i == 0:                
                                perimetro += 1
                            if i == self.fila - 1:    
                                perimetro += 1
                            if j == 0:                
                                perimetro += 1
                            if j == self.columna - 1: 
                                perimetro += 1
                        else:
                            if matriz[i-1, j] == 0:  
                                perimetro += 1
                            if matriz[i+1, j] == 0:   
                                perimetro += 1
                            if matriz[i, j-1] == 0:   
                                perimetro += 1
                            if matriz[i, j+1] == 0:   
                                perimetro += 1

            perimetro_contacto = (4 * area - perimetro) / 2

            Q1, Q3, QD = 0, 0, 0
            for i in range(self.fila - 1):
                for j in range(self.columna - 1):
                    p1 = int(matriz[i,   j  ])
                    p2 = int(matriz[i,   j+1])
                    p3 = int(matriz[i+1, j  ])
                    p4 = int(matriz[i+1, j+1])
                    suma = p1 + p2 + p3 + p4
                    if suma == 1:
                        Q1 += 1
                    elif suma == 3:
                        Q3 += 1
                    elif suma == 2:
                        if (p1 == 1 and p4 == 1 and p2 == 0 and p3 == 0):
                            QD += 1
                        elif (p2 == 1 and p3 == 1 and p1 == 0 and p4 == 0):
                            QD += 1

            caracteristica_euler = (Q1 - Q3 + 2 * QD) / 4

            if area - math.sqrt(area) != 0:
                com_discreta = (area - (perimetro / 4)) / (area - math.sqrt(area))
            else:
                com_discreta = 0

            label_perimetro.config(text=f"{perimetro}")
            label_area.config(text=f"{area}")
            label_perimetro_c.config(text=f"{perimetro_contacto:.4f}")
            label_euler.config(text=f"{caracteristica_euler:.4f}")
            label_com_discreta.config(text=f"{com_discreta:.4f}")
        else:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")