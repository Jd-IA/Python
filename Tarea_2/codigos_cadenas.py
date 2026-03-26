import tkinter as tk
import heapq
from collections import Counter
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


class Pixel:
    def __init__(self):
        self.fila = 0
        self.columna = 0
        self.matriz_binaria = 0
        self.matriz_N4 = 0
        self.perimetro_N4 = 0
        self.matriz_N8 = 0
        self.perimetro_N8 = 0
        self.matriz_rep_pixeles = 0
        self.codigo_F4 = []
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

    def cargar_imagen(self, label_interfaz):
        # 1. Abrir el cuadro de diálogo
        ruta_imagen_og = filedialog.askopenfilename()

        if ruta_imagen_og:
            # --- PROCESAMIENTO DE DATOS ORIGINALES ---
            # Abrimos la imagen original para mantener la resolución real
            imagen_og = Image.open(ruta_imagen_og).convert("RGB")
            img_og_array = np.array(imagen_og)

            # Guardamos las dimensiones ORIGINALES en los atributos de la clase
            fila_real = img_og_array.shape[0]
            columna_real = img_og_array.shape[1]
            self.set_fila(fila_real)
            self.set_columna(columna_real)

            print(f"Datos originales guardados: {fila_real}x{columna_real}")

            # Crear la matriz binaria basada en los datos REALES
            matriz = np.zeros((fila_real, columna_real))
            for i in range(fila_real):
                for j in range(columna_real):
                    if (img_og_array[i, j, 0] != 0):
                        matriz[i, j] = 1
            
            self.set_matriz_binaria(matriz)
            print("Matriz binaria generada con éxito.")

            # --- PROCESAMIENTO PARA VISUALIZACIÓN (Interfaz) ---
            # Creamos una COPIA de la imagen para no afectar la original
            imagen_display = imagen_og.copy()
            
            # Redimensionamos la copia a un máximo de 350x350
            imagen_display.thumbnail((350, 350), Image.Resampling.LANCZOS)
            
            # 2. Visualización (Reescalado a 350x350)
            imagen_display = imagen_og.copy()
            imagen_display.thumbnail((350, 350), Image.Resampling.LANCZOS)
            
            # Convertir y actualizar el Label que recibimos por parámetro
            nueva_img_tk = ImageTk.PhotoImage(imagen_display)
            label_interfaz.config(image=nueva_img_tk)
            label_interfaz.image = nueva_img_tk # Evita que desaparezca de memoria
            
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
                        #print(f"Primer 1 encontrado en x: {self.x_inicio}, y: {self.y_inicio}")
                        encontrado = True
                        break  
                if encontrado:
                    break  
 
        else:
            print("No se abrio un arhcivo txt")
        
    def vecindad_N4(self):
        perimetro = 0 
        matriz_perimetro = np.zeros_like(self.matriz_binaria)
        matriz = self.matriz_binaria
        
        # Recorremos TODA la matriz (desde 0 hasta el final)
        for i in range(0, self.fila):
            for j in range(0, self.columna):
                if matriz[i, j] == 1:
                    
                    # --- CASO ESPECIAL: Píxeles en los bordes de la imagen ---
                    # Si el píxel está en la orilla, es perímetro automáticamente
                    if (i == 0 or i == self.fila - 1 or 
                        j == 0 or j == self.columna - 1):
                        perimetro += 1
                        matriz_perimetro[i, j] = 1
                    
                    # --- TU LÓGICA NORMAL: Píxeles internos ---
                    # Solo revisamos vecinos si NO estamos en la orilla
                    else:
                        if (matriz[i-1, j] == 0 or matriz[i, j-1] == 0 or 
                            matriz[i+1, j] == 0 or matriz[i, j+1] == 0):
                            perimetro += 1
                            matriz_perimetro[i, j] = 1
        
        # Guardar y notificar resultados
        print(f"Perimetro N4: {perimetro}")
        self.set_matriz_N4(matriz_perimetro, perimetro)

        # --- Bloque de visualización (Ventana Roja) ---
        alto, ancho = matriz_perimetro.shape
        img_color = np.zeros((alto, ancho, 3), dtype=np.uint8)
        img_color[matriz_perimetro == 1] = [255, 0, 0]

        ventana_resaltado = tk.Toplevel()
        ventana_resaltado.title("Visualización Vecindad N4")
        ventana_resaltado.config(bg="#38403D")

        imagen_pil = Image.fromarray(img_color)
        imagen_pil.thumbnail((500, 500), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(imagen_pil)

        lbl_img = tk.Label(ventana_resaltado, image=img_tk, bg="#38403D")
        lbl_img.image = img_tk 
        lbl_img.pack(padx=20, pady=20)

        tk.Label(
            ventana_resaltado, 
            text=f"Píxeles en el perímetro N4: {perimetro}",
            fg="white", bg="#38403D", font=("Arial", 12, "bold")
        ).pack(pady=10)

    def vecindad_N8(self):
        perimetro=0
        matriz_perimetro = np.zeros_like(self.matriz_binaria)
        matriz=self.matriz_binaria
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
                        
                        perimetro = perimetro + 1
                        matriz_perimetro[i, j] = 1

        print(f"Perimetro N8: {perimetro}")
        self.set_matriz_N8(matriz_perimetro, perimetro)

        alto, ancho = matriz_perimetro.shape
        img_color = np.zeros((alto, ancho, 3), dtype=np.uint8)

        img_color[matriz_perimetro == 1] = [255, 0, 0]

        ventana_resaltado_2 = tk.Toplevel()
        ventana_resaltado_2.title("Vecindad N8")
        ventana_resaltado_2.config(bg="#38403D")

        imagen_pil_2 = Image.fromarray(img_color)
        imagen_pil_2.thumbnail((500, 500), Image.Resampling.LANCZOS)
        
        img_tk_2 = ImageTk.PhotoImage(imagen_pil_2)

        lbl_img_2 = tk.Label(ventana_resaltado_2, image=img_tk_2, bg="#38403D")
        lbl_img_2.image = img_tk_2 
        lbl_img_2.pack(padx=20, pady=20)

        tk.Label(
            ventana_resaltado_2, 
            text=f"Píxeles en el perímetro N8: {perimetro}",
            fg="white", bg="#38403D", font=("Arial", 12, "bold")
        ).pack(pady=10)
    
    def representar_pixeles(self):
            # Para que se solapen, escalamos por 2 en lugar de 3
            # (2 * original + 1) para cubrir los bordes finales
            filas_rep = self.fila * 2 + 1
            cols_rep = self.columna * 2 + 1
            matriz_representacion = np.zeros((filas_rep, cols_rep))

            for i in range(self.fila):
                for j in range(self.columna): 
                    if self.matriz_binaria[i, j] == 1:
                        # Usamos desplazamiento de 2 para que las aristas coincidan
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

    def formato_codificado(self, x, y, codigo, alto, ancho):
        texto=f"{alto}x{ancho} {x},{y} {codigo}"

        return texto
    
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
    def f4(self, entry):

        codigo = []
        x = 0
        y = 0
        
        encontrado = False
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    
                    x = i 
                    y = j
                    print(f"x {x}, y {y}")
                    encontrado = True
                    break  
            if encontrado:
                break  
        final_x = x
        final_y = y

        pos_recorridas = []

        n = 0
    
        while (n < self.fila * self.columna):

            if y + 1 < self.columna and self.matriz_binaria[x, y+1] == 1 and ((x, y+1) not in pos_recorridas) and self.verificar_vecidnad_N8(x, y+1, self.matriz_binaria):
                codigo.append(0)
                y += 1
                
            elif x + 1 < self.fila and self.matriz_binaria[x+1, y] == 1 and ((x+1, y) not in pos_recorridas) and self.verificar_vecidnad_N8(x+1, y, self.matriz_binaria):
                codigo.append(1) 
                x += 1

            elif y - 1 >= 0 and self.matriz_binaria[x, y-1] == 1 and ((x, y-1) not in pos_recorridas) and self.verificar_vecidnad_N8(x, y-1, self.matriz_binaria):
                codigo.append(2) 
                y -= 1
                
            elif x - 1 >= 0 and self.matriz_binaria[x-1, y] == 1 and ((x-1, y) not in pos_recorridas) and self.verificar_vecidnad_N8(x-1, y, self.matriz_binaria):
                codigo.append(3)
                x -= 1
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

            pos_recorridas.append((x, y))
            

            if x == final_x and y == final_y:
                break
                
            n += 1
        print(n)
        n=0
        print(f"Código F4 Final: {codigo} (Longitud: {len(codigo)})")

        self.codigo_F4 = codigo
        entry.delete("0",tk.END)    
        entry.insert("end","F4 ")
        entry.insert("end",str(codigo))

        return self.codigo_F4


    def f4_2(self): #No usar este, este se usa solamente para 3ot

        codigo = []
        x = 0
        y = 0
        
        encontrado = False
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    x = i 
                    y = j
                    encontrado = True
                    break  
            if encontrado:
                break  
        final_x = x
        final_y = y

        pos_recorridas = []

        n = 0
    
        while (n < self.fila*self.columna):
            if self.matriz_binaria[x, y+1]==1 and ((x,y+1) not in pos_recorridas) and self.verificar_vecidnad_N8(x, y+1, self.matriz_binaria):
                codigo.append(0)
                y += 1
            elif self.matriz_binaria[x+1, y] == 1 and ((x+1,y) not in pos_recorridas) and self.verificar_vecidnad_N8(x+1, y, self.matriz_binaria):
                codigo.append(1) 
                x += 1
            elif self.matriz_binaria[x, y-1] == 1 and ((x,y-1) not in pos_recorridas) and self.verificar_vecidnad_N8(x, y-1, self.matriz_binaria):
                codigo.append(2) 
                y -= 1
            elif self.matriz_binaria[x-1, y] == 1 and ((x-1,y) not in pos_recorridas) and self.verificar_vecidnad_N8(x-1, y, self.matriz_binaria):
                codigo.append(3)
                x -= 1
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

            pos_recorridas.append((x, y))
            

            if x == final_x and y == final_y:
                break
                
            n += 1
        n=0

        self.codigo_F4 = codigo

        return self.codigo_F4




    def f8(self, entry):
        codigo = []
        x, y = 0, 0
        encontrado = False

        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1 and self.verificar_vecidnad_N8(i, j, self.matriz_binaria):
                    x, y = i, j
                    encontrado = True
                    break
            if encontrado: break

        if not encontrado:
            return []

        inicio_x, inicio_y = x, y
        pos_recorridas = set() 
        
        n = 0
        max_pasos = self.fila * self.columna 

        while n < max_pasos:
            pos_actual = (x, y)

            if self.matriz_binaria[x, y+1] == 1 and (x, y+1) not in pos_recorridas and self.verificar_vecidnad_N8(x, y+1, self.matriz_binaria):
                codigo.append(0); y += 1
            elif self.matriz_binaria[x+1, y+1] == 1 and (x+1, y+1) not in pos_recorridas and self.verificar_vecidnad_N8(x+1, y+1, self.matriz_binaria):
                codigo.append(1); x += 1; y += 1
            elif self.matriz_binaria[x+1, y] == 1 and (x+1, y) not in pos_recorridas and self.verificar_vecidnad_N8(x+1, y, self.matriz_binaria):
                codigo.append(2); x += 1
            elif self.matriz_binaria[x+1, y-1] == 1 and (x+1, y-1) not in pos_recorridas and self.verificar_vecidnad_N8(x+1, y-1, self.matriz_binaria):
                codigo.append(3); x += 1; y -= 1
            elif self.matriz_binaria[x, y-1] == 1 and (x, y-1) not in pos_recorridas and self.verificar_vecidnad_N8(x, y-1, self.matriz_binaria):
                codigo.append(4); y -= 1
            elif self.matriz_binaria[x-1, y-1] == 1 and (x-1, y-1) not in pos_recorridas and self.verificar_vecidnad_N8(x-1, y-1, self.matriz_binaria):
                codigo.append(5); x -= 1; y -= 1
            elif self.matriz_binaria[x-1, y] == 1 and (x-1, y) not in pos_recorridas and self.verificar_vecidnad_N8(x-1, y, self.matriz_binaria):
                codigo.append(6); x -= 1
            elif self.matriz_binaria[x-1, y+1] == 1 and (x-1, y+1) not in pos_recorridas and self.verificar_vecidnad_N8(x-1, y+1, self.matriz_binaria):
                codigo.append(7); x -= 1; y += 1
            else:

                break

            pos_recorridas.add(pos_actual)

            if x == inicio_x and y == inicio_y:
                print("¡Contorno cerrado!")
                break
                
            n += 1

        print(n)
        n=0
        print(f"Código F8 Final: {codigo} (Longitud: {len(codigo)})")

        self.codigo_F8 = codigo
        entry.delete("0",tk.END)  
        entry.insert("end","F8 ")  
        entry.insert("end",str(codigo))

        return self.codigo_F8

    def f8_2(self):
        codigo = []
        x, y = 0, 0
        encontrado = False


        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1 and self.verificar_vecidnad_N8(i, j, self.matriz_binaria):
                    x, y = i, j
                    encontrado = True
                    break
            if encontrado: break

        if not encontrado:
            return []

        inicio_x, inicio_y = x, y
        pos_recorridas = set() 
        
        n = 0
        max_pasos = self.fila * self.columna 

        while n < max_pasos:
            pos_actual = (x, y)
            
            if self.matriz_binaria[x, y+1] == 1 and (x, y+1) not in pos_recorridas and self.verificar_vecidnad_N8(x, y+1, self.matriz_binaria):
                codigo.append(0); y += 1
            elif self.matriz_binaria[x+1, y+1] == 1 and (x+1, y+1) not in pos_recorridas and self.verificar_vecidnad_N8(x+1, y+1, self.matriz_binaria):
                codigo.append(1); x += 1; y += 1
            elif self.matriz_binaria[x+1, y] == 1 and (x+1, y) not in pos_recorridas and self.verificar_vecidnad_N8(x+1, y, self.matriz_binaria):
                codigo.append(2); x += 1
            elif self.matriz_binaria[x+1, y-1] == 1 and (x+1, y-1) not in pos_recorridas and self.verificar_vecidnad_N8(x+1, y-1, self.matriz_binaria):
                codigo.append(3); x += 1; y -= 1
            elif self.matriz_binaria[x, y-1] == 1 and (x, y-1) not in pos_recorridas and self.verificar_vecidnad_N8(x, y-1, self.matriz_binaria):
                codigo.append(4); y -= 1
            elif self.matriz_binaria[x-1, y-1] == 1 and (x-1, y-1) not in pos_recorridas and self.verificar_vecidnad_N8(x-1, y-1, self.matriz_binaria):
                codigo.append(5); x -= 1; y -= 1
            elif self.matriz_binaria[x-1, y] == 1 and (x-1, y) not in pos_recorridas and self.verificar_vecidnad_N8(x-1, y, self.matriz_binaria):
                codigo.append(6); x -= 1
            elif self.matriz_binaria[x-1, y+1] == 1 and (x-1, y+1) not in pos_recorridas and self.verificar_vecidnad_N8(x-1, y+1, self.matriz_binaria):
                codigo.append(7); x -= 1; y += 1
            else:
                break

            pos_recorridas.add(pos_actual)

            if x == inicio_x and y == inicio_y:
                print("¡Contorno cerrado!")
                break
                
            n += 1

        print(n)
        n=0
        self.codigo_F8 = codigo

        return self.codigo_F8

    def af8(self, entry):
        #codigo de f8 a af8
        codigo = self.f8_2()
        a_f8=[]
        aux=0
        for i in range(len(codigo)-1):
            aux = (int(codigo[i+1])-int(codigo[i]))%8
            a_f8.append(aux)
        aux = (int(codigo[int(len(codigo)-1)])-int(codigo[0]))%8

        a_f8.append(aux)

        self.codigo_AF8=a_f8
        
        print(f"Código AF8 Final: {a_f8} (Longitud: {len(a_f8)})")

        entry.delete("0",tk.END) 
        entry.insert("end","AF8 ")   
        entry.insert("end",str(a_f8))

        return self.codigo_AF8

    def vcc_3(self, entry):

        self.representar_pixeles()

        x, y = 0, 0
        fila = self.matriz_rep_pixeles.shape[0]
        columna = self.matriz_rep_pixeles.shape[1]
        encontrado = False

        for i in range(fila):
            for j in range(columna):
                if self.matriz_rep_pixeles[i, j] == 1:
                    x, y = i, j
                    encontrado = True
                    break
            if encontrado: break

        final_x, final_y = x, y
        pos_recorridas = []
        codigo = []

        caminos_inicio = 0
        if y+2 < columna and self.matriz_rep_pixeles[x, y+2] == 1 and self.verificar_vecidnad_N8(x, y+2, self.matriz_rep_pixeles): caminos_inicio += 1
        if x+2 < fila    and self.matriz_rep_pixeles[x+2, y] == 1 and self.verificar_vecidnad_N8(x+2, y, self.matriz_rep_pixeles): caminos_inicio += 1
        if y-2 >= 0      and self.matriz_rep_pixeles[x, y-2] == 1 and self.verificar_vecidnad_N8(x, y-2, self.matriz_rep_pixeles): caminos_inicio += 1
        if x-2 >= 0      and self.matriz_rep_pixeles[x-2, y] == 1 and self.verificar_vecidnad_N8(x-2, y, self.matriz_rep_pixeles): caminos_inicio += 1
        
        codigo.append(max(1, caminos_inicio - 1))
        pos_recorridas.append((x, y))

        n = 0
        largo=self.matriz_rep_pixeles.shape[0]
        ancho=self.matriz_rep_pixeles.shape[1]
        while (n < (largo*ancho)):
            movido = False
            if y+2 < columna and self.matriz_rep_pixeles[x, y+2] == 1 and self.verificar_vecidnad_N8(x, y+2, self.matriz_rep_pixeles) and ((x, y+2) not in pos_recorridas):
                y += 2
                movido = True
            elif x+2 < fila and self.matriz_rep_pixeles[x+2, y] == 1 and self.verificar_vecidnad_N8(x+2, y, self.matriz_rep_pixeles) and ((x+2, y) not in pos_recorridas):
                x += 2
                movido = True
            elif y-2 >= 0 and self.matriz_rep_pixeles[x, y-2] == 1 and self.verificar_vecidnad_N8(x, y-2, self.matriz_rep_pixeles) and ((x, y-2) not in pos_recorridas):
                y -= 2
                movido = True
            elif x-2 >= 0 and self.matriz_rep_pixeles[x-2, y] == 1 and self.verificar_vecidnad_N8(x-2, y, self.matriz_rep_pixeles) and ((x-2, y) not in pos_recorridas):
                x -= 2
                movido = True

            if movido:
                caminos_totales = 0
                if y+2 < columna and self.matriz_rep_pixeles[x, y+2] == 1: caminos_totales += 1
                if x+2 < fila    and self.matriz_rep_pixeles[x+2, y] == 1: caminos_totales += 1
                if y-2 >= 0      and self.matriz_rep_pixeles[x, y-2] == 1: caminos_totales += 1
                if x-2 >= 0      and self.matriz_rep_pixeles[x-2, y] == 1: caminos_totales += 1
                
                codigo.append(caminos_totales - 1)
                pos_recorridas.append((x, y))
                
                if x == final_x and y == final_y:
                    break
            else:
                break
            n += 1
        n=0
        print(f"Código VCC Final: {codigo} (Longitud: {len(codigo)})")

        self.codigo_VCC3 = codigo

        entry.delete("0",tk.END)    
        entry.insert("end","VCC ")
        entry.insert("end",str(codigo))

        return self.codigo_VCC3


    def _3ot(self, entry):
        # Obtenemos el código F4
        codigo = self.f4_2() 
        n = len(codigo)
        c_3ot = []
        
        # Manejo circular: CF4(n+1) := CF4(1)
        codigo_extendido = codigo + [codigo[0]]
        
        for i in range(n):
            actual = int(codigo_extendido[i])
            siguiente = int(codigo_extendido[i+1])
            
            # 1. Si no hay cambio de dirección
            if siguiente == actual:
                c_3ot.append(0)
            else:
                # 2. Si hay cambio, buscamos la referencia k (último valor diferente a actual)
                k = None
                for j in range(i - 1, -1, -1):
                    if int(codigo[j]) != actual:
                        k = int(codigo[j])
                        break
                
                # Si no hay previo (inicio de la cadena), usamos el último del arreglo
                if k is None:
                    k = int(codigo[-1])
                
                # 3. Aplicamos la lógica de la matriz omitiendo el caso "*"
                if siguiente == k:
                    c_3ot.append(1)
                elif siguiente == (k + 2) % 4:
                    c_3ot.append(2)
                else:
                    # Omitimos cualquier otra transición no contemplada
                    pass

        self.codigo_3OT = c_3ot
        print(f"Código 3OT Final: {c_3ot} (Longitud: {len(c_3ot)})")

        entry.delete("0",tk.END)  
        entry.insert("end","3OT ")  
        entry.insert("end",str(codigo))
        return self.codigo_3OT
    

    def compresion_huffman(self, etiqueta_interfaz):
        codigo = self.codigo_F4()
    
        # Para calculo de frecuencias y probabilidades
        n = len(codigo)
        frecuencias = Counter(codigo)
        
        # De cada elemento: [frecuencia, [símbolo, "binario"]]
        heap = [[f, [s, ""]] for s, f in frecuencias.items()]
        heapq.heapify(heap)
        
        # Arbol de Huffman
        while len(heap) > 1:
            bajo = heapq.heappop(heap)
            alto = heapq.heappop(heap)
            # Asignando 0 a la rama izquierda y 1 a la derecha
            for par in bajo[1:]:
                par[1] = '0' + par[1]
            for par in alto[1:]:
                par[1] = '1' + par[1]
            heapq.heappush(heap, [bajo[0] + alto[0]] + bajo[1:] + alto[1:])

        nodos_finales = heapq.heappop(heap)[1:]
        longitud_promedio = 0
        
        for simbolo, bits in nodos_finales:
            prob_i = frecuencias[simbolo] / n
            long_bits_i = len(bits)
            longitud_promedio += prob_i * long_bits_i
      
        etiqueta_interfaz.config(text=f"{longitud_promedio:.4f}")
     
        