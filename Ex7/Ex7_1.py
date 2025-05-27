from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterEnum,
                       QgsProcessingParameterFileDestination, QgsProject, QgsVectorLayer,
                       QgsProcessingParameterString)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from qgis.utils import iface
from pathlib import Path
import time
import os

# Creating a class for a pdf profile 
class CreateCityDistrictProfile(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        
        # Get the list of district names from the layer
        self.district_names = self.get_district_names()
        # Add a parameter for selecting a district from a dropdown list 
        self.addParameter(
            QgsProcessingParameterEnum(
                'DISTRICT',
                'Select City District',
                options=self.district_names
            )
        )
        # Add a parameter for selecting data type to include in the report
        self.addParameter(
            QgsProcessingParameterEnum(
                'INCLUDE',
                'Include data about:',
                options=['Schools', 'Swimming Pools']
            )
        )
        # Add a parameter to select the destination file path for the output PDF

        self.addParameter(
            QgsProcessingParameterFileDestination(
                'OUTPUT',
                'PDF Output',
                fileFilter='PDF files (*.pdf)'
            )
        )
    
    # retrive the parameters and map the indexs from the layers
    def processAlgorithm(self, parameters, context, feedback):
        district_index = parameters['DISTRICT']
        include_index = parameters['INCLUDE']
        output_path = parameters['OUTPUT']

        district_name = self.district_names[district_index]
        include_option = ['Schools', 'public_swimming_pools'][include_index]

        feedback.pushInfo(f'Generating profile for {district_name}, including {include_option}')

        pdf_path = self.createPDF(district_name, include_option, output_path, feedback)

        return {'OUTPUT': pdf_path}

    # functions for registiratoin of the districts
    def name(self):
        return 'create_city_district_profile'

    def displayName(self):
        return 'Create City District Profile'

    def group(self):
        return 'Custom Scripts'

    def groupId(self):
        return 'customscripts'

    def shortHelpString(self):
        return 'Creates a profile of a Münster city district in PDF format.'

    def createInstance(self):
        return CreateCityDistrictProfile()

    # retrieve the district names in a shortlist form the district layer
    def get_district_names(self):
        layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        names = sorted([f['Name'] for f in layer.getFeatures()])
        return names

    # creating a pdf showing the statistics and map of the snapshot
    def createPDF(self, district_name, include_layer, output_path, feedback):
        project = QgsProject.instance()
        
        # Load relevant layers
        district_layer = project.mapLayersByName('Muenster_City_Districts')[0]
        parcels_layer = project.mapLayersByName('Muenster_Parcels')[0]
        house_layer = project.mapLayersByName('House_Numbers')[0]
        optional_layer = project.mapLayersByName(include_layer)[0]

        selected_feature = next(f for f in district_layer.getFeatures() if f['Name'] == district_name)
        geom = selected_feature.geometry()
        
        # Calculate the area
        area = geom.area() / 1_000_000 
        parent_district = selected_feature['P_District']

        # Count parcels
        parcels = [f for f in parcels_layer.getFeatures() if f.geometry().intersects(geom)]
        parcel_count = len(parcels)

        # Count households
        households = [f for f in house_layer.getFeatures() if f.geometry().intersects(geom)]
        household_count = len(households)

        # Count schools/pools
        optionals = [f for f in optional_layer.getFeatures() if f.geometry().intersects(geom)]
        optional_count = len(optionals)

        # Zoom to selected district 
        iface.mapCanvas().setExtent(geom.boundingBox())
        iface.mapCanvas().refresh()
        time.sleep(5)
        map_img_path = os.path.join(Path(output_path).parent, 'map_snapshot.png')
        iface.mapCanvas().saveAsImage(map_img_path)

        # Create PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, f"City District Profile: {district_name}")
        c.setFont("Helvetica", 12)
        c.drawString(50, 770, f"Parent District: {parent_district}")
        c.drawString(50, 750, f"Area: {area:.2f} km²")
        c.drawString(50, 730, f"Households: {household_count}")
        c.drawString(50, 710, f"Parcels: {parcel_count}")
        c.drawString(50, 690, f"{include_layer.replace('_', ' ').title()}: {optional_count if optional_count > 0 else 'No data available'}")

        # Map image
        c.drawImage(map_img_path, 50, 450, width=500, height=200)

        c.showPage()
        c.save()
        feedback.pushInfo("PDF created successfully.")
        return output_path
