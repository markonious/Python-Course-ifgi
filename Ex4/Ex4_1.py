from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# Get the value of the district name 
district_name = '["Stat_Name"]'  # This dynamically gets the value from the field

# Format name for Wikipedia URL
formatted_name = district_name.replace(' ', '_')

# Build the Wikipedia URL
url = f"https://en.wikipedia.org/wiki/{formatted_name}"

# Open it in a pop-up window
webview = QWebView()
webview.load(QUrl(url))
webview.setWindowTitle(f"Wikipedia  - {district_name}")
webview.resize(800, 600)
webview.show()
