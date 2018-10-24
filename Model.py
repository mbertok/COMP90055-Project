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
import sys

import random



class Model(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height,expose,recover,rate,prop1=0.2,prop2=0.3,prop3=0.5,hubs={},homes=[(0,0)],schools=[(0,0)],workplaces=[(0,0)],home_max={},school_max={},work_max={},
                 entertain=[(0,0)],shops=[(0,0)],infect_agent_station=[],infect_agent_move=[],preventative_measures_active=False,stage_thresholds=[],vacc_rate=0.0
                 ,export_results=False,filename="log.csv"):
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.expose=expose*96
        self.recover=recover*96
        self.infection_rate=rate
        self.restricted=[]
        self.day=0
        self.hour=0
        self.quarter=0
        self.traindelayprob=0.0
        self.time=96#15 minute intervals
        self.preventative_measures_active=preventative_measures_active
        self.vaccination=False
        self.entertain_lockdown=False
        self.school_lockdown=False
        self.stage_thresholds=stage_thresholds
        self.preventative_stage=-1
        self.vacc_rate=vacc_rate



        #Create graph of grid
        self.graph=nx.Graph()
        #In this loop we create links between neighbours on a grid, while avoiding links to squares
        # that do not exist i.e exist outside of the bounds of our grid
        for i in range(width):
            for j in range(height):
                self.graph.add_node((i,j))
                #We do not want the grid to wrap around
                if i==0:# at an edge on the grid
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
        #self.summary=

        #Create hubs
        self.stations=hubs

        for h in self.stations.keys():
            co=[]
            for x in h:
                co.append(int(x))
            for r in self.stations[h]:
                #Adding transport link to graph
                self.graph.add_edge((co[0],co[1]),r,weight=2)
            self.grid.place_agent(StationaryAgent("Rail"), co)


        #create homes
        self.homes=homes
        self.home_current_capacity={}
        self.home_max_capacity={}
        for h in homes:
            self.grid.place_agent(StationaryAgent("Home"), h)
            self.home_current_capacity[h]=0
            self.home_max_capacity[h]=home_max[h]

        #create schools
        self.schools=schools
        self.school_current_capacity={}
        self.school_max_capacity={}

        for s in schools:
            self.grid.place_agent(StationaryAgent("School"), s)
            self.school_current_capacity[s]=0
            self.school_max_capacity[s]=school_max[s]
        #create workplaces
        self.workplaces=workplaces
        self.workplace_current_capacity={}
        self.workplace_max_capacity={}

        for w in workplaces:
            self.grid.place_agent(StationaryAgent("Workplace"), w)
            self.workplace_current_capacity[w]=0
            self.workplace_max_capacity[w]=work_max[w]
        # Create agents
        sum_prop=float(prop1+prop2+prop3)

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


        #Creating the agent population
        self.agentprop=[N*(prop1/sum_prop),N*(prop2/sum_prop),N*(prop3/sum_prop)]
        self.infection_count=int(random.uniform(0.05,0.1)*N)
        stage=1
        agent_id=0
        for p in self.agentprop:
            for i in range(int(p)):
                # Add the agent to a random grid cell
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                #Place everyone in their own homes
                if stage==1:
                    a = Worker(agent_id, self,self.expose,self.recover,self.infection_rate,x,y)
                elif stage==2:
                    a= Student(agent_id, self,self.expose,self.recover,self.infection_rate,x,y)
                elif stage==3:
                    a=Retiree(agent_id, self,self.expose,self.recover,self.infection_rate,x,y)
                a.x, a.y = a.places[0][1]
                self.schedule.add(a)
                self.grid.place_agent(a, (int(a.x), int(a.y)))
                agent_id+=1
                #print((agent_id/N))
                if (agent_id/N)%0.1==0:
                    print(str(agent_id)+" agents generated")#Progress message

            stage+=1

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
        else:
            # setup infected population
            for e in random.sample(self.schedule.agents, self.infection_count):
                e.infect()


        self.datacollector = DataCollector(
        {"Healthy": lambda m: self.count_state(m, 1),
         "Exposed": lambda m: self.count_state(m, 2),
         "Infected": lambda m: self.count_state(m, 3),
         "Recovered": lambda m: self.count_state(m, 4)

         })
        self.export_results=export_results
        if export_results:
            #Creating the file to export to
            self.output_file=open(filename,"w")
            #creating the header
            self.output_file.write("Step,Healthy,Exposed,Infected,Recovered \n")
            #Setting the file to close when model shut down
            atexit.register(self.close_file,self)
            #print("Export file created")
       # self.datacollector = DataCollector(
        #    model_reporters={"Gini": compute_gini},  # A function to call
         #   agent_reporters={"Wealth": "wealth"})  # An agent attribute

    #This function steps through a "tick" in the system
    #Input:None
    #Output: None
    def step(self):
        susceptible=[agent for agent in self.schedule.agents if ((not agent.vaccinated) and agent.stage==1) or agent.stage==4]
        infected=[agent for agent in self.schedule.agents if agent.stage==3 or agent.stage==2]
       # print((susceptible))
       # print(infected)
        if susceptible and infected:# If there are still agents to infect or infectees
                #print("Step")
            self.datacollector.collect(self)
            if self.export_results:#Writing to export file
                try:
                    self.output_file.write(
                    "{},{},{},{},{} \n".format(self.schedule.steps, self.count_state(self, 1), self.count_state(self, 2),
                                               self.count_state(self, 3), self.count_state(self, 4)))
                except ValueError:
                    sys.exit()
            #Updating the time
            self.quarter+=1
            if self.quarter>3:
                self.hour+=1
                self.quarter=0
            if self.hour>23:
                self.hour=0
                self.day+=1

            if self.preventative_measures_active:#Implementing preventative measures
                if self.preventative_stage<len(self.stage_thresholds)-1:
                    #check proportion
                    if float(self.count_state(self, 3) / self.num_agents)>float(self.stage_thresholds[self.preventative_stage + 1]):
                    #increment stage
                        self.preventative_stage+=1
                    if self.preventative_stage>=0:
                        try:
                            #Get random agents to vaccinate
                            agents=[agent for agent in self.schedule.agents if (not agent.vaccinated) and agent.stage==1 and agent.staying]
                            agents_to_vaccinate=random.sample(agents,int(self.vacc_rate))
                            for a in agents_to_vaccinate:
                                a.vaccinate()
                        except:
                            pass
                    if self.preventative_stage==1:
                        self.entertain_lockdown=True
                    if self.preventative_stage==2:
                        self.school_lockdown=True

            self.schedule.step()
       #def count(self):
         #   for
    @staticmethod
    #This function closes the file when the system closes
    #Input: model
    def close_file(model):
        model.output_file.close()
    @staticmethod
    #This function counts the number of agents in some state
    #Input: model, stage: the state the agent is in
    #Output: The number of agents in the given state in the model
    def count_state(model, stage):
        count = 0
        for person in model.schedule.agents:
            if person.stage == stage:
                count += 1
        return count


