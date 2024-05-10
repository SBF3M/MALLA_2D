# -*- coding: utf-8 -*-
# Proyecto SBFEM
# Código de python para integrar GMSH y MATLAB

import gmsh
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("modelo_1")

tm = 2
tmr = 0.01

# PUNTOS
gmsh.model.geo.addPoint(0, 0, 0, tmr, 0)
gmsh.model.geo.addPoint(0.05, 0, 0, tmr, 1)
gmsh.model.geo.addPoint(0.1, 0, 0, tmr, 2)
gmsh.model.geo.addPoint(0, 0.1, 0, tmr, 3)
gmsh.model.geo.addPoint(0, 0.05, 0, tmr, 4)

# LINEAS Y ARCOS

gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addCircleArc(2, 0, 3, 2)
gmsh.model.geo.addLine(3, 4, 3 )
gmsh.model.geo.addCircleArc(4, 0, 1, 4)

# CURVES LOOPS

gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)

# PLANES

gmsh.model.geo.addPlaneSurface([1], 1)

# PHYSICAL GROUP -- Para crear entidades de interés, como una línea o cara cargada

gmsh.model.addPhysicalGroup(1, [1], 101)
gmsh.model.setPhysicalName(1, 101, "Apoyo inferior")

gmsh.model.addPhysicalGroup(1, [3], 103)
gmsh.model.setPhysicalName(1, 103, "Apoyo superior")

gmsh.model.addPhysicalGroup(1, [4], 104)
gmsh.model.setPhysicalName(1, 104, "Linea cargada")

s = gmsh.model.addPhysicalGroup(2, [1])
gmsh.model.setPhysicalName(2, s, "superficie")

# SINCRONIZAR

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.option.setNumber("Mesh.SurfaceFaces", 1)  # Para ver las caras de los elementos finitos
gmsh.option.setNumber("Mesh.Points", 1)        # Ver los nodos de la malla

# GUARDAR MALLA

filename = "malla_2.msh"
gmsh.write(filename)

# VISUALIZAR

gmsh.fltk.run()
gmsh.finalize()



from leer_GMSH import xnod_from_msh, LaG_from_msh, plot_msh

malla = 'malla_2.msh'

# Matriz de coordenadas nodales
xnod = xnod_from_msh(malla, dim=2)

# Se imprimen los primeros 10 nodos
for i in range(10):
    x, y = xnod[i]
    print(f'Nodo {i+1:2.0f}: x = {x:.4f}, y = {y:.4f}')

# Matriz de interconexión nodal
LaG = LaG_from_msh(malla)
nef = LaG.shape[0]

# Se imprimen los primeros 5 elementos y los 5 últimos:
print()
for e in list(range(5)) + list(range(nef-5, nef)):
    print(f'Elemento {e+1:3.0f}: Superficie = {LaG[e, 0]+1},   '
          f'Nodos = {LaG[e, 1:]+1}')
    
top = np.zeros_like(LaG)
for e in range(len(LaG)):
    top[e, :] = LaG[e, :] +1


np.savetxt('top.txt', top, fmt='%d', delimiter=' ')
np.savetxt('coord.txt', xnod, fmt='%.4f', delimiter=' ')
