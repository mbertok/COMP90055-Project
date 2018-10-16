# model.py
from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation,BaseScheduler
from mesa.datacollection import DataCollector
from Agent import *
import numpy as np
import matplotlib.pyplot as plt
import  random
import math
import secrets
import atexit
import networkx as nx

import random

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)

class Model(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height,expose,recover,rate,prop1=0.2,prop2=0.3,prop3=0.5,hubs={},homes=[(0,0)],schools=[(0,0)],workplaces=[(0,0)],home_max={},school_max={},work_max={},
                 entertain=[(0,0)],shops=[(0,0)],infect_agent_station=[],infect_agent_move=[],preventative_measures_active=False,stage_thresholds=[],vacc_rate=0.0):
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
     #   print(str(width)+":"+str(height))
     #   print(prop1)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.expose=expose*96
        self.recover=recover*96
        self.infection_rate=rate
        self.restricted=[]
        self.day=0
        self.hour=0
        self.quarter=0
        self.traindelayprob=0.0#Change from hardcode later
        self.time=96#15 minute intervals
        self.preventative_measures_active=preventative_measures_active
        self.vaccination=False
        self.entertain_lockdown=False
        self.school_lockdown=False
        self.stage_thresholds=stage_thresholds
        self.preventative_stage=-1
        self.vacc_rate=vacc_rate


       # for i in range(len(blocked_cells)):
       #     self.restricted.append((blocked_cells[0],blocked_cells[1]))
        #Create graph of grid
        self.graph=nx.Graph()
        for i in range(width):
            for j in range(height):
                self.graph.add_node((i,j))
              #  print(str(i)+":"+str(j))
                if i==0:
                    if j==0:
                        self.graph.add_edge((i, j), (i + 1, j), weight=5)
                        self.graph.add_edge((i, j), (i, j + 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j + 1), weight=5)
                    elif j==height-1:
                        self.graph.add_edge((i, j), (i, j - 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j - 1), weight=5)
                    else:
                        self.graph.add_edge((i, j), (i, j - 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j), weight=5)
                        self.graph.add_edge((i, j), (i, j + 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j - 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j + 1), weight=5)
                elif i==width-1:
                    if j==0:
                        self.graph.add_edge((i, j), (i - 1, j), weight=5)
                        self.graph.add_edge((i, j), (i, j + 1), weight=5)
                        self.graph.add_edge((i, j), (i - 1, j + 1), weight=5)
                    elif j==height-1:
                        self.graph.add_edge((i, j), (i - 1, j), weight=5)
                        self.graph.add_edge((i, j), (i, j - 1), weight=5)
                        self.graph.add_edge((i, j), (i - 1, j - 1), weight=5)
                    else:
                        self.graph.add_edge((i, j), (i - 1, j), weight=5)
                        self.graph.add_edge((i, j), (i, j - 1), weight=5)
                        self.graph.add_edge((i, j), (i, j + 1), weight=5)
                        self.graph.add_edge((i, j), (i - 1, j + 1), weight=5)
                        self.graph.add_edge((i, j), (i - 1, j - 1), weight=5)
                else:
                    if j==0:
                        self.graph.add_edge((i, j), (i - 1, j), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j), weight=5)
                        self.graph.add_edge((i, j), (i, j + 1), weight=5)
                        self.graph.add_edge((i, j), (i - 1, j + 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j + 1), weight=5)
                    elif j==height-1:
                        self.graph.add_edge((i, j), (i - 1, j), weight=5)
                        self.graph.add_edge((i, j), (i, j - 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j), weight=5)
                        self.graph.add_edge((i, j), (i - 1, j - 1), weight=5)
                        self.graph.add_edge((i, j), (i + 1, j - 1), weight=5)
                    else:
                        self.graph.add_edge((i,j),(i-1,j),weight=5)
                        self.graph.add_edge((i,j),(i,j-1),weight=5)
                        self.graph.add_edge((i,j),(i+1,j),weight=5)
                        self.graph.add_edge((i,j),(i,j+1),weight=5)
                        self.graph.add_edge((i,j),(i-1,j+1),weight=5)
                        self.graph.add_edge((i,j),(i-1,j-1),weight=5)
                        self.graph.add_edge((i,j),(i+1,j-1),weight=5)
                        self.graph.add_edge((i,j),(i+1,j+1),weight=5)
       #     print(self.graph.edges)
      #  print(self.graph.nodes)

          #      self.graph.add_edge()
        #Add neighbours

        #Add transport links


        #self.summary=
        #Create hubs
        self.stations=hubs
       # for hub in hubs:
        #    for h in range(len(hub)):
       #         if h == len(hub) - 1:
        #            self.stations[hub[h]] = [hub[h - 1]]
         #       elif h>0:
          #         self.stations[hub[h]]=[hub[h-1],hub[h+1]]
           #     elif h==0:
            #        self.stations[hub[h]]=[hub[h+1]]
             #   else:
             #       pass
              #  print(hub[h])
        for h in self.stations.keys():
          #  print(h)
         #   print(self.stations[h])
            co=[]
            for x in h:
                co.append(int(x))
          #  print(co)
            for r in self.stations[h]:
                self.graph.add_edge((co[0],co[1]),r,weight=2)
            self.grid.place_agent(StationaryAgent("Rail"), co)
        #print("Stations: "+str(self.stations.keys()))
        #create homes
        self.homes=homes
        self.home_current_capacity={}
       # self.home_max_capacity=home_max
        self.home_max_capacity={}
       # for h in home_max.keys():
         #   print("KeyH:"+str(h))
        for h in homes:
          #  print("Home:"+str(h))
            self.grid.place_agent(StationaryAgent("Home"), h)
            self.home_current_capacity[h]=0
            self.home_max_capacity[h]=home_max[h]
        #create schools
        self.schools=schools
        self.school_current_capacity={}
        #self.school_max_capacity=school_max
        self.school_max_capacity={}

        for s in schools:
          #  print("School:"+str(s))
            self.grid.place_agent(StationaryAgent("School"), s)
            self.school_current_capacity[s]=0
            self.school_max_capacity[s]=school_max[s]
        #create workplaces
        self.workplaces=workplaces
        self.workplace_current_capacity={}
        #self.workplace_max_capacity=work_max
        self.workplace_max_capacity={}

        for w in workplaces:
       #     print("Workplace:"+str(w))
            self.grid.place_agent(StationaryAgent("Workplace"), w)
            self.workplace_current_capacity[w]=0
            self.workplace_max_capacity[w]=work_max[w]
        # Create agents
        sum_prop=float(prop1+prop2+prop3)
        print(sum_prop)

        #Test code
        self.shops=shops
        self.shop_max_capacity={}
        self.shop_current_capacity = {}
        for s in self.shops:
            self.grid.place_agent(StationaryAgent("Shop"), s)
            self.shop_current_capacity[s] = 0
            self.shop_max_capacity[s] = self.num_agents*2 #Test value


        self.entertain=entertain
        self.entertain_max_capacity = {}
        self.entertain_current_capacity = {}
        for e in self.entertain:
            self.grid.place_agent(StationaryAgent("Entertain"),e)
            self.entertain_current_capacity[e] = 0
            self.entertain_max_capacity[e] = self.num_agents*2 #Test value


        if len(infect_agent_move)==0 and len(infect_agent_station)==0:
            self.initial_infected=True
        else:
            self.initial_infected=False

        self.agentprop=[N*(prop1/sum_prop),N*(prop2/sum_prop),N*(prop3/sum_prop)]
        stage=1
        agent_id=0
        for p in self.agentprop:
          #  print("P:"+str(p))
          #  print("stage:"+str(stage))
            for i in range(int(p)):
                # Add the agent to a random grid cell
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                #Place everyone in their own homes
                if stage==1:
                #    print("Worker")
                    a = Worker(agent_id, self,expose,recover,self.infection_rate,x,y,self.initial_infected)
                elif stage==2:
                  #  print("Student")
                    a= Student(agent_id, self,expose,recover,self.infection_rate,x,y,self.initial_infected)
                elif stage==3:
                   # print("Retire")
                    a=Retiree(agent_id, self,expose,recover,self.infection_rate,x,y,self.initial_infected)
                a.x, a.y = a.places[0][1]
                self.schedule.add(a)
                self.grid.place_agent(a, (int(a.x), int(a.y)))
               # print("Loc:"+str(a.x)+":"+str(a.y))
                agent_id+=1
            #if agent_id%100==0:
                print(str(agent_id)+" agents generated")

            stage+=1
       # print("Created agents")
        if not self.initial_infected:
            for s1,s2 in infect_agent_station:
                # Add the agent to a random grid cell
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                #create Agent
                #Add to scheduler
                agent_id+=1
            for m1,m2 in infect_agent_move:
                # Add the agent to a random grid cell
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                # create Agent
                # Add to scheduler
                agent_id+=1


        #Change later
        self.datacollector = DataCollector(
        {"Healthy": lambda m: self.count_type(m,1),
         "Exposed": lambda m: self.count_type(m, 2),
         "Infected": lambda m: self.count_type(m, 3),
         "Recovered": lambda m: self.count_type(m, 4)

         })
        print("Finished!")
        self.output_file=open("Log.csv","w")
        self.output_file.write("Step,Healthy,Exposed,Infected,Recovered \n")
        atexit.register(self.close_file,self)
       # self.datacollector = DataCollector(
        #    model_reporters={"Gini": compute_gini},  # A function to call
         #   agent_reporters={"Wealth": "wealth"})  # An agent attribute

    def step(self):
        #print("Step")
        self.datacollector.collect(self)
        self.quarter+=1
        if self.quarter>3:
            self.hour+=1
            self.quarter=0
        if self.hour>23:
            self.hour=0
            self.day+=1
        if self.preventative_measures_active:
            print(self.preventative_stage)
            if self.preventative_stage<len(self.stage_thresholds)-1:
                #check proportion
                if float(self.count_type(self,3)/self.num_agents)>float(self.stage_thresholds[self.preventative_stage+1]):
                #increment stage
                    self.preventative_stage+=1
                    if self.preventative_stage==1:
                        try:
                            #Get random agents to vaccinate
                            agents=[agent for agent in self.schedule.agents if (not agent.vaccinated) and agent.stage==1 and agent.staying]
                            agents_to_vaccinate=random.sample(agents,int(self.vacc_rate))
                            for a in agents_to_vaccinate:
                                a.vaccinate()
                        except:
                            pass
                    if self.preventative_stage==2:
                        self.entertain_lockdown=True
                    if self.preventative_stage==3:
                        self.school_lockdown=True


        self.schedule.step()
        self.output_file.write("{},{},{},{},{} \n".format(self.schedule.steps,self.count_type(self,1),self.count_type(self,2),self.count_type(self,3),self.count_type(self,4)))
    #def count(self):
     #   for
    @staticmethod
    def close_file(model):
        model.output_file.close()
    @staticmethod
    def count_type(model, stage):
        """
        Change later
        """
        count = 0
        for person in model.schedule.agents:
            if person.stage == stage:
                count += 1
        return count


