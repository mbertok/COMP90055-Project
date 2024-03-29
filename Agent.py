from Model import Model
from mesa import Agent, Model
import random
import secrets
from Model import Model
import networkx as nx
from scipy.stats import truncnorm
import numpy



#Deprecated
def Get_closest(locs, dest):
    min=9999#hardcoded for now
    next=(0,0)
  #  print(locs)
    for loc in list(locs):
        if Manhattan_distance(loc, dest)<min:
            min=Manhattan_distance(loc, dest)
            next=loc
    return (int(next[0]),int(next[1]))
#Deprecated
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

    def __init__(self, unique_id, model,exposed_length,recovery_time,rate,x,y):
        super().__init__(unique_id, model)
        #if initial_infection:
         #   infected = random.choice([True, False])
       # else:
        infected=False
        self.destination=(self.model.grid.width-1,self.model.grid.height-1)
        if infected:
            self.stage=2
        else:
            self.stage=1
        exposed_length=exposed_length/96
        #print("Exposed:"+str(exposed_length))
        exposure_dist=truncnorm( a=(1 - exposed_length) / 1, b=(10 - exposed_length) / 1,loc=exposed_length,scale=1)
        self.exposure_threshold=int(exposure_dist.rvs(1)[0]*96)
        #print("Exposure:"+str(self.exposure_threshold))
        self.expose=0
        self.infected_length=0
        recovery_time=recovery_time/96
        recover_dist = truncnorm(a=(1 - recovery_time) / 1, b=(10 - recovery_time) / 1, loc=recovery_time, scale=1)
        self.recover_period = int(recover_dist.rvs(1)[0]*96)
        #print("Recover:"+str(self.recover_period))
        self.infect_prob=rate
        self.x=x
        self.y=y
        self.stay_time=0
        self.stage_behaviour=0
        self.step_stage=0
        self.path={}
        self.places={}
        self.stay_times={}
        self.leavetimes={}
        #rename later
        self.stay_time=0
        self.staying=False
        self.current_day=self.model.day
        self.vaccinated=False
        #self.times=[1,2,3]
        #self.places=[(9,9),(2,3),(5,5)]
        #Needs to scale with grid
        self.walk_threshold=self.model.grid.width/4


    def check_routine(self):
        #If time for move
        #print(type(self))
        hour = self.model.hour
        #day=self.model.day%7
        #print("Hour:" + str(hour))
        #print("Day:" + str(self.current_day))
        #print(self.leavetimes)
        # Check schedule
        #If not staying
        if not(self.staying):
                if self.leavetimes[self.current_day][self.stage_behaviour] <= hour or (self.step_stage!=0):
              #      print("L1:" + str(self.leavetimes[self.stage_behaviour]))
               #     print("Dest:" + str(self.path[self.current_day][self.stage_behaviour]))
               #     print(self.stage_behaviour)
               #     print(self.step_stage)
               #     print(self.unique_id)
                    #If weekend
                    if self.current_day>4:
                        if not self.model.entertain_lockdown:
                            self.move(list(self.path[self.current_day][self.stage_behaviour][self.step_stage]))
                    else:
                        #Agent is student going to school
                        if self.current_day<5 and type(self) is Student:
                            if not self.model.school_lockdown:
                                self.move(list(self.path[self.current_day][self.stage_behaviour][self.step_stage]))
                        else:
                            self.move(list(self.path[self.current_day][self.stage_behaviour][self.step_stage]))
                    self.step_stage+=1
                    if self.step_stage>=len(self.path[self.current_day][self.stage_behaviour]):
                        self.step_stage=0
                        self.stage_behaviour+=1
                        self.staying = True
                        if self.stage_behaviour>=len(self.places[self.current_day]):
                            self.stage_behaviour=0
                            self.current_day+=1
                            self.current_day=self.current_day%7
                           # print("Reset"+str(self.stage_behaviour))
        #If staying
        else:
          #  print("Staying")
           # print(self.stay_times[self.current_day][self.stage_behaviour])
            #print(self.stay_time)
            #If exceded stay_time+exceded leave time


            if self.stay_time>self.stay_times[self.current_day][self.stage_behaviour]:
                self.staying=False
                self.stay_time=0
                #print("Leaving:")

                #Not staying
                #reset stay_time
            else:
                self.stay_time+=1
                #increment stay_time

    # Deprecated
    def check_routine_1(self):
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
    #Moves the agent to the specified destination
    #Input: The destination to move to
    def move(self,dest):
        #print("To:"+str(dest))
        self.model.grid.move_agent(self,(int(dest[0]),int(dest[1])))
        self.x,self.y=dest

    # Deprecated
    def move_1(self,dest):
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

    # Deprecated
    def infect_1(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            for c in cellmates:
                print("Type:"+str(type(c)))
                if issubclass(type(c),Person):
                    print("Person!")
                    if c.stage==1:
                        chance = random.random()
                        print("Chance:" + str(chance))
                        if chance <= self.infect_prob:
                            c.stage = 2
                            c.expose=0
                            print("Infected!")
    #Infects an agent with the disease
    def infect(self):
        self.stage=2

    #This functions simulates the interactions an agent has with it's cellmates
    def interact(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        cellmates=list(filter(lambda c: issubclass(type(c),Person), cellmates))
        #remove stationary agents
        for c in cellmates:
            if not issubclass(type(c),Person):
         #       print(type(c))
                cellmates.remove(c)
        numb_interactions=random.randrange(0,len(cellmates))
#        if numb_interactions
        for i in range(numb_interactions):
            a=random.choice(cellmates)
            if self.stage==1 and not(self.vaccinated):
                #If interacting with infected agent
                if a.stage==3 :
                    chance = numpy.random.random_sample()

                    if float(chance) <= self.model.infection_rate:
                        self.stage = 2
                        self.expose = 0
                        #print("Infected!")
            elif self.stage==3:
                #If interacting with healthy agent
                if a.stage==1 and not(a.vaccinated):
                    chance = numpy.random.random_sample()

                    if float(chance) <= self.model.infection_rate:
                        a.stage = 2
                        a.expose = 0
                        #print("Infected!")







    #This function steps an agent through it's daily routine
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

        else:
            pass
        #print("Type:"+str(type(self)))
        self.check_routine()
        #if self.stage==3 :
        self.interact()
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

    def GenerateDailySchedule(self):
        pass
    def GenerateWeeklySchedule(self):
        #self.schedule=[]
        #self.leavetimes=[]
        # probability to shop
        prob_shop = 0.5  # base
        self.path={}
        #Weekdays
        #print("Weekdays")
        self.weekday=self.GenerateDailySchedule()
       # print("Weekdays1")
        for i in range(5):
            #self.path.append([])
            self.places[i]=(self.weekday)
            self.leavetimes[i]=(self.GenerateLeaveTimesWeekDay())
          #  print("New leavetimes:"+str(self.leavetimes))
            self.Create_paths(i)
            self.stay_times[i]=self.GenerateStayTimesWeek()
            #self.path[i]=[]
            #self.path[i].append()


     #   print("Weekends")
        #weekends
        for j in range(2):
            #If going out all day
#            self.path.append([])
            times=[random.randrange(6,11),random.randrange(14,17)]


            #If going out in afternoon
            times=[random.randrange(14,17)]

            #If going out in morning
            times=[random.randrange(6,11)]

            #self.leavetimes[j+5]=(times)
            places=[]
            for t in times:
                if random.uniform(0,1) < prob_shop:
                    places.append(self.setLocation(self.model.shops,self.model.shop_current_capacity,
                                    self.model.shop_max_capacity))
                else:
                    places.append(self.setLocation(self.model.entertain, self.model.entertain_current_capacity,
                                                   self.model.entertain_max_capacity))
            places.append(self.weekday[1])#Home of agent
            self.places[j+5]=(places)
            self.leavetimes[j+5]=self.GenerateLeaveTimesWeekEnd(len(places))
            self.stay_times[j+5]=self.GenerateStayTimesWeekEnd(j)
            self.Create_paths(j+5)
       # self.path
    def GenerateDailyTimes(self):
        pass
    def GenerateLeaveTimesWeekDay(self):
        pass
    def GenerateLeaveTimesWeekEnd(self,i):
        pass
    def GenerateStayTimesWeek(self):
        pass

 #   def GenerateLeisurePlaces(self):

    #Creates the paths an agent needs to
    def Create_paths(self,day):
        #self.path[day]=[]
      #  print(self.places[day])
        to_add=[]
        for p in range(len(self.places[day])):
            if p>0:
                to_add.append(nx.shortest_path(self.model.graph,source=(self.places[day][p-1]),target=self.places[day][p],weight="weight"))
            else:

                if day==0:
                    if len(self.places[day])>1:
                        to_add.append(nx.shortest_path(self.model.graph,source=(self.places[day][p+1]),target=self.places[day][p],weight="weight"))#Starting location
                    else:
                        to_add.append(nx.shortest_path(self.model.graph,source=(self.places[day][p]),target=self.places[day][p],weight="weight"))#Starting location
                else:
                    to_add.append(nx.shortest_path(self.model.graph,source=(self.places[day-1][-1]),target=self.places[day][p],weight="weight"))
        self.path[day]=list(to_add)
        #print("Paths:"+str(self.path[day]))

    def GenerateLeaveTimesWeekEnd(self, i):
        times = [random.randrange(8, 10), random.randrange(13, 15), random.randrange(17, 22)]
        leavetimes = []
        if i <= len(times):
            for j in range(i):
                leavetimes.append(times[j])
            return leavetimes
        else:
            print("Error!")
    def GenerateStayTimesWeekEnd(self,i):
        stay_times=[]
        for j in range(len(self.leavetimes[i+5])):
            stay_times.append(random.randrange(5,7))
        return stay_times
    #Vaccinates an agent
    def vaccinate(self):
        self.vaccinated=True





class Worker(Person):
     def __init__(self, unique_id, model,exposed_length,recovery_time,rate,x,y):
         super().__init__( unique_id, model,exposed_length,recovery_time,rate,x,y)

         self.GenerateWeeklySchedule()

         ##create path to follow for each destination
     def GenerateDailySchedule(self):
         home = self.setLocation(self.model.homes, self.model.home_current_capacity, self.model.home_max_capacity)
         workplace = self.setLocation(self.model.workplaces, self.model.workplace_current_capacity,
                                      self.model.workplace_max_capacity)
         return [workplace,home]

     def GenerateDailyTimes(self):
         return [random.randrange(7,9),random.randrange(15,17)]

     def GenerateLeaveTimesWeekDay(self):
         return [random.randrange(7,9),random.randrange(17,21)]

     def GenerateStayTimesWeek(self):
         return [random.randrange(7,9),random.randrange(6,10)]





class Student(Person):
    def __init__(self, unique_id, model, exposed_length, recovery_time, rate, x, y):
        super().__init__(unique_id, model, exposed_length, recovery_time, rate, x, y)
        self.GenerateWeeklySchedule()


    def GenerateDailySchedule(self):
        home = self.setLocation(self.model.homes, self.model.home_current_capacity, self.model.home_max_capacity)
        school = self.setLocation(self.model.schools, self.model.school_current_capacity,
                                  self.model.school_max_capacity)
        return [school,home]

    def GenerateDailyTimes(self):
        return [random.randrange(6, 9), random.randrange(15, 17)]

    def GenerateLeaveTimesWeekDay(self):
        return [random.randrange(6, 8), random.randrange(14, 15)]
    def GenerateStayTimesWeek(self):
        return [random.randrange(7, 9), random.randrange(6, 7)]



class Retiree(Person):
    def __init__(self, unique_id, model, exposed_length, recovery_time, rate, x, y):
        super().__init__(unique_id, model, exposed_length, recovery_time, rate, x, y)

        self.GenerateWeeklySchedule()

    def GenerateDailySchedule(self):
        home = self.setLocation(self.model.homes, self.model.home_current_capacity, self.model.home_max_capacity)
        return [home,home]
    def GenerateLeaveTimesWeekDay(self):
        return [random.randrange(1, 8), random.randrange(3, 10)]
    def GenerateStayTimesWeek(self):
        return [random.randrange(18, 21), random.randrange(18, 21)]

    def GenerateDailyTimes(self):
        return [0]
#Not being used
class Infection_Spreader_Moving(Agent):

    def __init__(self,unique_id,model,infect_prob):
        super().__init__(unique_id,model)
        self.infect_prob=infect_prob

    def step(self):
        self.move()#need to see if random
        self.infect()
    def infect(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for c in cellmates:
                if type(c) is Person:
                    if c.stage == 1:
                        chance=random.random()
                        print("Chance:"+str(chance))
                        if chance <= self.infect_prob:
                            c.stage = 2
                            c.expose = 0

#Not being used
class Infection_Spreader_Stationary(Agent):

    def __init__(self,unique_id,model,infect_prob):
        super().__init__(unique_id,model)
        self.infect_prob=infect_prob
    def step(self):
        self.infect()
    def infect(self):
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for c in cellmates:
                if not issubclass(c, Person):
                    cellmates.remove(c)
            numb_interactions = random.randrange(0, len(cellmates))
            #        if numb_interactions
            for i in range(numb_interactions):
                a = random.choice(cellmates)
                if random.random() <= self.model.infect_rate:#Include some sort of scaling by numer of cellmates
                    a.stage = 2
                    a.expose = 0
