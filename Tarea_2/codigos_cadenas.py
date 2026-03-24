from tkinter import filedialog
from PIL import Image
import numpy as np
import os

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

    def cargar_imagen(self):
        ruta_imagen_og = filedialog.askopenfilename()

        if ruta_imagen_og:

            imagen_og = Image.open(ruta_imagen_og).convert("RGB")
            img_og_array = np.array(imagen_og)

            fila = img_og_array.shape[0]

            self.set_fila(fila)

            columna = img_og_array.shape[1]

            self.set_columna(columna)

            print(f"Dimensiones Original: {img_og_array.shape}")

            matriz = np.zeros((fila, columna))

            for i in range(fila):
                for j in range(columna):
                    if (img_og_array[i, j, 0] != 0):
                        matriz[i, j] = 1
            
            self.set_matriz_binaria(matriz)
            
            print("Datos de matriz binaria cargados...")
        else:
            print("No se abrio una imagen")

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
        matriz=self.matriz_binaria
        for i in range(0,self.fila-1):
            for j in range(0,self.columna-1):
                if [i,j]==1:
                    aux=i
                    aux_2=j
                    if(matriz[aux-1,aux_2]==0 or matriz[aux,aux_2-1]==0 or matriz[aux+1,aux_2]==0 or matriz[aux,aux_2+1]==0):
                        perimetro=perimetro+1
                        matriz_perimetro[i,j]=1
        
        print(f"Perimetro N4: {perimetro}")

        self.set_matriz_N4(matriz_perimetro, perimetro)

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
            #print(matriz_representacion)
            #text = ""
            #for i in range(filas_rep):
                #linea = ",".join(str(int(matriz_representacion[i, j])) for j in range(cols_rep))
                #text += linea + "\n"

            #carpeta_destino = r"C:\Users\Golde\Documentos\Python\Code-chain"
            #if not os.path.exists(carpeta_destino):
                #os.makedirs(carpeta_destino)

            #nombre_archivo = os.path.join(carpeta_destino, "representacion_pixeles.txt")
            #with open(nombre_archivo, "w") as archivo:
                #archivo.write(text)
            
            #print(f"Archivo guardado con solapamiento en: '{nombre_archivo}'.")
    def formato_codificado(self, x, y, codigo, alto, ancho):
        texto=f"{alto}x{ancho} {x},{y} {codigo}"

        return texto
    
    def verificar_vecidnad_N8(self,i,j, matriz):
        vecindad_n8 = False

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
                
                vecindad_n8=True

        return vecindad_n8
    def verificar_vecidnad_N4(self, i, j, matriz):
        vecindad_n4 = False

        if matriz[i, j] == 1:
            aux = i
            aux_2 = j
            if (matriz[aux-1, aux_2] == 0 or 
                matriz[aux, aux_2-1] == 0 or 
                matriz[aux+1, aux_2] == 0 or
                matriz[aux, aux_2+1] == 0): 
                
                vecindad_n4 = True

        return vecindad_n4
    def f4(self):

        codigo = []
        x = 0
        y = 0
        
        encontrado = False
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    x = i 
                    y = j
                    #print(f"Primer 1 encontrado en x: {x}, y: {y}")
                    encontrado = True
                    break  
            if encontrado:
                break  
        final_x = x
        final_y = y

        pos_recorridas = []
        #pos_recorridas.append((x, y))

        n = 0
    
        while (n < self.fila*self.columna):
            # Guardamos x, y actuales para comparar después si hubo movimiento
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
            
            #print(f"{x},{y}")

            # Condición de parada: si regresamos al punto inicial
            if x == final_x and y == final_y:
                #print("Contorno cerrado con éxito.")
                break
                
            n += 1
        n=0
        print(f"Código F4 Final: {codigo} (Longitud: {len(codigo)})")

        self.codigo_F4= codigo

        return self.codigo_F4

        #print(f"Trayectoria: {pos_recorridas}")
        #print(f"codiog F4: {codigo}")
        #print(f"Longitud del codigo: {len(codigo)}")
        #print(f"Perimetro total: {perimetro}") 


        #codec=formato_codificado(final_x,final_y,codigo,fila,columna)

        #nombre = os.path.basename(ruta_archivo_og)
        #carpeta_destino = r"C:\Users\Golde\Documentos\Python\Code-chain"
        
        #if not os.path.exists(carpeta_destino):
        #    os.makedirs(carpeta_destino)

        #nombre_archivo = os.path.join(carpeta_destino, f"codigo_F4_{nombre}")

        #with open(nombre_archivo, "w") as archivo:
        #    archivo.write(codec)
        
        #else:
        #    print("No se abrio un arhcivo txt")

    def f8(self):

        codigo = []
        x = 0
        y = 0
        
        encontrado = False
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    x = i 
                    y = j
                    #print(f"Primer 1 encontrado en x: {x}, y: {y}")
                    encontrado = True
                    break  
            if encontrado:
                break  
        final_x = x
        final_y = y

        pos_recorridas = []
        #pos_recorridas.append((x, y))

        n = 0
        while (n < self.fila*self.columna):

            
            if self.matriz_binaria[x, y+1] == 1 and ((x, y+1) not in pos_recorridas) and self.verificar_vecidnad_N8(x, y+1, self.matriz_binaria):
                codigo.append(0) 
                y += 1
            elif self.matriz_binaria[x+1, y+1] == 1 and ((x+1,y+1) not in pos_recorridas) and self.verificar_vecidnad_N8(x+1, y+1, self.matriz_binaria):
                codigo.append(1)
                x += 1
                y += 1
            elif self.matriz_binaria[x+1, y] == 1 and ((x+1,y) not in pos_recorridas)and self.verificar_vecidnad_N8(x+1, y, self.matriz_binaria):
                codigo.append(2)
                x += 1
            elif self.matriz_binaria[x+1, y-1] == 1 and ((x+1,y-1) not in pos_recorridas)and self.verificar_vecidnad_N8(x+1, y-1, self.matriz_binaria):
                codigo.append(3)
                x += 1
                y -= 1
            elif self.matriz_binaria[x, y-1] == 1 and ((x,y-1) not in pos_recorridas)and self.verificar_vecidnad_N8(x, y-1, self.matriz_binaria):
                codigo.append(4)
                y -= 1
            elif self.matriz_binaria[x-1, y-1] == 1 and ((x-1,y-1) not in pos_recorridas)and self.verificar_vecidnad_N8(x-1, y-1, self.matriz_binaria):
                codigo.append(5)
                x -= 1
                y -= 1
            elif self.matriz_binaria[x-1, y] == 1 and ((x-1,y) not in pos_recorridas)and self.verificar_vecidnad_N8(x-1, y, self.matriz_binaria):
                codigo.append(6)
                x -= 1
            elif self.matriz_binaria[x-1, y+1] == 1 and ((x-1,y+1) not in pos_recorridas)and self.verificar_vecidnad_N8(x-1, y+1, self.matriz_binaria):
                codigo.append(7)
                x -= 1
                y += 1


            pos_recorridas.append((x, y))
            #print(f"{x},{y}")

            if x == final_x and y == final_y:
                #print("Contorno cerrado con éxito.")
                break
            n += 1
        
        
        #print(f"Numero de pasos: {n}")
        n=0
        print(f"Código F8 Final: {codigo} (Longitud: {len(codigo)})")

        self.codigo_F8 = codigo

        return self.codigo_F8
    
    def af8(self):
        #codigo de f8 a af8
        codigo = self.f8()
        a_f8=[]
        aux=0
        for i in range(len(codigo)-1):
            aux = (int(codigo[i+1])-int(codigo[i]))%8
            a_f8.append(aux)
        aux = (int(codigo[int(len(codigo)-1)])-int(codigo[0]))%8

        a_f8.append(aux)

        self.codigo_AF8=a_f8
        
        print(f"Código AF8 Final: {a_f8} (Longitud: {len(a_f8)})")

        return self.codigo_AF8

    def vcc_3(self):
        self.vecindad_N8()
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
                # Conteo de conectividad: Total - 1
                caminos_totales = 0
                if y+2 < columna and self.matriz_rep_pixeles[x, y+2] == 1: caminos_totales += 1
                if x+2 < fila    and self.matriz_rep_pixeles[x+2, y] == 1: caminos_totales += 1
                if y-2 >= 0      and self.matriz_rep_pixeles[x, y-2] == 1: caminos_totales += 1
                if x-2 >= 0      and self.matriz_rep_pixeles[x-2, y] == 1: caminos_totales += 1
                
                codigo.append(caminos_totales - 1)
                pos_recorridas.append((x, y))
                
                if x == final_x and y == final_y:
                    #print("Contorno cerrado")
                    break
            else:
                break
            n += 1
        n=0
        print(f"Código VCC Final: {codigo} (Longitud: {len(codigo)})")

        self.codigo_VCC3 = codigo

        return self.codigo_VCC3

        #codec = self.formato_codificado(self.x_inicio, self.y_inicio, codigo, self.fila, self.columna)

        #nombre = os.path.basename(self.ruta_archivo_og)

        #carpeta_destino = r"C:\Users\Golde\Documentos\Python\Code-chain"
        
        #if not os.path.exists(carpeta_destino):
        #    os.makedirs(carpeta_destino)

        #nombre_archivo = os.path.join(carpeta_destino, f"codigo_VCC3_{nombre}")

        #with open(nombre_archivo, "w") as archivo:
        #    archivo.write(codec)

    def _3ot(self):
        # Obtenemos el código F4
        codigo = self.f4() 
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
        return self.codigo_3OT
        
        

#pixeles = Pixel()
#pixeles.cargar_imagen()
#pixeles.vecindad_N8()
#pixeles.representar_pixeles()
#pixeles.vcc_3()