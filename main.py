from controller import webServer
from controller.ErreseinaController import ErreseinaController

erreseinak = ErreseinaController()

erreseinak.kargatu()
webServer.app.run(debug=True)
