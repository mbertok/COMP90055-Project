from TestMesa import Model
import numpy as np
import matplotlib.pyplot as plt
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer



model = Model(50, 10, 10)
for i in range(100):
    model.step()
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
    plt.imshow(agent_counts, interpolation='nearest')
    #plt.refreshdata
    #plt.drawnow
#plt.colorbar()

    # If running from a text editor or IDE, remember you'll need the following:
    #plt.show()
#gini = model.datacollector.get_model_vars_dataframe()
#gini.plot()