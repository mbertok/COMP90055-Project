from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
import sys


#This method checks if the file given is in the correct format
#Input: file, the configuration file needed to be validated
#Output: a boolean indicating if the file is formatted in a valid way
def Validate(file):
    lines = open(file[0], 'r')
   # print("Validation Started")
    housing_max_capacity=0
    school_max_capacity=0
    workplaces_max_capacity=0
    stations={}
    #model = {}
    #agents = {}
    contents=(lines.read().split("\n"))#Getting the file line by line
    #print(contents)

    # initialisation
    agents_info_included = False
    model_info_included = False
    preventative_included = False
    agents={"numb_agents":0, "prop_student":0, "prop_worker":0, "prop_retiree":0}
    model={"width":0, "height":0, "expose_time":0, "recover_time":0, "infect_rate":0}

    for c in range(len(contents)):
        #print(contents[c].split(","))
        line=contents[c].split(",")
        #Checking population data
        if line[0]=="Agent Pop":
           # print("Checking Agent parameters")
            parameters = ["numb_agents", "prop_student", "prop_worker", "prop_retiree"]
            for i in range(len(line[1:])):
                try:
                    agents[parameters[i]]=line[i+1]
                except IndexError:
                    return False
            if not(isinstance(int(agents["numb_agents"]),int) and  isinstance(float(agents["prop_student"]),float)  and  isinstance(float(agents["prop_worker"]),float) and isinstance(float(agents["prop_retiree"]), float)):
               # print("Not correct type")
                return False
           #if proportions do not add up to 1
            if float(agents["prop_student"])+float(agents["prop_worker"])+float(agents["prop_retiree"])!=1:
               return False
            agents_info_included=True
           # print(agents_info_included)
        #Checking model data
        elif line[0]=="Model":
            parameters = ["width", "height", "expose_time", "recover_time", "infect_rate", "preventative_on"]
            for i in range(len(line[1:])):
                try:
                    model[parameters[i]]=line[i+1]
                except IndexError:
                    return False
            #Checking if all fields valid
            if not (isinstance(int(model["width"]), int) and isinstance(int(model["height"]), int) and isinstance(int(model["width"]), int) and isinstance(int(model["expose_time"]), int)
                    and isinstance(int(model["recover_time"]), int) and isinstance(float(model["infect_rate"]), float)):
                    if not ( int(model["preventative_on"])==1 or int(model["preventative_on"])==0):
                        return False
            model_info_included = True
            #print(model_info_included)
        #Checking preventative measures
        elif line[0]=="Preventative":
            if ("preventative_on" in model.keys()) and int(model["preventative_on"])==1 :
                #Checking the proportions
                thresholds=line[1:4]
                for t in range(len(thresholds)):
                    if not(isinstance(float(thresholds[t]),float) and float(thresholds[t])<1):
                        return False
                    if t<(len(thresholds)-1) and float(thresholds[t])>float(thresholds[t+1]):
                        return False
                #print("FLoat")
                if not(isinstance(int(line[4]),int) and int(line[4])<=int(agents["numb_agents"])):
                    return False
                if not bool(int(model["preventative_on"])):
                    return False
                preventative_included=True
            else:
                return False

        #Checking if all locations are within the bounds of the model
        elif line[0]=="Rail":
            if model_info_included:
                #Check if within bounds
                id=line[1]
                coords=line[2].split(" ")
                if not(CheckDimensions(coords[0],coords[1],model["width"],model["height"])):
                   # print("Dimensions")
                    return False
                # print(station_coord)
                station_connected = line[3].split(" ")
                stations[id] = station_connected
        elif line[0] == "House":
            if model_info_included:
                coords = line[2].split(" ")
                if not (CheckDimensions(coords[0], coords[1], model["width"], model["height"])):
                    return False
                housing_max_capacity+=int(line[3])
                #print(line[3])
                #Check if within bounds
        elif line[0] == "Workplace":
            if model_info_included:
                # Check if within bounds
                coords = line[2].split(" ")
                if not (CheckDimensions(coords[0], coords[1], model["width"], model["height"])):
                    return False
                workplaces_max_capacity += int(line[3])
                # Check if not over capacity
        elif line[0] == "School":
            if model_info_included:
                # Check if within bounds
                coords = line[2].split(" ")
                if not (CheckDimensions(coords[0], coords[1], model["width"], model["height"])):
                    return False
                school_max_capacity += int(line[3])
                # Check if not over capacity
        elif line[0] == "Entertain":
            if model_info_included:
                # Check if within bounds
                coords = line[2].split(" ")
                if not (CheckDimensions(coords[0], coords[1], model["width"], model["height"])):
                    return False
        elif line[0] == "Shop":
            if model_info_included:
                # Check if within bounds
                coords = line[2].split(" ")
                if not (CheckDimensions(coords[0], coords[1], model["width"], model["height"])):
                    return False
        #Ignore blank lines
        elif line[0]=="":
            pass
        #Comments start with #
        elif line[0][0]=="#":
            #print("Comment")
            pass
        else:
            return False



    #Check if all connected stations exist
    for k in stations.keys():
        for s in stations[k]:
            if not(s in stations.keys()):
                return False
    # Check if not under-capacity
    #If all conditions met accept, else reject
    return agents_info_included and model_info_included and CheckCapacity(agents["numb_agents"],1,housing_max_capacity) and CheckCapacity(agents["numb_agents"],agents["prop_student"],school_max_capacity) \
           and  CheckCapacity(agents["numb_agents"],agents["prop_worker"],workplaces_max_capacity) \
           and ((preventative_included and int(model["preventative_on"])) or (  not preventative_included and (not int(model["preventative_on"]))))



#This method checks if the given coordinates are within the bounds given
#Input: (w,h) the given coordinates, (width,height) the dimensions of the space
#Output: a boolean indicating if the given coordinates is within the bounds given
def CheckDimensions(w,h,width,height):
        print(w)
        print(w<width)
        print(height)
        if int(w)<int(width) and int(h)<int(height):
            print("True")
            return True
        else:
            return False
#This methods checks if the capacity proposed is enough for the population
#Input: proportion, population gives the population, capacity gives the proposed capacity
#Output: a boolean indicating if the given capacity is enough
def CheckCapacity(population,proportion,capacity):
        if int(capacity)>=int(population)*float(proportion):
            return True
        else:
            return False
