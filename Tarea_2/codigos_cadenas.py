import tkinter as tk
import heapq
import os
import numpy as np
from collections import Counter
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from scipy.ndimage import binary_fill_holes


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
        self.x_rp=""
        self.y_rp=""
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
        ruta_imagen_og = filedialog.askopenfilename()

        if ruta_imagen_og:

            imagen_og = Image.open(ruta_imagen_og).convert("RGB")
            img_og_array = np.array(imagen_og)

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
            label_interfaz.config(image=nueva_img_tk)
            label_interfaz.image = nueva_img_tk 
            
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


    def recuperar_tamaño_original(self, matriz_escalada):
        # matriz_escalada es la 'matriz_rellena' de tamaño (2M+1, 2N+1)
        filas_rep, cols_rep = matriz_escalada.shape
        
        # Operación inversa: n = (n_rep - 1) // 2
        original_filas = (filas_rep - 1) // 2
        original_cols = (cols_rep - 1) // 2
        
        matriz_original = np.zeros((original_filas, original_cols), dtype=np.uint8)
        
        for i in range(original_filas):
            for j in range(original_cols):
                # Saltamos a los centros (1, 3, 5...)
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
        
        codigo=(str(entry.get()).split(" - "))


        texto=f"{codigo[0]} {self.fila}x{self.columna} {self.x_inicio},{self.y_inicio} {codigo[1]}"

        nombre = f"codigo {codigo[0]} {self.fila}x{self.columna}"
        carpeta_destino = os.path.dirname(__file__)
        
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        nombre_archivo = os.path.join(carpeta_destino, nombre)

        with open(nombre_archivo, "w") as archivo:
            archivo.write(texto)
        
        messagebox.showinfo("Exportar", "Archivo generado correctamente")
    
    def decodificar_archivo(self):
        pass

    def decodificar_entry(self, entry, label_interfaz):
        
        print(entry.get())

        
        if entry.get()=="":
            messagebox.showwarning("Aviso", "Código de cadena vacio.")
        else:
            codigo=(str(entry.get()).split(" - "))
            tipo=codigo[0]
            texto_cadena=codigo[1]

            if tipo=="F4":

                self.representar_pixeles()
                filas = self.matriz_rep_pixeles.shape[0]
                columnas = self.matriz_rep_pixeles.shape[1]
                encontrado = False
                for i in range(filas):
                    for j in range(columnas):
                        if self.matriz_rep_pixeles[i, j] == 1:
                            x = i 
                            y = j
                            encontrado = True
                            break  
                    if encontrado:
                        break  

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
                # 4. AHORA SÍ: Volver al tamaño original
                matriz_og = self.recuperar_tamaño_original(matriz_rellena)

                # 5. Mostrar (matriz_og ya tiene el tamaño M x N)
                img_bw = (matriz_og * 255).astype(np.uint8)
                imagen_pil = Image.fromarray(img_bw, mode='L')

                imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)

                nueva_img_tk = ImageTk.PhotoImage(imagen_pil)

                # 6. Actualizar el label
                label_interfaz.config(image=nueva_img_tk)
                label_interfaz.image = nueva_img_tk

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
                label_interfaz.config(image=nueva_img_tk)
                label_interfaz.image = nueva_img_tk

            elif tipo == "AF8":
            
                # 1. Procesar la cadena de texto
                paso1 = texto_cadena.strip("[]") 
                paso2 = paso1.split(",") 
                cadena = [int(i) for i in paso2]

                # 2. Inicializar dimensiones y punto de partida
                filas, columnas = self.fila, self.columna
                x, y = self.x_inicio, self.y_inicio
                
                matriz_perimetro = np.zeros((filas, columnas))
                matriz_perimetro[x, y] = 1 # Pintar punto de inicio

                # La dirección inicial es RELATIVA a 0 para el primer movimiento
                dir_actual = 0 

                # 3. Reconstruir el perímetro
                for i in range(len(cadena)):
                    # El primer número nos da la dirección inicial absoluta
                    # Los siguientes se suman para obtener el nuevo rumbo
                    dir_actual = (dir_actual + cadena[i]) % 8
                    
                    if dir_actual == 0:   y += 1             # Este
                    elif dir_actual == 1: x += 1; y += 1      # Sureste
                    elif dir_actual == 2: x += 1             # Sur
                    elif dir_actual == 3: x += 1; y -= 1      # Suroeste
                    elif dir_actual == 4: y -= 1             # Oeste
                    elif dir_actual == 5: x -= 1; y -= 1      # Noroeste
                    elif dir_actual == 6: x -= 1             # Norte
                    elif dir_actual == 7: x -= 1; y += 1      # Noreste
                    
                    # Verificación de límites
                    if 0 <= x < filas and 0 <= y < columnas:
                        matriz_perimetro[x, y] = 1


                matriz_rellena = binary_fill_holes(matriz_perimetro).astype(int)

                # 5. Mostrar imagen corregida
                img_bw = (matriz_rellena * 255).astype(np.uint8)
                imagen_pil = Image.fromarray(img_bw, mode='L')
                imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)
                
                nueva_img_tk = ImageTk.PhotoImage(imagen_pil)
                label_interfaz.config(image=nueva_img_tk)
                label_interfaz.image = nueva_img_tk

            elif tipo == "VCC":
                from scipy.ndimage import binary_fill_holes
                
                self.representar_pixeles()
                filas, columnas = self.matriz_rep_pixeles.shape
                
                # Buscar inicio dinámico
                x, y = 0, 0
                encontrado = False
                for i in range(filas):
                    for j in range(columnas):
                        if self.matriz_rep_pixeles[i, j] == 1:
                            x, y = i, j
                            encontrado = True
                            break
                    if encontrado:
                        break

                # Procesar cadena
                limpio = texto_cadena.strip("[]")
                cadena = [int(i.strip()) for i in limpio.split(",") if i.strip()]

                matriz_perimetro = np.zeros((filas, columnas))

                # Dirección inicial (derecha)
                dx, dy = 0, 2
                
                matriz_perimetro[x, y] = 1
                n=0
                for giro in cadena:
                    print(giro)


                    if giro == 0:
                        pass  # recto
                    elif giro == 1:  # derecha
                        dx, dy = dy, -dx
                    elif giro == 2:  # izquierda
                        dx, dy = -dy, dx

                    # Punto intermedio (evitar huecos)
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

                # Rellenar figura
                matriz_rellena = binary_fill_holes(matriz_perimetro).astype(int)
                
                matriz_og = self.recuperar_tamaño_original(matriz_rellena)

                img_bw = (matriz_og * 255).astype(np.uint8)
                imagen_pil = Image.fromarray(img_bw, mode='L')
                imagen_pil.thumbnail((350, 350), Image.Resampling.LANCZOS)

                nueva_img_tk = ImageTk.PhotoImage(imagen_pil)
                label_interfaz.config(image=nueva_img_tk)
                label_interfaz.image = nueva_img_tk

                
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
        
        # Actualizar la interfaz (Tkinter)
        entry.delete("0", "end")
        entry.insert("end", "F4 - ")
        entry.insert("end", str(codigo))

        return self.codigo_F4
    
    def f4_2(self):

                
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
    
        return self.codigo_F4

    def f8(self, entry):
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

            


            
            # Dirección 0
            if self.matriz_binaria[x, y+1] == 1 and ((x, y+1) not in pos_recorridas or (x, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y+1, self.matriz_binaria):
                codigo.append(0); y += 1
                pos_recorridas.add((x, y))
            # Dirección 1
            elif self.matriz_binaria[x+1, y+1] == 1 and ((x+1, y+1) not in pos_recorridas or (x+1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y+1, self.matriz_binaria):
                codigo.append(1); x += 1; y += 1
                pos_recorridas.add((x, y))
            # Dirección 2
            elif self.matriz_binaria[x+1, y] == 1 and ((x+1, y) not in pos_recorridas or (x+1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y, self.matriz_binaria):
                codigo.append(2); x += 1
                pos_recorridas.add((x, y))
            # Dirección 3
            elif self.matriz_binaria[x+1, y-1] == 1 and ((x+1, y-1) not in pos_recorridas or (x+1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y-1, self.matriz_binaria):
                codigo.append(3); x += 1; y -= 1
                pos_recorridas.add((x, y))
            # Dirección 4
            elif self.matriz_binaria[x, y-1] == 1 and ((x, y-1) not in pos_recorridas or (x, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y-1, self.matriz_binaria):
                codigo.append(4); y -= 1
                pos_recorridas.add((x, y))
            # Dirección 5
            elif self.matriz_binaria[x-1, y-1] == 1 and ((x-1, y-1) not in pos_recorridas or (x-1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y-1, self.matriz_binaria):
                codigo.append(5); x -= 1; y -= 1
                pos_recorridas.add((x, y))
            # Dirección 6
            elif self.matriz_binaria[x-1, y] == 1 and ((x-1, y) not in pos_recorridas or (x-1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y, self.matriz_binaria):
                codigo.append(6); x -= 1
                pos_recorridas.add((x, y))
            # Dirección 7 (La que te falta)
            elif self.matriz_binaria[x-1, y+1] == 1 and ((x-1, y+1) not in pos_recorridas or (x-1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y+1, self.matriz_binaria):
                codigo.append(7); x -= 1; y += 1
                pos_recorridas.add((x, y))
            else:
                break

            # Verificamos si ya llegamos al origen DESPUÉS de haber movido x, y
            if (x, y) == (inicio_x, inicio_y):
                print("¡Contorno cerrado con el último paso!")
                break
                
            n += 1
        print(f"Código F8 Final: {codigo} (Longitud: {len(codigo)})")
        n=0

        # Actualizar interfaz
        self.codigo_F8 = codigo
        entry.delete("0", tk.END)  
        entry.insert("end", f"F8 - {codigo}")

        return self.codigo_F8
    
    def f8_2(self):
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

            


            
            # Dirección 0
            if self.matriz_binaria[x, y+1] == 1 and ((x, y+1) not in pos_recorridas or (x, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y+1, self.matriz_binaria):
                codigo.append(0); y += 1
                pos_recorridas.add((x, y))
            # Dirección 1
            elif self.matriz_binaria[x+1, y+1] == 1 and ((x+1, y+1) not in pos_recorridas or (x+1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y+1, self.matriz_binaria):
                codigo.append(1); x += 1; y += 1
                pos_recorridas.add((x, y))
            # Dirección 2
            elif self.matriz_binaria[x+1, y] == 1 and ((x+1, y) not in pos_recorridas or (x+1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y, self.matriz_binaria):
                codigo.append(2); x += 1
                pos_recorridas.add((x, y))
            # Dirección 3
            elif self.matriz_binaria[x+1, y-1] == 1 and ((x+1, y-1) not in pos_recorridas or (x+1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x+1, y-1, self.matriz_binaria):
                codigo.append(3); x += 1; y -= 1
                pos_recorridas.add((x, y))
            # Dirección 4
            elif self.matriz_binaria[x, y-1] == 1 and ((x, y-1) not in pos_recorridas or (x, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x, y-1, self.matriz_binaria):
                codigo.append(4); y -= 1
                pos_recorridas.add((x, y))
            # Dirección 5
            elif self.matriz_binaria[x-1, y-1] == 1 and ((x-1, y-1) not in pos_recorridas or (x-1, y-1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y-1, self.matriz_binaria):
                codigo.append(5); x -= 1; y -= 1
                pos_recorridas.add((x, y))
            # Dirección 6
            elif self.matriz_binaria[x-1, y] == 1 and ((x-1, y) not in pos_recorridas or (x-1, y) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y, self.matriz_binaria):
                codigo.append(6); x -= 1
                pos_recorridas.add((x, y))
            # Dirección 7 (La que te falta)
            elif self.matriz_binaria[x-1, y+1] == 1 and ((x-1, y+1) not in pos_recorridas or (x-1, y+1) == (inicio_x, inicio_y)) and self.verificar_vecidnad_N4(x-1, y+1, self.matriz_binaria):
                codigo.append(7); x -= 1; y += 1
                pos_recorridas.add((x, y))
            else:
                break

            # Verificamos si ya llegamos al origen DESPUÉS de haber movido x, y
            if (x, y) == (inicio_x, inicio_y):
                print("¡Contorno cerrado con el último paso!")
                break
                
            n += 1
        print(f"Código F8 Final: {codigo} (Longitud: {len(codigo)})")
        n=0

        # Actualizar interfaz
        self.codigo_F8 = codigo


        return self.codigo_F8

    def af8(self, entry):
        codigo = self.f8_2() # Obtiene F8 absoluto
        if not codigo: return []
        
        # El primer elemento es la dirección absoluta inicial
        a_f8 = [int(codigo[0])] 
        
        # Los demás son los diferenciales (giros)
        for i in range(len(codigo) - 1):
            aux = (int(codigo[i+1]) - int(codigo[i])) % 8
            a_f8.append(aux)
            
        self.codigo_AF8 = a_f8
        # ... (resto de tu print y entry)
        
        print(f"Código AF8 Final: {a_f8} (Longitud: {len(a_f8)})")

        entry.delete("0",tk.END) 
        entry.insert("end","AF8 - ")   
        entry.insert("end",str(a_f8))

        return self.codigo_AF8

    def vcc_3(self, entry):
        self.representar_pixeles()
        filas, columnas = self.matriz_rep_pixeles.shape

        # 🔍 Buscar primer pixel (inicio)
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

        # 👉 Dirección inicial (derecha en escala 2)
        dir_anterior = (0, 2)

        max_iter = filas * columnas
        n = 0

        while n < max_iter:
            movido = False

            dx, dy = dir_anterior

            # 🔥 IMPORTANTE: NO pisar dx, dy
            opciones = [
                (-dy, dx),   # izquierda primero
                (dx, dy),    # recto
                (dy, -dx)    # derecha
            ]
            for ndx, ndy in opciones:

                nx, ny = x + ndx, y + ndy

                if (0 <= nx < filas and 0 <= ny < columnas and
                    self.matriz_rep_pixeles[nx, ny] == 1 and
                    ((nx, ny) not in pos_recorridas or (nx, ny) == (start_x, start_y))):

                    # 🧠 Calcular giro correctamente
                    x1, y1 = dir_anterior
                    x2, y2 = ndx, ndy

                    giro_val = x1 * y2 - y1 * x2

                    if giro_val == 0:
                        codigo.append(0)  # recto
                    elif giro_val < 0:
                        codigo.append(1)  # derecha
                    else:
                        codigo.append(2)  # izquierda

                    # 🚶 mover
                    x += ndx
                    y += ndy

                    dir_anterior = (ndx, ndy)
                    pos_recorridas.append((x, y))

                    # 🔁 cierre de ciclo
                    if (x, y) == (start_x, start_y):
                        movido = True
                        break

                    movido = True
                    break

            if not movido:
                break

            n += 1

        # 🧾 guardar resultado
        self.codigo_VCC3 = codigo
        entry.delete("0", "end")
        entry.insert("end", f"VCC - {codigo}")

        return codigo
    
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
        entry.insert("end","3OT - ")  
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
     
        