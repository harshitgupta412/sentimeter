import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from colorspacious import cspace_converter
from collections import OrderedDict
from matplotlib.colors import Normalize,ListedColormap,LinearSegmentedColormap
import numpy as np

data = pd.read_csv('States.csv')

fig, ax = plt.subplots()
m = Basemap(resolution='c',projection='merc',lat_0=54.5,lon_0=-4.36,llcrnrlon=68.,llcrnrlat=6.,urcrnrlon=97,urcrnrlat=37.)

m.drawmapboundary(fill_color="#46bcec")
m.fillcontinents(color="#f2f2f2",lake_color='#46bcec')
m.drawcoastlines()

m.readshapefile('IND_adm/IND_adm1','INDIA')
d = []
for state_info in m.INDIA_info:
    state =state_info['NAME_1']
    r = 0
    for i in data.index:
        if data['State'][i].lower() == state.lower():
            r = data['Value'][i]
            break
    d.append(r)
map_data = pd.DataFrame({
    'shapes': [Polygon(np.array(shape),True) for shape in m.INDIA],
    'area': [area['NAME_1'] for area in m.INDIA_info],
    'satlist': d,
})

shapes = [Polygon(np.array(shape),True) for shape in m.INDIA]
cmap = plt.get_cmap('Oranges')
cmap = plt.get_cmap('RdYlGn',512)
cmap = ListedColormap(cmap(np.linspace(0.15,0.85,256)))

# colors = ["darkorange", "gold", "greenyellow", "lawngreen", "limegreen"]
# cmap = LinearSegmentedColormap.from_list("mycmap", colors)

pc = PatchCollection(shapes,zorder=2)
norm = Normalize()

pc.set_facecolor(cmap(norm(map_data['satlist'].fillna(0).values)))
ax.add_collection(pc)

# Create a mapper to map color intensities to values
mapper = matplotlib.cm.ScalarMappable(cmap=cmap)
mapper.set_array(d)
plt.colorbar(mapper, shrink=0.4)
# Set title for the plot
ax.set_title("DISTRIBUTION ON INDIAN STATES")
# Change plot size and font size
plt.rcParams['figure.figsize'] = (15,15)
plt.rcParams.update({'font.size': 20})
plt.show()

print('done')