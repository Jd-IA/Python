import bpy
import numpy as np
import mathutils

# PARA EL OBJETO
obj = bpy.context.active_object # el objeto en selección
mesh = obj.data # las propiedades del objeto
matrix_world = obj.matrix_world # posición y orientación del objeto actuales

# PARA EL CENTRO DE MASA DEL OBJETO
points = np.array([matrix_world * v.co for v in mesh.vertices]) # conviertiendo cada voxel a coordenadas del espacio
center_of_mass = np.mean(points, axis=0) 
points_centered = points - center_of_mass

# PARA GENERAR LA MATRIZ DE TENSOR DE INERCIA
x, y, z = points_centered.T
I = np.array([
    [np.sum(y**2 + z**2), -np.sum(x * y), -np.sum(x * z)],
    [-np.sum(x * y), np.sum(x**2 + z**2), -np.sum(y * z)],
    [-np.sum(x * z), -np.sum(y * z), np.sum(x**2 + y**2)]
])

eigenvalues, eigenvectors = np.linalg.eigh(I) # función que extrae los Ejes Principales del Tensor de Inercia

# PARA ALINEACIÓN E INVARIANCIA ANTE ROTACIÓN
if np.linalg.det(eigenvectors) < 0:
    eigenvectors[:, 2] *= -1
for i in range(3):
    projection = points_centered @ eigenvectors[:, i]
    if np.sum(projection**3) < 0:
        eigenvectors[:, i] *= -1
if np.linalg.det(eigenvectors) < 0:
    eigenvectors[:, 2] *= -1

rot_matrix = mathutils.Matrix(eigenvectors.tolist()).to_4x4() # convierte los ejes calculados en una matriz de rotación de Blender
rot_matrix.invert()

obj.location = (0, 0, 0) # se traslada el objeto al centro 
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
obj.matrix_world = rot_matrix * obj.matrix_world
