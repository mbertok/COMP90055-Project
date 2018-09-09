import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from Server import create_server
import random
class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.ports=[]
        self.editable=[]
        # Create widgets
        self.agent=QLabel("Number of agents",self)
        self.numb_agent = QLineEdit("")
        self.editable.append(self.numb_agent)
        self.student_prop_label = QLabel("Proportion of students", self)
        self.student_prop = QLineEdit("")
        self.editable.append(self.student_prop)
        self.worker_prop_label = QLabel("Proportion of workers", self)
        self.worker_prop = QLineEdit("")
        self.editable.append(self.worker_prop)
        self.retire_prop_label = QLabel("Proportion of retirees", self)
        self.retire_prop = QLineEdit("")
        self.editable.append(self.retire_prop)
        self.width_label=QLabel("Width of grid(squares)",self)
        self.width=QLineEdit("")
        self.editable.append(self.width)
        self.height_label=QLabel("Height of grid(squares)",self)
        self.height=QLineEdit("")
        self.editable.append(self.height)
        self.infection_label = QLabel("Infection Rate", self)
        self.infection = QLineEdit("")
        self.editable.append(self.infection)
        self.infection_length_label = QLabel("Infection length(Ticks)", self)
        self.infection_length = QLineEdit("")
        self.editable.append(self.infection_length)
        self.exposure_label = QLabel("Exposure length(Ticks)", self)
        self.exposure = QLineEdit("")
        self.editable.append(self.exposure)
        self.recover_label = QLabel("Time taken to recover (Ticks)", self)
        self.recover = QLineEdit("")
        self.editable.append(self.recover)
        self.port_label=QLabel("Port",self)
        self.port=QLineEdit("")
        self.editable.append(self.port)
        self.button = QPushButton("Create simulation")
        self.ran_button = QPushButton("Create  random simulation")
        self.ConfigLoad = QPushButton("Upload config")
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.agent,1,0)
        layout.addWidget(self.numb_agent,1,1,1,1)
        layout.addWidget(self.student_prop_label, 3, 2)
        layout.addWidget(self.student_prop,3,3,1,1)
        layout.addWidget(self.worker_prop_label, 4, 2)
        layout.addWidget(self.worker_prop,4,3,1,1)
        layout.addWidget(self.retire_prop_label, 5, 2)
        layout.addWidget(self.retire_prop,5,3,1,1)
        layout.addWidget(self.width_label,2,0)
        layout.addWidget(self.width,2,1,1,1)
        layout.addWidget(self.height_label,3,0)
        layout.addWidget(self.height,3,1,1,1)
        layout.addWidget(self.infection_label, 4, 0)
        layout.addWidget(self.infection,4,1,1,1)
        layout.addWidget(self.infection_length_label, 5, 0)
        layout.addWidget(self.infection_length,5,1,1,1)
        layout.addWidget(self.exposure_label, 6, 0)
        layout.addWidget(self.exposure,6,1,1,1)
        layout.addWidget(self.recover_label, 7, 0)
        layout.addWidget(self.recover, 7, 1, 1, 1)
        layout.addWidget(self.port_label,8,0)
        layout.addWidget(self.port,8,1,1,1)
        layout.addWidget(self.button,9,1,1,1)
        layout.addWidget(self.ConfigLoad)
        layout.addWidget(self.ran_button)
        # Set dialog layout
        self.setLayout(layout)
        #self.setGeometry(400,400,400,400)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.server)
        self.ConfigLoad.clicked.connect(self.load_config)


    def load_config(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open configuration file')
        file_open=open(self.file[0],'r')
        parameters=["numb_agents","prop_student","prop_worker","prop_retiree","width","height","expose_time","infect_time"]
        parameter={}
        line_count=0
        with file_open:
            text = file_open.read()
            text=text.split("\n")
            for line in text:
                print(text)
                line_count+=1
                print(line_count)
                if line_count==1:
                    parameters = ["numb_agents", "prop_student", "prop_worker", "prop_retiree"]
                    t=line.split(",")
                    print(t)
                    for i in range(len(parameters)):
                        print(t[i])
                        parameter[parameters[i]]=t[i]
                        #print(t[i])
                    self.numb_agent.setText(parameter["numb_agents"])
                    self.student_prop.setText(parameter["prop_student"])
                    self.worker_prop.setText(parameter["prop_worker"])
                    self.retire_prop.setText(parameter["prop_retiree"])

                elif line_count==2:
                    parameters = ["width","height","expose_time","infect_time","recover_time","infect_rate","port"]
                    t = line.split(",")
                    for i in range(len(parameters)):
                        parameter[parameters[i]] = t[i]
                        print(parameter[parameters[i]])
                    self.width.setText(parameter["width"])
                    self.height.setText(parameter["height"])
                    self.exposure.setText(parameter["expose_time"])
                    self.infection_length.setText(parameter["infect_time"])
                    self.infection.setText(parameter["infect_rate"])
                    self.recover.setText(parameter["recover_time"])
                    self.port.setText(parameter["port"])
                else:
                    print(text)
                    t=line.split(":")
                    if t[0] is "House":
                        house_info=t[1].split(",")
                        house_coord=house_info[0]
                        house_id=house_info[1]
                        house_capacity=house_info[2]
                    elif t[0] is "Rail":
                        station_info=t[1].split(",")
                        station_id=station_info[0]
                        station_coord=station_info[1]
                        station_connected=station_info[2]
                        for s in station_connected:
                            print (s)




        for e in self.editable:
            e.setReadOnly(True)
            #e.setText("L")

   # def verify_config(self,parameters):

    def create_Random_simulation(self):
        ran_width=random.randrange(10,100)
        ran_height=random.randrange(10,100)
        ran_agent_num=random.randrange(10,1000)
        ran_exposure=random.randrange(5,100)
        ran_recover=random.randrange(5,100)
        ran_infect=random.randrange(0,1)
        ran_port=random.randrange(1000,9999)
        prop1=random.randrange(0,1)
        prop2=random.randrange(0,1)
        prop3=random.randrange(0,1)
        #sumagents=prop1+prop2+prop3

        prophub=random.randrange(0.3,0.7)

        prophome=random.randrange(0.4,0.9)
        propworkplace=random.randrange(0.4,0.9)
        propschool=random.randrange(0.4,0.9)


        Server=create_server()



    # Greets the user
    def server(self):
        Server=create_server(int(self.width.text()),int(self.height.text()),int(self.numb_agent.text()),int(self.exposure.text()),int(self.recover.text()),float(self.infection.text()),float(self.worker_prop.text()),float(self.student_prop.text()),float(self.retire_prop.text()))
        Server.port = int(self.port.text()) # The default
        Server.launch()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())