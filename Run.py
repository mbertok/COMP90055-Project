from Server import create_server
Server=create_server(10,10)
Server.port = 8521 # The default
Server.launch()

import sys
from PySide2.QtWidgets import QApplication, QMessageBox

# Create the application object
app = QApplication(sys.argv)

# Create a simple dialog box
msg_box = QMessageBox()
msg_box.setText("Hello World!")
msg_box.show()

sys.exit(msg_box.exec_())

