from folium import Map, TileLayer, Marker
from folium.plugins import HeatMap

carte = Map(location=[45.764037, 4.835659], zoom_start=10)

tile_layer = TileLayer('OpenStreetMap', opacity=0.7, tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
carte.add_child(tile_layer)

marker = Marker(location=[45.764037, 4.835659], popup='Lyon', icon=folium.Icon(color='red'))
carte.add_child(marker)

heat_map = HeatMap([[45.764037, 4.835659]], radius=10, blur=5, max_val=10, min_val=0, gradient={0.4: 'red', 0.6: 'yellow', 1: 'green'})
carte.add_child(heat_map)

carte
