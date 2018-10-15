from Model import Model,Person,StationaryAgent
import numpy as np
import matplotlib.backends.backend_tkagg
from mesa.visualization.modules import CanvasGrid, ChartModule,TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
import os

package_dir = os.path.dirname(os.path.abspath(__file__))
#thefile = os.path.join(package_dir,'test.cvs')
Colors = {"Healthy": "#66cd00", "Exposed": "#ffd700", "Infected": "#b22222", "Recovered": "#9932cc"}
Places_To_Colors={"School":"#00FFFF","Workplaces":"#b2149d","Homes":"#1a15b2","Transport Hubs":"#14d114","Entertainment Centres":"#b27514","Shops":"#b21448"}
class Legend(TextElement):
    def render(self, model):
       # ratio = model.resistant_susceptible_ratio()
        #ratio_text = '&infin;' if ratio is math.inf else '{0:.2f}'.format(ratio)
        #infected_text = str(number_infected(model))
        out=["<div display: flex > Environment Legend  "]
        #out=["<table>"]
        places=list(Places_To_Colors.keys())
        color=list(Colors.keys())
        out.append("<div>")
        for p in places:
            out.append("<svg width=\"20\" height=\"20\" ><rect x=\"0\"   y=\"0\" width=\"30\" height=\"30\"  fill={} /></svg>:{} &nbsp;&nbsp;".format(str(Places_To_Colors[p]),str(p)))
        out.append("</div>")
        out.append("<div> Agent state:")
        for c in color:
            out.append("<span   style=\" white-space: nowrap; color:{};\"> {}</span> ".format(Colors[c], str(c)))
        out.append("</div>")
        out.append("<table id=\"data\"> ")

        for i in range(1, 5, 1):
            out.append("<tr><td>{}: </td><td>{}</td> </tr>".format(color[i-1],model.count_type(model,i)))
        out.append("</table> \n")
        out.append("<div class='button'> <a href=\"#\" id =\"export\" role='button'>Export</a> </div>")
     #   out.append(" <script type='text/javascript'>$(document).ready(function () {"/
      #            "function  exportDataToCSV($table, filename) {"/
        out.append("<script type=\'text/javascript\'>")
        out.append("$(document).ready(function () {")
        out.append("function exportResults($table, filename) {")
        out.append(""" var $headers=$table.find('tr:has(th)'))
                        var $rows=$table.find('tr:has(td)');
                        console.log("$rows")""")

        out.append(""" $("#export").click(function (event) {
                var outputFile = window.prompt("Save file || 'export';\
                outputFile = outputFile.replace('.csv','') + '.csv'\
                exportResults.apply(this, [$('#data>table'), outputFile]);\
            });/
        });/""")
        out.append("</script>")




           #for p in range(len(places)):
         #   out.append("<div style=\" margin-left:500px;\"><img src={} width=20 height=20><h6>:{}</h6></div>".format("local/"+str(Places_To_Icons[places[p]]),str(places[p])))
          #  out.append("<div style=\" margin-top:-10px; margin-bottom:-20px;\" ><h6 style=\"color:{};\">{}</h6></div> ".format(Colors[color[p]],str(color[p])))
        #out.append("<div style=\"margin-bottom:50px;\" float: left> :")
       # out.append("</div> <div>")
        #for c in Colors.keys():
         #      out.append(" <h4 style=\"color:{};\"> {}</h4> ".format(Colors[c],str(c)))

        out.append("</div>")
        return out


def create_server(numb_agents,width,height,expose,recover,rate,prop_worker,prop_student,prop_retire,hubs,homes,schools,workplaces,
                  home_capacity,school_capacity,work_capacity,entertain,shops,stationary_agents=[],moving_agents=[],preventative_toggle=False,stage_threshold=[0.2, 0.5, 0.7],
                  vacc_rate=0.5,port=0):
    #Colors={"Healthy":"#66cd00","Exposed":"#ffd700","Infected":"#b22222","Recovered":"#9932cc"}
    grid = CanvasGrid(agent_portrayal, width, height, 800, 500)
    chart_element = ChartModule([{"Label": label, "Color": color} for (label, color) in Colors.items()])

    server = ModularServer(Model,
                           [grid, Legend(),chart_element],
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
                                    "entertain":entertain,
                                    "shops":shops,
                                    "infect_agent_station":stationary_agents,
                                    "infect_agent_move":moving_agents,
                                    "preventative_measures_active": preventative_toggle,
                                    "stage_thresholds" : stage_threshold,
                                    "vacc_rate" : vacc_rate



    })
    server.port=port
    server.launch()
    #return server

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
                      #"heading_y": 0,
                     # "text": agent.unique_id,
                     # "text_color": "white",
         #            "r": 0.5,
                     }
        if agent.type is "Rail":
                portrayal["Color"]=Places_To_Colors["Transport Hubs"]
                portrayal["text"]="Trans"
               # portrayal["Shape"] = Places_To_Icons["Transport Hubs"]
        elif agent.type is "Home":
            portrayal["Color"] = Places_To_Colors["Homes"]
           # portrayal["text"]="Home"
           # portrayal["Shape"]=Places_To_Icons["Homes"]
        elif agent.type is "Workplace":
            portrayal["Color"] = Places_To_Colors["Workplaces"]
           # portrayal["Shape"]=Places_To_Icons["Workplaces"]
        elif agent.type is "School":
            portrayal["Color"] = Places_To_Colors["School"]
          #  portrayal["Shape"]=Places_To_Icons["School"]
        elif agent.type is "Entertain":
            portrayal["Color"] = Places_To_Colors["Entertainment Centres"]
        elif agent.type is "Shop":
            portrayal["Color"] =Places_To_Colors["Shops"]



    else:
        portrayal={}
    return portrayal
