import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from Server import create_server
from threading import Thread
from FileValidator import Validate
import tkinter
import threading
import socket
from PySide2.QtCore import QThread
import multiprocessing
import random
import multiprocessing
import re


def get_port():
    s = socket.socket()
    s.bind(('', 0))  # Bind to a free port provided by the host.
    return s.getsockname()[1]  # Return the port number assigned.
def SimThread(Thread):
    def __init__(self,simulation):
        self.running=False
        self.function=simulation
        super(SimThread(),self).__init__()
    def start(self):
        self.running=True
        super(SimThread(), self).start()
    def run(self):
        while self.running:
            self.function()
    def stop(self):
        self.running=False

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setEnvironment=False
        self.ports=[]
        self.editable=[]
        self.stationary_agents = []
        self.moving_agents = []
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
        self.preventative_toggle_label=QLabel("Implement preventative measures?", self)
        self.preventative_toggle=QCheckBox("", self)
     #   self.infection_length_label = QLabel("Infection length(Days)", self)#Not using
      #  self.infection_length = QLineEdit("")
#        self.editable.append(self.infection_length)
        self.exposure_label = QLabel("Exposure length(Days)", self)
        self.exposure = QLineEdit("")
        self.editable.append(self.exposure)
        self.recover_label = QLabel("Time taken to recover (Days)", self)
        self.recover = QLineEdit("")
        self.editable.append(self.recover)
        self.port_label=QLabel("Port(Auto assigned)",self)
        self.port=QLineEdit(" ")
        self.vacc_rate_label=QLabel("Vaccination Rate(Agents per tick)")
        self.vacc_rate=QLineEdit(" ")
        self.editable.append(self.vacc_rate)
        self.stages_threshold_label = QLabel("Proportion infected for each stage of preventative measures")
        self.stages_threshold = QLineEdit(" ")
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
        self.entertain_label = QLabel("Proportion of Leisure centres(%)")
        self.prop_entertain = QSpinBox()
        self.prop_entertain.setRange(0, 100)
        self.shop_label = QLabel("Proportion of Shops(%)")
        self.prop_shop = QSpinBox()
        self.prop_shop.setRange(0, 100)
        self.export_label=QLabel("Export results?")
        self.export=QCheckBox("",self)
        self.filename_label=QLabel("Filename:")
        self.filename=QLineEdit("")

        #self.prop_school.setSingleStep(0.01)
        self.StartButton = QPushButton("Create simulation")
        #self.DiseaseLoad = QPushButton("Upload disease model")
        self.ran_button = QPushButton("Create  random simulation")
        self.ConfigLoad = QPushButton("Upload config")
        self.quit=QPushButton("Quit")

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
        layout.addWidget(self.entertain_label, 8, 2)
        layout.addWidget(self.prop_entertain, 8, 3, 1, 1)
        layout.addWidget(self.shop_label, 9, 2)
        layout.addWidget(self.prop_shop, 9, 3, 1, 1)
        layout.addWidget(self.export_label,10,2)
        layout.addWidget(self.export,10,3,1,1)
        layout.addWidget(self.filename_label,11,2)
        layout.addWidget(self.filename,11,3,1,1)

        layout.addWidget(self.width_label,2,0)
        layout.addWidget(self.width,2,1,1,1)
        layout.addWidget(self.height_label,3,0)
        layout.addWidget(self.height,3,1,1,1)
        layout.addWidget(self.infection_label, 4, 0)
        layout.addWidget(self.infection,4,1,1,1)
        layout.addWidget(self.preventative_toggle_label, 5, 0)
        layout.addWidget(self.preventative_toggle,5,1,1,1)
        layout.addWidget(self.exposure_label, 6, 0)
        layout.addWidget(self.exposure,6,1,1,1)
        layout.addWidget(self.recover_label, 7, 0)
        layout.addWidget(self.recover, 7, 1, 1, 1)
        layout.addWidget(self.port_label,8,0)
        layout.addWidget(self.port,8,1,1,1)
        self.port.setReadOnly(True)
        layout.addWidget(self.stages_threshold_label,9,0,1,1)
        layout.addWidget(self.stages_threshold,9,1,1,1)
        layout.addWidget(self.vacc_rate_label,10,0,1,1)
        layout.addWidget(self.vacc_rate,10,1,1,1)

        layout.addWidget(self.StartButton, 12, 1, 1, 1)
        layout.addWidget(self.ConfigLoad, 12, 2, 1, 1)
        #layout.addWidget(self.DiseaseLoad, 11, 2, 1, 1)
        layout.addWidget(self.ran_button, 12, 3, 1, 1)
        #layout.addWidget(self.quit)
        # Set dialog layout
        self.setLayout(layout)
        #self.setGeometry(400,400,400,400)
        # Add button signal to greetings slot
        self.StartButton.clicked.connect(self.launch_server)
       # QtCore.QObject.connect(self.StartButton,self.launch_server)
        self.ConfigLoad.clicked.connect(self.load_config)
        self.ran_button.clicked.connect(self.create_Random_simulation)
        self.setWindowTitle('Disease Simulation')
        #self.quit.clicked.connect(exit())


    def load_config(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open configuration file')
        #print(self.file)
        if  not all(self.file):
            #print("Empty")
            return
        if Validate(self.file) :
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
                        parameters = ["width","height","expose_time","recover_time","infect_rate","preventative_on"]
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
                        #print("Pren:"+str((int(parameter["preventative_on"]))))
                        self.preventative_toggle.setChecked(bool(int(parameter["preventative_on"])))
                        #self.port.setText(parameter["port"])
                    elif t[0] == "Preventative":
                        print(line)
                        #self.preventative_toggle.isChecked(True)
                        self.stages_threshold.setText(str((",").join(t[1:4])))
                        self.vacc_rate.setText(str(t[4]))
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
            self.preventative_toggle.setEnabled(False)
            #print(get_port())
        else:
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("File Error")
            error_message.showMessage("File is not formatted correctly")
    def load_disease_model(self):
        #Add file validation
        disease_file=QFileDialog.getOpenFileName(self, 'Open configuration file')
        file_open = open(self.file[0], 'r')
        self.stationary_agents=[]
        self.moving_agents=[]
        self.model_loaded=True
        line_count=0
        with file_open:
            text = file_open.read()
            text = text.split("\n")
            for line in text:
                if line[0]=="Properties":
                    stationary=line[1]
                    numb_agents=line[2]
                    is_random=line[3]
                elif line[0]=="Proportions":
                    stat_prop=line[1]
                    move_prop=line[2]
                else:
                    if line[0]=="Stationary":
                        info=line[1].split(" ")
                        coord_x,coord_y=info[0],info[1]
                        self.stationary_agents.append((coord_x,coord_y))
                    if line[0]=="Moving":
                        info=line[1].split(" ")
                        coord_x,coord_y=info[0],info[1]
                        self.moving_agents.append((coord_x,coord_y))
            #if is_random:
                #Create random agents

    def setError(self,bool, message):
        if not bool:
            self.message=message
        else:
            pass

    def verify_config(self):
       self.message=""
       agent_numb=isinstance(int(self.numb_agent.text()),int)
       vacc=False
       print("testing width")
       width=isinstance(int(self.width.text()),int)
       self.setError(width,"Width is not a number")
       height=isinstance(int(self.height.text()),int)
       self.setError(height,"Height is not a number")
       if float(self.infection.text())<=1:
           infect=True
       else:
           infect=False
           self.setError(infect,"Infection rate is greater than 1")
           #return infect
       exposure=isinstance(int(self.exposure.text()),int)
       if not exposure:
           self.setError(exposure,"Exposure length is not a number")
       print("Exposure")
       recover=isinstance(int(self.recover.text()),int)
       if not recover:
           self.setError(recover,"Recovery length is not a number")
       print("Recover")
       #port=isinstance(int(self.port.text()),int)
       #print("Port")
       if float(self.student_prop.text())+float(self.worker_prop.text())+float(self.retire_prop.text())!=1:
           proportions=False
           self.setError(proportions,"Proportions are not correct")
          # return proportions
       else:
           proportions=True
           print("Proportions")
       if self.preventative_toggle.isChecked():
           vacc=False
           if isinstance(int(self.vacc_rate.text()),int):
               vacc=True
               #print(vacc)
           else:
               vacc=False
               self.setError(vacc,"Vaccination rate is not a number")
               #return vacc
           print("Stages")
           print(len(list(self.stages_threshold.text().split(","))))
           if len(list(self.stages_threshold.text().split(",")))!=3:
               stages=False
               self.setError(stages,"Threshold have not been set correctly")
               #return stages
           else:
               stages=True
       else:
           print(bool)
           if str(self.vacc_rate.text()) and str(self.stages_threshold.text()):
               vacc=True
               stages=True
           else:
               vacc=False
               stages=False
               self.setError(vacc and stages,"Preventative measures not blank")

       #export=False
       if self.export.isChecked():
           matches=re.findall("\w+",str(self.filename.text()))
           if matches and len(matches)==1:
               export=True
           else:
               export=False
               self.setError(export,"Filename is not valid")
               #return export
       else:
           if self.filename.text():
               export=False
               self.setError(export,"Filename field is not blank")
           else:
            export=True
       return agent_numb and width and height and infect and exposure and recover  and proportions and vacc and stages and export

    def create_Random_simulation(self):
        self.StartButton.setEnabled(False)
        self.ran_button.setEnabled(False)
        self.ConfigLoad.setEnabled(False)

        self.sim = threading.Thread(target=self.random_simulation)
        self.sim.setDaemon(True)
        self.sim.start()
       # Server.port=int(ran_port)
        #Server.launch()
    def random_simulation(self):
        ran_width = random.randrange(10, 40)
        ran_height = random.randrange(10, 40)
        ran_agent_num = random.randrange(10, 1000)
        ran_exposure = random.randrange(1, 6)
        ran_recover = random.randrange(3, 9)
        ran_infect = random.uniform(0, 1)
        ran_port = get_port()
        prop1 = random.uniform(0, 1)
        prop2 = random.uniform(0, 1)
        prop3 = random.uniform(0, 1)
        print(str(ran_width) + ":" + str(ran_height))
        # sumagents=prop1+prop2+prop3

        prophub = random.uniform(0.01, 0.25)
        # print(prophub)
        ran_hub = {}
        hubs = self.randomCoordinates(prophub * (ran_width * ran_height), ran_width, ran_height)
        for h in hubs:
            num = random.randrange(2, 4)
            hub_elem = []
            # print(num)
            for i in range(num):
                hub_elem.append(hubs[random.randrange(len(hubs))])
            # else:
            #    ran_hub[h]=ran_hub[h].append(hubs[random.randrange(len(hubs))])

            ran_hub[h] = hub_elem
            # print(ran_hub[h])
        # print(hubs)
        prophome = random.uniform(0.02, 0.2)
        propworkplace = random.uniform(0.01, 0.2)
        propschool = random.uniform(0.01, 0.2)
        prop_leisure = random.uniform(0.01, 0.2)
        prop_shops = random.uniform(0.01, 0.2)
        prop_total = prophome + propworkplace + propschool
        # print(prophome/prop_total)
        # print(propschool/prop_total)
        # print(propworkplace/prop_total)
        homes = self.randomCoordinates((prophome) * (ran_width * ran_height), ran_width, ran_height)
        home_capacity = {}
        for h in homes:
            home_capacity[h] = random.randrange(int(ran_agent_num / 2), int(ran_agent_num))
        print("Homes:" + str((prophome)))
        workplaces = self.randomCoordinates((propworkplace) * (ran_width * ran_height), ran_width, ran_height)
        work_capacity = {}
        for w in workplaces:
            work_capacity[w] = random.randrange(int(ran_agent_num / 2), int(ran_agent_num))
        print("Workplaces:" + str((propworkplace)))
        schools = self.randomCoordinates((propschool) * (ran_width * ran_height), ran_width, ran_height)
        school_capacity = {}
        for s in schools:
            school_capacity[s] = random.randrange(int(ran_agent_num / 2), int(ran_agent_num))
        print("Schools:" + str((propschool)))
        # print(homes)
        # print(workplaces)
        # print(schools)
        leisure = self.randomCoordinates((prop_leisure) * (ran_width * ran_height), ran_width, ran_height)
        shops = self.randomCoordinates((prop_shops) * (ran_width * ran_height), ran_width, ran_height)
        preventative = random.choice([True, False])
        stages_threshold = []
        print(preventative)
        if preventative:
            for s in range(3):
                if s == 0:
                    stages_threshold.append(random.uniform(0.01, 0.2))
                else:
                    stages_threshold.append(stages_threshold[s - 1] + random.uniform(0.02, 0.2))
            vacc_rate = random.uniform(0, 1)
        else:
            vacc_rate = 0

        # export_results=random.choice([True,False])
        export_results = True
        filename = str(ran_port)
        # if export_results:
        # filename=str(ran_port)+"csv"
        # else:
        #   filename=""

        print(str(prop1) + ":" + str(prop2) + ":" + str(prop3))
        self.numb_agent.setText(str(ran_agent_num))
        self.width.setText(str(ran_width))
        self.height.setText(str(ran_height))
        self.exposure.setText(str(ran_exposure))
        self.recover.setText(str(ran_recover))
        self.infection.setText(str(ran_infect))
        self.student_prop.setText(str(prop1))
        self.worker_prop.setText(str(prop2))
        self.retire_prop.setText(str(prop3))
        self.port.setText(str(ran_port))
        self.preventative_toggle.setChecked(preventative)
#        self.stages_threshold.setText(",".join((stages_threshold)))
        print("Stages="+str(stages_threshold))
        create_server(ran_agent_num, ran_width, ran_height, ran_exposure, ran_recover, ran_infect, prop1, prop2, prop3,
                      ran_hub, homes, schools, workplaces,
                      home_capacity, school_capacity, work_capacity, leisure, shops, [], [], preventative,
                      stages_threshold, vacc_rate, export_results, filename, ran_port)
    def CreateRandomHubs(self,proportion,width,height):
        network={}
        hubs = self.randomCoordinates(float(proportion) * int(width) * int(height), width, height)
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
            environment=self.randomCoordinates(float(proportion)*(int(width)*int(height)),width,height)
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
    def simulation(self):
        #self.thread = QtCore.QThread(self)
        self.StartButton.setEnabled(False)
        self.ran_button.setEnabled(False)
        self.ConfigLoad.setEnabled(False)
        self.port.setText(str(get_port()))
        server=create_server(int(self.numb_agent.text()),int(self.width.text()),int(self.height.text()),int(self.exposure.text()),int(self.recover.text()),float(self.infection.text()),
                             float(self.worker_prop.text()),float(self.student_prop.text()),float(self.retire_prop.text()),self.hubs,self.homes,self.schools,self.workplaces,
                             self.homecapacity,self.schoolcapacity,self.workplacecapacity,self.entertain,self.shops,self.stationary_agents,self.moving_agents,self.preventative_toggle.isChecked(),self.stages_threshold.text().split(",")
                             ,self.vacc_rate.text(),self.export.isChecked(),self.filename.text(),int(self.port.text()))
        #server.port = int(self.port.text()) # The default
#           server.moveToThread(self.thread)
       # server.launch()

        #self.thread.start()
        print("Launched!")


        #From https://stackoverflow.com/questions/2838244/get-open-tcp-port-in-python/2838309#2838309
    def launch_server(self):
        if not self.setEnvironment:
            self.hubs = self.CreateRandomHubs(float(int(self.prop_hub.value()) / 100), int(self.width.text()),
                                              int(self.height.text()))
            self.homes, self.homecapacity = self.CreateRandomEnvironment(int(self.numb_agent.text()), float(self.prop_home.value()/100),
                                                                         int(self.width.text()), int(self.height.text()))
            self.schools, self.schoolcapacity = self.CreateRandomEnvironment(int(self.numb_agent.text()),
                                                                             float(self.prop_school.value()/100),
                                                                             int(self.width.text()), int(self.height.text()))
            self.workplaces, self.workplacecapacity = self.CreateRandomEnvironment(int(self.numb_agent.text()),
                                                                                   float(self.prop_workplace.value()/100),
                                                                                   int(self.width.text()),
                                                                                   int(self.height.text()))
            self.entertain = self.randomCoordinates(
                float((self.prop_entertain.value()) /100)* (int(self.width.text()) * int(self.height.text())),
                int(self.width.text()), int(self.height.text()))
            self.shops = self.randomCoordinates(
                float((self.prop_shop.value()/100) * (int(self.width.text())) * int(self.height.text())), int(self.width.text()),
                int(self.height.text()))
            # Get randomised response model
       # self.StartButton.setEnabled(False)
        #self.ran_button.setEnabled(False)
        #self.ConfigLoad.setEnabled(False)
        if self.verify_config():
            self.sim=threading.Thread(target=self.simulation)
            self.sim.setDaemon(True)
            #self.sim=multiprocessing.Process(target=self.server)
            self.sim.start()
        else:
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("Config Error")
            error_message.showMessage(self.message)
            # error_message.setModal(True)
            # error_message.exec_()



    def closeEvent(self, evnt):
        #self.sim.join()
        sys.exit()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    #form.setStyle('Fusion')
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
