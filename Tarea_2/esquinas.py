import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk, ImageDraw

class Pixel:

    def __init__(self):
        self.fila             = 0
        self.columna          = 0
        self.matriz_binaria   = []
        self.nombre_imagen    = ""
        self.codigo_F8        = []
        self.codigo_AF8       = []
        self.x_inicio         = 0
        self.y_inicio         = 0
        self.contorno_coords  = []
        self.imagen_original_pil = None

    def cargar_imagen(self, label):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif")]
        )
        if not ruta:
            messagebox.showwarning("Aviso", "No se seleccionó ningún archivo.")
            return

        extensiones_validas = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")
        if not ruta.lower().endswith(extensiones_validas):
            messagebox.showwarning("Aviso", "El archivo seleccionado no es una imagen válida.")
            return

        imagen_og = Image.open(ruta).convert("RGB")
        self.imagen_original_pil = imagen_og
        img_array = np.array(imagen_og)

        self.nombre_imagen = os.path.splitext(os.path.basename(ruta))[0]
        self.fila    = img_array.shape[0]
        self.columna = img_array.shape[1]

        matriz = np.zeros((self.fila, self.columna))
        for i in range(self.fila):
            for j in range(self.columna):
                if img_array[i, j, 0] != 0:
                    matriz[i, j] = 1
        self.matriz_binaria = matriz

        imagen_display = imagen_og.copy()
        imagen_display.thumbnail((350, 350), Image.Resampling.LANCZOS)
        nueva_img_tk = ImageTk.PhotoImage(imagen_display)
        label.config(image=nueva_img_tk)
        label.image = nueva_img_tk
        print("Imagen cargada correctamente.")

    def es_contorno_N4(self, i, j):
        m = self.matriz_binaria
        if m[i, j] == 0:
            return False
        if i == 0 or i == self.fila - 1 or j == 0 or j == self.columna - 1:
            return True
        return (m[i-1, j] == 0 or m[i+1, j] == 0 or
                m[i, j-1] == 0 or m[i, j+1] == 0)

    def f8(self):
        if len(self.matriz_binaria) == 0:
            return []

        codigo = []
        coords = []

        encontrado = False
        x = y = 0
        for i in range(self.fila):
            for j in range(self.columna):
                if self.matriz_binaria[i, j] == 1:
                    x, y = i, j
                    self.x_inicio, self.y_inicio = i, j
                    encontrado = True
                    break
            if encontrado:
                break

        inicio_x, inicio_y = x, y
        pos_recorridas = {(x, y)}
        coords.append((x, y))

        direcciones = [
            (0,  0,  1), (1,  1,  1), (2,  1,  0), (3,  1, -1),
            (4,  0, -1), (5, -1, -1), (6, -1,  0), (7, -1,  1),
        ]

        n = 0
        max_pasos = self.fila * self.columna
        while n < max_pasos:
            movio = False
            for dir_cod, di, dj in direcciones:
                ni, nj = x + di, y + dj
                if (0 <= ni < self.fila and 0 <= nj < self.columna and
                        self.matriz_binaria[ni, nj] == 1 and
                        ((ni, nj) not in pos_recorridas or
                         (ni, nj) == (inicio_x, inicio_y)) and
                        self.es_contorno_N4(ni, nj)):
                    codigo.append(dir_cod)
                    x, y = ni, nj
                    pos_recorridas.add((x, y))
                    coords.append((x, y))
                    movio = True
                    break
            if not movio:
                break
            if (x, y) == (inicio_x, inicio_y):
                break
            n += 1

        self.codigo_F8 = codigo
        self.contorno_coords = coords
        return codigo

    def calcular_af8(self, codigo_f8):
        if not codigo_f8:
            return []

        a_f8 = [int(codigo_f8[0])]
        for i in range(len(codigo_f8) - 1):
            valor = (int(codigo_f8[i+1]) - int(codigo_f8[i])) % 8
            a_f8.append(valor)
        return a_f8

    def detectar_dss_gramatica(self, af8):
        n = len(af8)
        if n == 0:
            return []

        A, B, H = 0, 1, 7
        break_points = []
        i = 0

        while i < n:
            break_points.append(i)

            i += 1
            if i >= n:
                break

            while i < n and af8[i] == A:
                i += 1
            if i >= n:
                break

            patron = None
            if af8[i] == B and i + 1 < n and af8[i+1] == H:
                patron = (B, H)
            elif af8[i] == H and i + 1 < n and af8[i+1] == B:
                patron = (H, B)

            if patron is None:
                continue

            s1, s2 = patron
            while i < n:
                if i < n and af8[i] == s1:
                    i += 1
                else:
                    break
                if i < n and af8[i] == s2:
                    i += 1
                else:
                    break
                while i < n and af8[i] == A:
                    i += 1

        return break_points

    def calcular_perimetro_N4(self):

        perimetro = 0
        matriz = self.matriz_binaria

        for i in range(self.fila):
            for j in range(self.columna):
                if matriz[i, j] == 1:
                    if (i == 0 or i == self.fila - 1 or
                            j == 0 or j == self.columna - 1):
                        perimetro += 1
                    else:
                        if (matriz[i-1, j] == 0 or matriz[i+1, j] == 0 or
                                matriz[i, j-1] == 0 or matriz[i, j+1] == 0):
                            perimetro += 1

        return perimetro

    def calcular_cr(self, n, dp):

        if dp == 0:
            return 0.0
        return round(n / dp, 4)

    def calcular_ise(self, coords, indices_bp):

        ise   = 0.0
        n_bp  = len(indices_bp)
        n_pts = len(coords)

        for seg in range(n_bp):
            i_ini = indices_bp[seg]
            i_fin = indices_bp[(seg + 1) % n_bp]

            xk  = float(coords[i_ini][1])
            yk  = float(coords[i_ini][0])

            xk1 = float(coords[i_fin][1])
            yk1 = float(coords[i_fin][0])

            dxk = xk1 - xk
            dyk = yk1 - yk

            if i_fin > i_ini:
                rango = range(i_ini, i_fin + 1)
            else:
                rango = list(range(i_ini, n_pts)) + list(range(0, i_fin + 1))

            for k in rango:
                xi = float(coords[k][1])
                yi = float(coords[k][0])

                numerador   = ((xi - xk) * dyk - (yi - yk) * dxk) ** 2
                denominador = dxk ** 2 + dyk ** 2

                if denominador == 0:
                    d2 = 0.0
                else:
                    d2 = numerador / denominador

                ise += d2

        return round(ise, 4)

    def calcular_fom(self, n, dp, ise):
 
        if dp == 0 or ise == 0:
            return 0.0
        return round(n / (dp * ise), 4)

    def esquinas(self, entry_num_puntos_quiebre, label_resultado,
                 lbl_perimetro, lbl_cr, lbl_ise, lbl_fom):
        if len(self.matriz_binaria) == 0:
            messagebox.showwarning("Aviso", "No se ha cargado una imagen.")
            return

        codigo_f8 = self.f8()
        if not codigo_f8:
            messagebox.showwarning("Aviso", "No se pudo trazar el contorno.")
            return

        coords = self.contorno_coords
        n = len(coords)

        af8 = self.calcular_af8(codigo_f8)
        self.codigo_AF8 = af8

        indices_bp = self.detectar_dss_gramatica(af8)
        if len(indices_bp) < 3:
            paso = max(1, n // 20)
            indices_bp = []
            for k in range(0, n, paso):
                indices_bp.append(k)

        dp = len(indices_bp)

        perimetro = self.calcular_perimetro_N4()
        cr        = self.calcular_cr(n, dp)
        ise       = self.calcular_ise(coords, indices_bp)
        fom       = self.calcular_fom(n, dp, ise)

        img_poly = self.dibujar_poligono(coords, indices_bp)
        if img_poly is None:
            return

        img_tk = ImageTk.PhotoImage(img_poly)
        label_resultado.config(image=img_tk)
        label_resultado.image = img_tk
        label_resultado.update_idletasks()

        entry_num_puntos_quiebre.config(state="normal")
        entry_num_puntos_quiebre.delete(0, tk.END)
        entry_num_puntos_quiebre.insert(0, str(dp))
        entry_num_puntos_quiebre.config(state="readonly")

        lbl_perimetro.config(text=str(perimetro))
        lbl_cr.config(text=str(cr))
        lbl_ise.config(text=str(ise))
        lbl_fom.config(text=str(fom))

    def dibujar_poligono(self, coords, indices_bp):
        if not coords or not indices_bp:
            return None

        img_out = self.imagen_original_pil.copy()
        img_out.thumbnail((350, 350), Image.Resampling.LANCZOS)
        ancho, alto = img_out.size
        draw = ImageDraw.Draw(img_out)

        escala_x = ancho / self.columna
        escala_y = alto  / self.fila

        vertices = []
        for i in indices_bp:
            fila = coords[i][0]
            col  = coords[i][1]
            x    = int(col  * escala_x)
            y    = int(fila * escala_y)
            vertices.append((x, y))

        draw.line(vertices + [vertices[0]], fill="#2196F3", width=2)

        r = 5
        for v in vertices:
            draw.ellipse([v[0]-r, v[1]-r, v[0]+r, v[1]+r],
                         fill="#FF8C00", outline="white", width=1)

        return img_out