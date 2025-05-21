from qgis.core import (
    QgsProject,
    QgsField,
    QgsSpatialIndex,
    QgsFeatureRequest
)
from PyQt5.QtCore import QVariant

# Loading the layers 
pools_layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
districts_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# editing pools layer
pools_layer.startEditing()

# Update Type column values
for feature in pools_layer.getFeatures():
    current_type = feature["Type"]
    new_type = "Hallenbad" if current_type == "H" else "Freibad" if current_type == "F" else current_type
    pools_layer.changeAttributeValue(feature.id(), feature.fieldNameIndex("Type"), new_type)

# Step 2: Add a new 'district' column (string, 50 characters)
if "district" not in [field.name() for field in pools_layer.fields()]:
    pools_layer.dataProvider().addAttributes([QgsField("district", QVariant.String, len=50)])
    pools_layer.updateFields()

# Step 3: Create spatial index for faster lookup
district_index = QgsSpatialIndex(districts_layer.getFeatures())

# Step 4: Spatial join – assign district name to each pool
district_name_field = "name"  # Change this if your district name field has a different name.
for pool in pools_layer.getFeatures():
    point = pool.geometry().asPoint()
    intersecting_ids = district_index.intersects(pool.geometry().boundingBox())

    for dist_id in intersecting_ids:
        district = districts_layer.getFeature(dist_id)
        if district.geometry().contains(pool.geometry()):
            district_name = district[district_name_field]
            pools_layer.changeAttributeValue(pool.id(), pools_layer.fields().indexOf("district"), district_name)
            break

# Save changes
pools_layer.commitChanges()

print("Script completed: 'Type' values updated and 'district' assigned.")
