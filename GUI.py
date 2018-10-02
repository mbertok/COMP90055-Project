import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from Server import create_server
from threading import Thread
from FileValidator import Validate
import tkinter

import random
class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setEnvironment=False
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
     #   self.infection_length_label = QLabel("Infection length(Days)", self)#Not using
      #  self.infection_length = QLineEdit("")
#        self.editable.append(self.infection_length)
        self.exposure_label = QLabel("Exposure length(Days)", self)
        self.exposure = QLineEdit("")
        self.editable.append(self.exposure)
        self.recover_label = QLabel("Time taken to recover (Days)", self)
        self.recover = QLineEdit("")
        self.editable.append(self.recover)
        self.port_label=QLabel("Port",self)
        self.port=QLineEdit("")
        self.editable.append(self.port)
        self.school_label=QLabel("Proportion of schools(%)")
        self.prop_school=QSpinBox()
        self.prop_school.setRange(0,100)
        self.home_label = QLabel("Proportion of homes(%)")
        self.prop_home = QSpinBox()
        self.prop_home.setRange(0, 100)
        self.workplace_label = QLabel("Proportion of workplaces(%)")
        self.prop_workplace = QSpinBox()
        self.prop_workplace.setRange(0, 100)
        self.hub_label = QLabel("Proportion of Hubs(%)")
        self.prop_hub = QSpinBox()
        self.prop_hub.setRange(0, 100)
        #self.prop_school.setSingleStep(0.01)




        self.button = QPushButton("Create simulation")
        self.ran_button = QPushButton("Create  random simulation")
        self.ConfigLoad = QPushButton("Upload config")

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.agent,1,0)
        layout.addWidget(self.numb_agent,1,1,1,1)
        layout.addWidget(self.student_prop_label, 1, 2)
        layout.addWidget(self.student_prop,1,3,1,1)
        layout.addWidget(self.worker_prop_label, 2, 2)
        layout.addWidget(self.worker_prop,2,3,1,1)
        layout.addWidget(self.retire_prop_label, 3, 2)
        layout.addWidget(self.retire_prop,3,3,1,1)
        layout.addWidget(self.school_label,4,2)
        layout.addWidget(self.prop_school,4,3,1,1)
        layout.addWidget(self.workplace_label, 5, 2)
        layout.addWidget(self.prop_workplace, 5, 3, 1, 1)
        layout.addWidget(self.home_label, 6, 2)
        layout.addWidget(self.prop_home, 6, 3, 1, 1)
        layout.addWidget(self.hub_label, 7, 2)
        layout.addWidget(self.prop_hub, 7, 3, 1, 1)




        layout.addWidget(self.width_label,2,0)
        layout.addWidget(self.width,2,1,1,1)
        layout.addWidget(self.height_label,3,0)
        layout.addWidget(self.height,3,1,1,1)
        layout.addWidget(self.infection_label, 4, 0)
        layout.addWidget(self.infection,4,1,1,1)
    #    layout.addWidget(self.infection_length_label, 5, 0)
    #    layout.addWidget(self.infection_length,5,1,1,1)
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
        self.ran_button.clicked.connect(self.create_Random_simulation)


    def load_config(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open configuration file')
        if Validate(self.file):
            file_open=open(self.file[0],'r')
          #  parameters=["numb_agents","prop_student","prop_worker","prop_retiree","width","height","expose_time","infect_time"]
            parameters=[]
            parameter={}
            stations={}
            homes=[]
            workplaces=[]
            schools=[]
            shops=[]
            entertain=[]
            connected={}
            self.homecapacity={}
            self.schoolcapacity={}
            self.workplacecapacity={}
            self.shopcapacity={}
            self.entertaincapacity={}
            self.setEnvironment=True

            line_count=0
            with file_open:
                text = file_open.read()
                text=text.split("\n")
                for line in text:
                    print(line)
                    line_count+=1
                    print(line_count)
                    t=line.split(",")
                    if t[0]=="Agent Pop":
                        parameters = ["numb_agents", "prop_student", "prop_worker", "prop_retiree"]
                        t=t[1:]
                        print(t)
                        for i in range(len(parameters)):
                            print(t[i])
                            parameter[parameters[i]]=t[i]
                            #print(t[i])
                        self.numb_agent.setText(parameter["numb_agents"])
                        self.student_prop.setText(parameter["prop_student"])
                        self.worker_prop.setText(parameter["prop_worker"])
                        self.retire_prop.setText(parameter["prop_retiree"])

                    elif t[0]=="Model":
                        parameters = ["width","height","expose_time","recover_time","infect_rate","port"]
                        t =t[1:]
                        for i in range(len(parameters)):
                            parameter[parameters[i]] = t[i]
                            print(parameter[parameters[i]])
                        self.width.setText(parameter["width"])
                        self.height.setText(parameter["height"])
                        self.exposure.setText(parameter["expose_time"])
                        #self.infection_length.setText(parameter["infect_time"])
                        self.infection.setText(parameter["infect_rate"])
                        self.recover.setText(parameter["recover_time"])
                        self.port.setText(parameter["port"])
                    else:
                        #print(text)
                        t=line.split(",")
                        print(t[0])
                        if t[0] == "House":
                            house_info=t
                            house_id=house_info[1]
                            house_coord=house_info[2].split(" ")
                            house_coord=(int(house_coord[0]),int(house_coord[1]))
                            print(house_coord)
                            house_capacity=house_info[3]
                            homes.append((int(house_coord[0]),int(house_coord[1])))
                            print(homes)
                            self.homecapacity[house_coord]=house_capacity
                            print(self.homecapacity[house_coord])
                           # print(house_capacity)

                        elif t[0]=="Rail":
                            #print("hub!")
                            #station_info=t[1].split(" ")
                            station_id=t[1]
                            print(station_id)
                            station_coords=t[2].split(" ")
                            station_coord=(station_coords[0],station_coords[1])
                           # print(station_coord)
                            station_connected=t[3]
                            stations[station_id]=station_coord
                            connected[station_id]=station_connected
                          #  print(station_connected)
                          #  for s in station_connected:
                          #      print ("c"+str(s))
                        elif t[0]=="School":
                            school_id = t[1]
                            school_info = t[2].split(" ")
                            school_coord = (int(school_info[0]),int(school_info[1]))
                            print(school_coord)
                            school_capacity = t[3]
                            schools.append(school_coord)
                            self.schoolcapacity[school_coord]=school_capacity
                            print( self.schoolcapacity[school_coord])
                        elif t[0]=="Workplace":
                            workplace_id = t[1]
                            workplace_info = t[2].split(" ")
                            workplace_coord = (int(workplace_info[0]),int(workplace_info[1]))
                            workplace_capacity = t[3]
                            workplaces.append(workplace_coord)
                            self.workplacecapacity[workplace_coord]=workplace_capacity
                        elif t[0] == "Shop":
                            shop_id = t[1]
                            shop_info = t[2].split(" ")
                            shop_coord = (int(shop_info[0]), int(shop_info[1]))
                            shop_capacity = t[3]
                            shops.append(shop_coord)
                            self.shopcapacity[shop_coord] = shop_capacity
                        elif t[0] == "Entertain":
                            entertain_id = t[1]
                            entertain_info = t[2].split(" ")
                            entertain_coord = (int(entertain_info[0]), int(entertain_info[1]))
                            entertain_capacity = t[3]
                            entertain.append(entertain_coord)
                            self.entertaincapacity[entertain_coord] = entertain_capacity



            self.hubs={}
            print(connected.keys())
            for k in connected.keys():
                key=stations[k]
                print("Key:"+str(key))
                connect=connected[k].split(" ")
                print(connect)
                to_add=[]
                for c in connect:
                    print("C:"+str(c))
                for c in connect:
                    #c=connect[j]
                    print(c)
                    print(stations[c])
                    to_add.append(stations[c])
                    #if key in self.hubs:
                     #   self.hubs[key]=self.hubs[key].append(stations[c])
                    #else:
                     #   self.hubs[key]=[stations[c]]
                self.hubs[key]=to_add
                print(self.hubs[key])
            #self.hubs=hubs
            self.homes=homes
          #  print("H:"+str(self.homes))
         #   print("H1:"+str(self.homecapacity.keys()))
            self.workplaces=workplaces
            self.schools=schools
            self.shops=shops
            self.entertain=entertain
            for e in self.editable:
                e.setReadOnly(True)
                #e.setText("L")
        else:
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("File Error")
            error_message.showMessage("File is not formatted correctly")

    def verify_config(self):
       agent_numb=isinstance(int(self.numb_agent.text()),int)
       print("testing width")
       width=isinstance(int(self.width.text()),int)
       height=isinstance(int(self.height.text()),int)
       if float(self.infection.text())<=1:
           infect=True
       else:
           infect=False
       exposure=isinstance(int(self.exposure.text()),int)
       print("Exposure")
       recover=isinstance(int(self.recover.text()),int)
       print("Recover")
       port=isinstance(int(self.port.text()),int)
       print("Port")
       if float(self.student_prop.text())+float(self.worker_prop.text())+float(self.retire_prop.text())!=1:
           proportions=False
       else:
           proportions=True
           print("Proportions")
       return agent_numb and width and height and infect and exposure and recover and port and proportions






    def create_Random_simulation(self):
        ran_width=random.randrange(10,40)
        ran_height=random.randrange(10,40)
        ran_agent_num=random.uniform(10,1000)
        ran_exposure=random.uniform(0.5,3)
        ran_recover=random.uniform(3,9)
        ran_infect=random.randrange(0,1)
        ran_port=random.randrange(1000,9999)
        prop1=random.uniform(0,1)
        prop2=random.uniform(0,1)
        prop3=random.uniform(0,1)
        print(str(ran_width)+":"+str(ran_height))
        #sumagents=prop1+prop2+prop3

        prophub=random.uniform(0.03,0.25)
        #print(prophub)
        ran_hub={}
        hubs=self.randomCoordinates(prophub*(ran_width*ran_height),ran_width,ran_height)
        for h in hubs:
            num=random.randrange(2,4)
            hub_elem=[]
           # print(num)
            for i in range(num):
                hub_elem.append(hubs[random.randrange(len(hubs))])
               # else:
                #    ran_hub[h]=ran_hub[h].append(hubs[random.randrange(len(hubs))])

            ran_hub[h]=hub_elem
            #print(ran_hub[h])
        #print(hubs)
        prophome=random.uniform(0.02,0.03)
        propworkplace=random.uniform(0.01,0.03)
        propschool=random.uniform(0.01,0.03)
        prop_total=prophome+propworkplace+propschool
       # print(prophome/prop_total)
        #print(propschool/prop_total)
        #print(propworkplace/prop_total)
        homes=self.randomCoordinates((prophome)*(ran_width*ran_height),ran_width,ran_height)
        home_capacity={}
        for h in homes:
            home_capacity[h]=random.randrange(int(ran_agent_num/2),int(ran_agent_num))
        print("Homes:"+str((prophome)))
        workplaces=self.randomCoordinates((propworkplace)*(ran_width*ran_height),ran_width,ran_height)
        work_capacity = {}
        for w in workplaces:
            work_capacity[w] = random.randrange(int(ran_agent_num/2),int(ran_agent_num))
        print("Workplaces:"+str((propworkplace)))
        schools=self.randomCoordinates((propschool)*(ran_width*ran_height),ran_width,ran_height)
        school_capacity = {}
        for s in schools:
            school_capacity[s] = random.randrange(int(ran_agent_num/2),int(ran_agent_num))
        print("Schools:"+str((propschool)))
        #print(homes)
        #print(workplaces)
        #print(schools)



        print(str(prop1)+":"+str(prop2)+":"+str(prop3))
        Server=create_server(ran_agent_num,ran_width,ran_height,ran_exposure,ran_recover,ran_infect,prop1,prop2,prop3,ran_hub,homes,schools,workplaces,
                             home_capacity,school_capacity,work_capacity)
        Server.port=int(ran_port)
        Server.launch()
    def CreateRandomHubs(self,proportion,width,height):
        network={}
        hubs = self.randomCoordinates(proportion * (width * height), width, height)
        for h in hubs:
            num = random.randrange(2, 4)
            hub_elem = []
            # print(num)
            for i in range(num):
                hub_elem.append(hubs[random.randrange(len(hubs))])
            # else:
            #    ran_hub[h]=ran_hub[h].append(hubs[random.randrange(len(hubs))])

            network[h] = hub_elem
        return network
    def CreateRandomEnvironment(self,number,proportion,width,height):
            capacity={}
            environment=self.randomCoordinates(proportion*(width*height),width,height)
            for e in environment:
                capacity[e]=random.randrange(int(number/2),int(number))
            return environment,capacity

    def randomCoordinates(self,number,width,height):
        out=[]
        for i in range(int(number)):
            x=random.randrange(width)
            if x>width:
                print ("X")
            y=random.randrange(height)
            if y>height:
                print ("Y")
            out.append((x,y))
        return out
    # Greets the user
    def server(self):
        if not self.setEnvironment:
            self.hubs=self.CreateRandomHubs(float(self.prop_hub.text()/100),self.width.text(),self.height.text())
            self.homes,self.homecapacity=self.CreateRandomEnvironment(self.numb_agent.text(),self.prop_home.text(),self.width.text(),self.height.text())
            self.schools,self.schoolcapacity=self.CreateRandomEnvironment(self.numb_agent.text(),self.prop_school.text(),self.width.text(),self.height.text())
            self.workplaces,self.workplacecapacity=self.CreateRandomEnvironment(self.numb_agent.text(),self.prop_workplace.text(),self.width.text(),self.height.text())

        if self.verify_config():
            Server=create_server(int(self.numb_agent.text()),int(self.width.text()),int(self.height.text()),int(self.exposure.text()),int(self.recover.text()),float(self.infection.text()),
                                 float(self.worker_prop.text()),float(self.student_prop.text()),float(self.retire_prop.text()),self.hubs,self.homes,self.schools,self.workplaces,
                                 self.homecapacity,self.schoolcapacity,self.workplacecapacity)
            Server.port = int(self.port.text()) # The default
            Server.launch()
            print("Launched!")
        else:
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("Config Error")
            error_message.showMessage("Invalid Config")

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())