# Get the Schools layer 
layer = iface.activeLayer()

# Get selected features
selected_features = layer.selectedFeatures()

# Set path for CSV file
output_path = "D:/GIS MSc/python is GIS/SchoolReport.csv"  # Make sure this folder exists

# Open file 
with open(output_path, 'w', encoding='utf-8') as file:
    
    file.write("NAME,X,Y\n")
    
    # Loop through selected features
    for feature in selected_features:
        # Getting the school name
        name = feature["NAME"]
        
        # Get geometry and convert it to point
        point = feature.geometry().asPoint()
        x = point.x()
        y = point.y()
        
        # Write to the file
        file.write(f"{name},{x},{y}\n")

# check if the execuction was correct
print("School report exported successfully.")
