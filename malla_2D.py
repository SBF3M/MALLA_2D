# -*- coding: utf-8 -*-
# Proyecto SBFEM
# Código de python para integrar GMSH y MATLAB

import gmsh
import pandas as pd
import os

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

# CÓDIGO PARA EXTRAER LAS COORDENADAS DE NODOS Y TOPOLOGÍA

from leer_GMSH import xnod_from_msh, LaG_from_msh, plot_msh
malla = 'malla_2.msh'

# Matriz de coordenadas nodales
xnod = xnod_from_msh(malla, dim=2)

# Matriz de interconexión nodal
LaG = LaG_from_msh(malla)
nef = LaG.shape[0]


# USO DE PANDAS PARA CREAR DATAFRAMES
df = pd.DataFrame(xnod)
df_top =pd.DataFrame(LaG)

# GUARDAR DATOS

# Exportar data de coordenadas de nodos (TXT)
file_path = os.path.join(os.path.dirname(__file__), 'coordenadas_data.txt')
df.to_csv(file_path, sep=' ', index=True)

# Exportar data de topología (TXT)
file_path = os.path.join(os.path.dirname(__file__), 'topologia_data.txt')
df_top.to_csv(file_path, sep=' ', index=True)