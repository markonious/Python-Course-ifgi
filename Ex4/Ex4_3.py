import os
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer
)

# Set QGIS installation path
QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.42.1", True)  # Use raw string for path

# Initialize QGIS application
qgs = QgsApplication([], False)
qgs.initQgis()

# Folder containing shapefiles
folder_path = r"D:\GIS MSc\python in GIS and Arch\Python-Course-ifgi\Ex4\Muenster"  # Correct path

# Create new QGIS project instance
project = QgsProject.instance()

# Iterate through files in the folder and filter shapefiles
for filename in os.listdir(folder_path):
    if filename.endswith(".shp"):
        full_path = os.path.join(folder_path, filename)

        # Get filename without extension to use as layer name
        layer_name = os.path.splitext(os.path.basename(filename))[0]

        # Create and validate layer
        layer = QgsVectorLayer(full_path, layer_name, "ogr")
        if layer.isValid():
            project.addMapLayer(layer)
            print(f"Added: {layer_name}")
        else:
            print(f"Invalid shapefile: {filename}")

# Save the project to a new file
project.write(r"D:\GIS MSc\python in GIS and Arch\myFirstProject.qgz")

# Exit QGIS application
qgs.exitQgis()

print("All layers added")
