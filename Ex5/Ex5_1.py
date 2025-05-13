from qgis.PyQt.QtWidgets import QInputDialog, QMessageBox
from qgis.core import QgsExpression, QgsFeatureRequest

parent = iface.mainWindow()
canvas = iface.mapCanvas()

#Accessing layers 
districts_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
schools_layer = QgsProject.instance().mapLayersByName("Schools")[0]

#fetching district names 
district_names = sorted(set(f["Name"] for f in districts_layer.getFeatures()))  

#prompting the user to select a district in a dialogue box
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ", district_names)

if not bOk:
    QMessageBox.warning(parent, "Schools", "User cancelled")
else:
    # Get selected district feature & geometry
    expr = QgsExpression(f""""Name" = '{sDistrict}'""")  
    request = QgsFeatureRequest(expr)
    district_feature = next(districts_layer.getFeatures(request), None)

    if not district_feature:
        QMessageBox.warning(parent, "Schools", "District not found.")
    else:
        district_geom = district_feature.geometry()
        district_centroid = district_geom.centroid()
        district_id = district_feature.id()

        # finding and storing matching schools 
        matching_schools = []
        schools_layer.removeSelection()
        for school in schools_layer.getFeatures():
            school_geom = school.geometry()
            if district_geom.contains(school_geom):
                name = school["NAME"]          
                school_type = school["SchoolType"]   
                distance_m = school_geom.distance(district_centroid)
                distance_km = round(distance_m / 1000.0, 2)
                matching_schools.append((name, school_type, distance_km, school.id()))

        matching_schools.sort(key=lambda x: x[0])
        selected_school_ids = [fid for _, _, _, fid in matching_schools]

        #Highlighting district chosen with the schools 
        districts_layer.removeSelection()
        districts_layer.selectByIds([district_id])

        if not selected_school_ids:
            QMessageBox.information(parent, f"Schools in {sDistrict}", "No schools found in this district.")
        else:
            display_text = ""
            for name, school_type, distance_km, _ in matching_schools:
                display_text += f"{name} ({school_type}) – {distance_km} km to centroid\n"

            QMessageBox.information(parent, f"Schools in {sDistrict}", display_text)
            schools_layer.selectByIds(selected_school_ids)

            # Zooming to selected features
            canvas.zoomToFeatureIds(districts_layer, [district_id])
            canvas.zoomToSelected(schools_layer)
