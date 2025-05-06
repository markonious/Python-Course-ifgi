# Load layers
districts_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
schools_layer = QgsProject.instance().mapLayersByName("Schools")[0]

# Prepare spatial index for faster lookup
index = QgsSpatialIndex(schools_layer.getFeatures())

# Loop over each district
for district in districts_layer.getFeatures():
    geom = district.geometry()
    
    # Use spatial index to find nearby points first
    possible_ids = index.intersects(geom.boundingBox())
    
    # Filter points actually inside the polygon
    count = 0
    for fid in possible_ids:
        point_feat = schools_layer.getFeature(fid)
        if geom.contains(point_feat.geometry()):
            count += 1

    # Get district name
    district_name = district["Stat_Name"]  # Make sure this field exists
    print(f"{district_name}: {float(count)}")
