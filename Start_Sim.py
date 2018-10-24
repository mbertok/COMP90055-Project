from GUI import Form
import sys
from PySide2.QtWidgets import QApplication

app = QApplication(sys.argv)
form = Form()#Creating the main GUI
# form.setStyle('Fusion')
form.show()
# Run the main Qt loop
#sys.exit(app.exec_())
app.exec_()