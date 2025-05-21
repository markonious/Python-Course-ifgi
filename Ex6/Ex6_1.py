import sys
import csv
from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsField,
    QgsFeature,
    QgsGeometry
)

# Fix for large WKT fields
csv.field_size_limit(10_000_000)

# Path to your uploaded CSV file
csv_path = r"C:\Users\hp\Desktop\Python in QGIS and ArcGIS\Exercises\Exercise 6\Data for Session 6\standard_land_value_muenster.csv"

# Create a memory layer with MultiPolygon geometry
layer = QgsVectorLayer('MultiPolygon?crs=EPSG:25832', 'temp_standard_land_value_muenster', 'memory')
provider = layer.dataProvider()

# Add fields
provider.addAttributes([
    QgsField('standard_land_value', QVariant.Double),
    QgsField('type', QVariant.String),
    QgsField('district', QVariant.String)
])
layer.updateFields()

# Read the CSV file
with open(csv_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    features = []

    for row in reader:
        try:
            val = float(row['standard_land_value'].strip())
            land_type = row['type'].strip()
            district = row['district'].strip()
            wkt = row['geometry'].strip()

            geom = QgsGeometry.fromWkt(wkt)
            if not geom or not geom.isGeosValid():
                continue

            feature = QgsFeature()
            feature.setFields(layer.fields())
            feature.setGeometry(geom)
            feature.setAttribute('standard_land_value', val)
            feature.setAttribute('type', land_type)
            feature.setAttribute('district', district)

            features.append(feature)

        except Exception as e:
            continue  # skip any row with parsing errors

# Add features to the layer
provider.addFeatures(features)
layer.updateExtents()

# Add to the QGIS project
QgsProject.instance().addMapLayer(layer)
