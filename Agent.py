from Model import Model
from mesa import Agent, Model
import random
import secrets
from Model import Model



def Get_closest(locs, dest):
    min=9999#hardcoded for now
    next=(0,0)
  #  print(locs)
    for loc in list(locs):
        if Manhattan_distance(loc, dest)<min:
            min=Manhattan_distance(loc, dest)
            next=loc
    return (int(next[0]),int(next[1]))
def Manhattan_distance(x, y):
  #  print(x)
   # print(y)
    #print(str(list(zip(x,y))))
    return sum(abs(int(a) - int(b)) for a, b in zip(x, y))

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
        #Check time
        print(type(self))
        hour=self.model.hour
        print("Hour:"+str(hour))
        print(self.leavetime)
        #Check schedule
        for i in range(len(self.leavetime)-1,-1,-1):
            print("L:" + str(self.leavetime[i]))
            print(i)
            if self.leavetime[i]<=hour:
                print("L1:" + str(self.leavetime[i]))
                print("Dest:"+str(self.destination))
                #Check location
                #If desination
                if((self.x,self.y)==self.destination):
                    #If time not exceeded,
                    if self.stay_time<self.times[self.stage_behaviour]:
                        # stay
                        self.stay_time+=1
                        return
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
                    distance=Manhattan_distance((self.x, self.y), self.destination)
                    if distance>self.walk_threshold:
                        print("Going to Hub")
                        print("Distance:"+str(distance))
                        #List of transport hubs
                        locs=list(self.model.stations.keys())
                        #If not at transport hub
                        if (str(self.x),str(self.y)) not in locs:
                            #Get nearest transport hub
                            print("Not at hub")
                            print("Current_loc:"+str(self.x)+","+str(self.y))
                            next=Get_closest(locs, (self.x, self.y))
                            if Manhattan_distance(next,(self.x,self.y))>distance:
                                self.move(self.destination)
                                return
                            #move towards there
                            self.move(next)
                        else:
                            print("At hub")
                            #if train delayed
                            if random.uniform(0,1)<self.model.traindelayprob:
                                print("Delayed")
                                return
                            else:
                                stops=self.model.stations[(str(self.x),str(self.y))]
                                print("Stops:"+str(stops))
                                # find nearest stop to transport hub
                                # move to there
                                next=Get_closest(stops, self.destination)
                                self.model.grid.move_agent(self, next)
                                self.x, self.y = next

                    else:
                        self.move(self.destination)
            else:
                print("Not yet")
                pass



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
            if(Manhattan_distance(j, dest))<min:
                min=Manhattan_distance(j, dest)
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
        print("Type:"+str(type(self)))
        self.check_routine()
        if self.stage==3 :
            self.infect()
    def setLocation(self,list,curr_capacity_dict,max_capacity_dict):
        selected=False
       # print("List="+str(list))
        #print("Curr:"+str(curr_capacity_dict.keys()))
        #print("Max:"+str(max_capacity_dict.keys()))

        while(not selected):
            loc=secrets.choice(list)
         #   print("Selected: "+str(loc))
            if int(curr_capacity_dict[loc])<int(max_capacity_dict[loc]):
                selected=True
                curr_capacity_dict[loc]+=1
          #      print("Added capacity:"+str(curr_capacity_dict[loc]))
           #     print("Max capacity:"+str(max_capacity_dict[loc]))

        return loc


class Worker(Person):
     def __init__(self, unique_id, model,exposed_length,recovery_time,rate,x,y):
         super().__init__( unique_id, model,exposed_length,recovery_time,rate,x,y)
         self.times = [random.randrange(7,9), random.randrange(7,10)]
         self.leavetime=[random.randrange(7,9),random.randrange(15,17)]
         home=self.setLocation(self.model.homes,self.model.home_current_capacity,self.model.home_max_capacity)
         workplace=self.setLocation(self.model.workplaces,self.model.workplace_current_capacity,
                                    self.model.workplace_max_capacity)

         self.places=[home,workplace]


class Student(Person):
    def __init__(self, unique_id, model, exposed_length, recovery_time, rate, x, y):
        super().__init__(unique_id, model, exposed_length, recovery_time, rate, x, y)
        self.times = [random.randrange(8,9), random.randrange(5,7)]
        self.leavetime = [random.randrange(6,9),random.randrange(15,17)]
        home = self.setLocation(self.model.homes, self.model.home_current_capacity, self.model.home_max_capacity)
        school = self.setLocation(self.model.schools, self.model.school_current_capacity,
                                     self.model.school_max_capacity)

        self.places = [home,school]


class Retiree(Person):
    def __init__(self, unique_id, model, exposed_length, recovery_time, rate, x, y):
        super().__init__(unique_id, model, exposed_length, recovery_time, rate, x, y)
        self.leavetime=[0]
        self.times = [5]
        home = self.setLocation(self.model.homes, self.model.home_current_capacity, self.model.home_max_capacity)
        self.places = [ home]
