from os import closerange
import folium
import pandas
import branca
import ee
import geemap.foliumap as geemap


data = pandas.read_csv(r"C:\Users\Gastón\Python\Primeros proyectos\-files\csv\Udemy\-nuclear-power-stations.csv")
#data_json = pandas.read_json("files\world.json")

latitude = list(data["Latitude"])
longitude = list(data["Longitude"])
name = list(data["Name"])
gross_capacity = list(data["Gross Capacity /MW"])

gross_cap_removed_commas = [i.replace(",", "") for i in gross_capacity]

gross_cap = [int(i) for i in gross_cap_removed_commas]

def color_producer(gc):
    if gc < 700:
        return "lightblue"
    elif 700 <= gc < 1200:
        return "blue"
    else:
        return "darkblue"

map = folium.Map(location = [50.78837912727776, 14.320049151545614], zoom_start=5, tiles= "OpenStreetMap")    

fg = folium.FeatureGroup(name = "My nuclear map")

#here the zip function iterate the first item from both list, and creates a tuple with those two items. 

html = """
<h3><i>Nuclear Plant:</i><b></h3>
<h3><a href="https://www.google.com/search?q=nuclearplant%%22%s%%22" target="_blank">%s</a><b>.</h3>
"""

for lt, ln, nm, gc in zip(latitude, longitude, name, gross_cap):
    iframe = folium.IFrame(html=html % (nm, nm), width=150, height=100)
    fg.add_child(folium.Marker(location = [lt, ln], popup = folium.Popup(iframe), icon = folium.Icon(color = color_producer(gc))))

#specify the min and max values of your data
colormap = branca.StepColormap(['lightblue', 'blue', 'darkblue'],
                       vmin=3, vmax=10, index=[3, 4, 8, 10],
                       caption='step')
colormap.caption = 'Power Plant measured in MW(e)'
colormap.add_to(map)

map.add_child(fg)
map.save("Nuclear Power Plant Map.html")