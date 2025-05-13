# ask the user to enter an input
parent = iface.mainWindow()
# This opens a text input dialog and save the input if the user pressed ok
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", 
    "Enter coordinates as latitude, longitude", text=" ")
if bOK:
    try:
        lat_str, lon_str = sCoords.split(",")
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
    except Exception as e:
        QMessageBox.warning(parent, "Error", f"Invalid input format: {e}")

from qgis.core import (
    QgsPointXY, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsProject, QgsGeometry
)

# Create point in WGS84
wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
etrs89 = QgsCoordinateReferenceSystem("EPSG:25832")

point_wgs84 = QgsPointXY(lon, lat)

# Setup transform context
transformer = QgsCoordinateTransform(wgs84, etrs89, QgsProject.instance())
point_etrs89 = transformer.transform(point_wgs84)

layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

point_geom = QgsGeometry.fromPointXY(point_etrs89)
found = False

for feature in layer.getFeatures():
    if feature.geometry().contains(point_geom):
        found = True
        district_name = feature["Name"]  # or the actual field name
        break
from PyQt5.QtWidgets import QMessageBox

if found:
    QMessageBox.information(parent, "Result", f"The point is inside {district_name}.")
else:
    QMessageBox.information(parent, "Result", "The point is NOT inside any Münster city district.")
