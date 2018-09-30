from Model import Model,Person,StationaryAgent
import numpy as np
import matplotlib.pyplot as plt
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

Colors = {"Healthy": "#66cd00", "Exposed": "#ffd700", "Infected": "#b22222", "Recovered": "#9932cc"}

def create_server(numb_agents,width,height,expose,recover,rate,prop_worker,prop_student,prop_retire,hubs,homes,schools,workplaces,
                  home_capacity,school_capacity,work_capacity):
    #Colors={"Healthy":"#66cd00","Exposed":"#ffd700","Infected":"#b22222","Recovered":"#9932cc"}
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
    chart_element = ChartModule([{"Label": label, "Color": color} for (label, color) in Colors.items()])

    server = ModularServer(Model,
                           [grid, chart_element],
                          # [grid],
                           "Disease Model",
                           {"N": numb_agents,
                                    "width": width,
                                    "height": height,
                                    "expose": expose ,
                                    "recover" :recover,
                                    "rate" :rate,
                                    "prop1": prop_worker,
                                    "prop2": prop_student,
                                    "prop3": prop_retire,
                                    "hubs":hubs,
                                    "homes": homes,
                                    "schools": schools,
                                    "workplaces": workplaces,
                                    "home_max": home_capacity,
                                    "school_max": school_capacity,
                                    "work_max": work_capacity,
                                    "blocked_cells": []



    })
    return server

def agent_portrayal(agent):
    if issubclass(type(agent), Person):
        portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 2,
                         "Color": "red",
                        #"x": 0,
                        #"y": 2,
                         #"stroke_color": "#666666",
                         #"Filled": "true",
                         #"heading_x": 1,
                         #"heading_y": 0,
                         #"text": agent.unique_id,
                         #"text_color": "white",
                         "r": 0.5,
                     }
        if agent.stage==1:
            portrayal["Color"] = Colors["Healthy"]
            portrayal["Layer"] = 1
            portrayal["r"] = 0.6
        elif agent.stage==2:
            portrayal["Color"] = Colors["Exposed"]
            portrayal["Layer"] = 2
            portrayal["r"] = 0.1
        elif agent.stage==3:
            portrayal["Color"] = Colors["Infected"]
            portrayal["Layer"] = 3
            portrayal["r"] = 0.4
        elif agent.stage==4:
            portrayal["Color"] = Colors["Recovered"]
            portrayal["Layer"] = 4
            portrayal["r"] = 0.3
        else:
           pass
    elif type(agent) is StationaryAgent:
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 9,
                     "Color": "red",
                     "w": 1,
                     "h":1,
                     # "x": 0,
                     # "y": 2,
                     # "stroke_color": "#666666",
                     # "Filled": "true",
                     # "heading_x": 1,
                     # "heading_y": 0,
                     # "text": agent.unique_id,
                     # "text_color": "white",
         #            "r": 0.5,
                     }
        if agent.type is "Rail":
                portrayal["Color"]="green"
                portrayal["Shape"] = "train.png"
        elif agent.type is "Home":
            portrayal["Color"] = "blue"
            portrayal["Shape"]="home.png"
        elif agent.type is "Workplace":
            portrayal["Color"] = "purple"
            portrayal["Shape"]="office.png"
        elif agent.type is "School":
            portrayal["Color"] = "cyan"
            portrayal["Shape"]="school.png"
        #elif agent.type is "Venue":
        #elif agent.type is "Shop":


    else:
        portrayal={}
    return portrayal
