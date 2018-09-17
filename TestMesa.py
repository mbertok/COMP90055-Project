# model.py
from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
import matplotlib.pyplot as plt
import  random
import math
import secrets

import random

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)
def get_closest(locs,dest):
    min=9999#hardcoded for now
    next=(0,0)
    print(locs)
    for loc in list(locs):
        if manhattan_distance(loc,dest)<min:
            min=manhattan_distance(loc,dest)
            next=loc
    return next
def manhattan_distance(x, y):
    print(x)
    print(y)
    print(str(list(zip(x,y))))
    return sum(abs(int(a) - int(b)) for a, b in zip(x, y))
class Model(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height,expose,recover,rate,prop1=0.2,prop2=0.3,prop3=0.5,hubs={},homes=[(0,0)],schools=[(0,0)],workplaces=[(0,0)],home_max={},school_max={},work_max={},blocked_cells=[]):
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
        print(str(width)+":"+str(height))
        print(prop1)
        self.schedule = RandomActivation(self)
        self.running = True
        self.expose=expose
        self.recover=recover
        self.infection_rate=rate
        self.restricted=[]
        self.day=0
        self.hour=0
        self.quarter=0
        self.time=96#15 minute intervals
        for i in range(len(blocked_cells)):
            self.restricted.append((blocked_cells[0],blocked_cells[1]))
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
            print(self.stations[h])
            co=[]
            for x in h:
                co.append(int(x))
            print(co)
            self.grid.place_agent(StationaryAgent("Rail"), co)

        #create homes
        self.homes=homes
        self.home_current_capacity={}
       # self.home_max_capacity=home_max
        self.home_max_capacity={}
        for h in home_max.keys():
            print("KeyH:"+str(h))
        for h in homes:
            print("Home:"+str(h))
            self.grid.place_agent(StationaryAgent("Home"), h)
            self.home_current_capacity[h]=0
            self.home_max_capacity[h]=home_max[h]
        #create schools
        self.schools=schools
        self.school_current_capacity={}
        #self.school_max_capacity=school_max
        self.school_max_capacity={}

        for s in schools:
            print("School:"+str(s))
            self.grid.place_agent(StationaryAgent("School"), s)
            self.school_current_capacity[s]=0
            self.school_max_capacity[s]=school_max[s]
        #create workplaces
        self.workplaces=workplaces
        self.workplace_current_capacity={}
        #self.workplace_max_capacity=work_max
        self.workplace_max_capacity={}

        for w in workplaces:
            print("Workplace:"+str(w))
            self.grid.place_agent(StationaryAgent("Workplace"), w)
            self.workplace_current_capacity[w]=0
            self.workplace_max_capacity[w]=work_max[w]
        # Create agents
        sum_prop=float(prop1+prop2+prop3)
        print(sum_prop)
        self.agentprop=[(N*prop1)/sum_prop,(N*prop2)/sum_prop,(N*prop3)/sum_prop]
        stage=0
        for p in self.agentprop:
            for i in range(int(p)):
                # Add the agent to a random grid cell
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                #Place everyone in their own home
                if stage==0:
                    a = Worker(i, self,expose,recover,self.infection_rate,x,y)
                elif stage==1:
                    a= Student(i, self,expose,recover,self.infection_rate,x,y)
                elif stage==2:
                    a=Retiree(i, self,expose,recover,self.infection_rate,x,y)
                a.x, a.y = a.places[0]
                print("Loc:"+str(a.x)+":"+str(a.y))
                self.schedule.add(a)
                self.grid.place_agent(a, (int(a.x), int(a.y)))
            stage+=1
        print("Created agents")

        #Change later
        self.datacollector = DataCollector(
        {"Healthy": lambda m: self.count_type(m,1),
         "Exposed": lambda m: self.count_type(m, 2),
         "Infected": lambda m: self.count_type(m, 3),
         "Recovered": lambda m: self.count_type(m, 4)

         })
        print("Finished!")
       # self.datacollector = DataCollector(
        #    model_reporters={"Gini": compute_gini},  # A function to call
         #   agent_reporters={"Wealth": "wealth"})  # An agent attribute

    def step(self):
        print("Step")
        self.datacollector.collect(self)
        self.quarter+=1
        if self.quarter>3:
            self.hour+=1
            self.quarter=0
        if self.hour>23:
            self.hour=0
            self.day+=1

        self.schedule.step()
    #def count(self):
     #   for
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
class StationaryAgent(Agent):
    def __init__(self,type):
        self.type=type
    def step(self):
        pass
#class StationaryAgent(Agent):

class Person(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model,exposed_length,recovery_time,rate,x,y):
        super().__init__(unique_id, model)
        infected = random.choice([True, False])
        self.destination=(self.model.grid.width-1,self.model.grid.height-1)
        if infected:
            self.stage=2
        else:
            self.stage=1
        self.exposure_threshold=exposed_length
        self.expose=0
        self.infected_length=0
        self.recover_period=recovery_time
        self.infect_prob=rate
        self.x=x
        self.y=y
        self.stay_time=0
        self.stage_behaviour=0
        #rename later
        #self.times=[1,2,3]
        #self.places=[(9,9),(2,3),(5,5)]
        #Needs to scale with grid
        self.walk_threshold=self.model.grid.width/4


    def check_routine(self):
        #Check location
        #If desination
        if((self.x,self.y)==self.destination):
            #If time not exceeded,
            if self.stay_time<self.times[self.stage_behaviour]:
                # stay
                self.stay_time+=1
            else:
                # reset stay_time
                self.stay_time=0
                #update destination
                self.stage_behaviour+=1
                if self.stage_behaviour>=len(self.places):
                    self.stage_behaviour=0
                self.destination=self.places[self.stage_behaviour]
                self.move
        #if not at destination
        else:
            #Check distance to destination
            distance=manhattan_distance((self.x,self.y),self.destination)
            if distance>self.walk_threshold:
                print("Going to Hub")
                #List of transport hubs
                locs=list(self.model.stations.keys())
                #If not at transport hub
                if (self.x,self.y) not in locs:
                    #Get nearest transport hub
                    next=get_closest(locs,(self.x,self.y))
                    #move towards there
                    self.move(next)
                else:
                    stops=self.model.stations[(self.x,self.y)]
                    # find nearest stop to transport hub
                    # move to there
                    next=get_closest(stops,self.destination)
                    self.model.grid.move_agent(self, next)
                    self.x, self.y = next

            else:
                self.move(self.destination)



    def move(self,dest):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        for i in range(len(possible_steps)):
            if possible_steps[i] in self.model.restricted:
                del possible_steps[i]
        #possible_steps=set(possible_steps).difference(self.model.restricted)
        min=9999
        next_step=(0,0)
        #print("Curr:"+str(self.x)+","+str(self.y))
        #print("to:"+str(dest))
        for j in possible_steps:
           # print("Testing")
           # print(j)
            if(manhattan_distance(j,dest))<min:
                min=manhattan_distance(j,dest)
                next_step=j
            #    print("New min="+str(min)+" at:"+str(next_step))

        #print("\n New loc:")
        #print(str(self.x)+":"+str(self.y)+"\n")
        #new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, next_step)
        self.x,self.y=next_step

    def infect(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            for c in cellmates:
                if type(c) is Person:
                    if c.stage==1:
                        if random.random()<=self.infect_prob:
                            c.stage = 2
                            c.expose=0



    def step(self):
        if self.stage==2:
            self.expose+=1
            if self.expose>=self.exposure_threshold:
                self.stage=3
                self.expose=0
        elif self.stage==3:
            self.infected_length+=1
            if self.infected_length>=self.recover_period:
                self.stage=4
                self.infected_length=0
                print("Recovered!"+str(self.unique_id))

        else:
            pass
        self.check_routine()
        if self.stage==3 :
            self.infect()
    def setLocation(self,list,curr_capacity_dict,max_capacity_dict):
        selected=False
        print("List="+str(list))
        print("Curr:"+str(curr_capacity_dict.keys()))
        print("Max:"+str(max_capacity_dict.keys()))

        while(not selected):
            loc=secrets.choice(list)
            print("Selected: "+str(loc))
            if int(curr_capacity_dict[loc])<int(max_capacity_dict[loc]):
                selected=True
                curr_capacity_dict[loc]+=1
                print("Added capacity:"+str(curr_capacity_dict[loc]))
                print("Max capacity:"+str(max_capacity_dict[loc]))

        return loc


class Worker(Person):
     def __init__(self, unique_id, model,exposed_length,recovery_time,rate,x,y):
         super().__init__( unique_id, model,exposed_length,recovery_time,rate,x,y)
         self.times = [random.randrange(7,9), random.randrange(7,10)]
         self.leavetime=[]
         home=self.setLocation(self.model.homes,self.model.home_current_capacity,self.model.home_max_capacity)
         workplace=self.setLocation(self.model.workplaces,self.model.workplace_current_capacity,self.model.workplace_max_capacity)

         self.places=[home,workplace]


class Student(Person):
    def __init__(self, unique_id, model, exposed_length, recovery_time, rate, x, y):
        super().__init__(unique_id, model, exposed_length, recovery_time, rate, x, y)
        self.times = [random.randrange(8,9), random.randrange(5,7)]
        self.leavetime = []
        home = self.setLocation(self.model.homes, self.model.home_current_capacity, self.model.home_max_capacity)
        school = self.setLocation(self.model.schools, self.model.school_current_capacity,
                                     self.model.school_max_capacity)
        self.places = [home,school]


class Retiree(Person):
    def __init__(self, unique_id, model, exposed_length, recovery_time, rate, x, y):
        super().__init__(unique_id, model, exposed_length, recovery_time, rate, x, y)
        self.times = [5]
        home = self.setLocation(self.model.homes, self.model.home_current_capacity, self.model.home_max_capacity)
        self.places = [ home]
