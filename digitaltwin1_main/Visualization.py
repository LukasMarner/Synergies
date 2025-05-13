## Visualization DT
import pandas as pd
import folium
import geopandas as gpd
from shapely.geometry import Point
from folium.plugins import TimeSliderChoropleth
import numpy as np

def plot_lines_folium(map, gpdf, from_bus, to_bus, line_loading):
    connections_df = pd.DataFrame()
    connections_df['from_bus'] = from_bus
    connections_df['to_bus'] = to_bus
    connections_df['line_loading'] = line_loading
    polyline_layer = folium.FeatureGroup(name='Lines')
    for index, row in connections_df.iterrows():
        from_point = [gpdf[gpdf['new_bus']== row['from_bus']].geometry.values[0].y, gpdf[gpdf['new_bus']== row['from_bus']].geometry.values[0].x]
        to_point = [gpdf[gpdf['new_bus']== row['to_bus']].geometry.values[0].y, gpdf[gpdf['new_bus']== row['to_bus']].geometry.values[0].x]
        color = get_color(row['line_loading'])
        polyline = folium.PolyLine(locations=[from_point, to_point], color=color, weight = 1, popup=f"Line {int(row['from_bus'])}-{int(row['to_bus'])}<br>Line loading:{round(row['line_loading'],1)}%")
        polyline.add_to(polyline_layer)
    legend_html = '''
     <div style="position: fixed; 
                 bottom: 300px; left: 800px; width: 130px; height: 100px; 
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color:white;
                 ">&nbsp; Line loadings (%) <br>
                  &nbsp; 0 - 80 &emsp;  <i class="fa fa-square fa-1x" style="color:rgb(0, 0, 0)"></i><br>
                  &nbsp; 80 - 99 &nbsp;  <i class="fa fa-square fa-1x" style="color:orange"></i><br>
                  &nbsp; 100 &emsp;&nbsp;&nbsp;&nbsp; <i class="fa fa-square fa-1x" style="color:red"></i>
      </div>
     '''
    map.get_root().html.add_child(folium.Element(legend_html))
    map.add_child(polyline_layer)
    # Add layer control
    # polyline_layer_control = folium.LayerControl(position='topleft')
    # polyline_layer_control.add_to(map)
    return map


def get_color(line_loading):
    if line_loading >= 100:
        return 'red'
    elif line_loading > 80:
        return 'orange'
    else:
        return 'black'


def get_buses_df(net):
    # Buses DataFrame
    buses_df = pd.DataFrame({
    'Bus': net.bus['name'],
    'Substation': ['Hasle', 'Hasle', 'Snorrebakken', 'Olsker', 'Rønne Nord', 'Hasle', 'Allinge', 'Svaneke', 'Nexø', 'Bodilsker', 'Povlsker', 
                   'Åkirkeby', 'Dalslunde', 'Østerlars', 'Olsker', 'Gudhjem', 'Viadukten', 'Viadukten', 'Rønne Syd', 'Værket', 'Værket', 'Vesthavnen', 
                   'Viadukten', 'Viadukten', 'Viadukten', 'Hasle', 'Hasle', 'Borrby', 'Tomelilla', 'Værket', 'Værket', 'Værket', 'Værket', 'Værket', 
                   'Værket', 'Værket', 'Værket', 'Snorrebakken', 'Hasle','Hasle', 'Hasle', 'Olsker', 'Østerlars', 'Åkirkeby', 'Nexø', 'Bodilsker', 'Rønne Syd', 'Allinge', 
                   'Svaneke', 'Viadukten', 'Viadukten', 'Rønne Nord', 'Povlsker', 'Vesthavnen', 'Gudhjem'],
    'Voltage kV': net.bus['vn_kv'],
    'vm_pu': net.res_bus['vm_pu']
        })
    return buses_df

def get_gdf_substations():
    substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten', 'Dalslunde', 'Borrby', 'Tomelilla']
    df = pd.DataFrame(
    {
        "Substation": substations,
        "Latitude": [55.068056,55.268333, 55.063056, 55.199167, 55.170278, 55.063056,55.231944, 55.153333, 55.022222, 55.111111, 55.089722,55.111667, 55.134722, 55.14695253737007, 55.102778, 55.097778, 55.11051730808371, 55.457945215609776, 55.542039180824084],
        "Longitude": [14.897778, 14.800278, 15.065833, 14.953056,  14.723333,  15.115833,14.795556, 14.935, 15.055833,14.707778, 14.730556, 14.744444, 15.136111, 14.708142277040857,14.690556, 14.713889, 15.036508198409708, 14.179861159823005, 13.971791742192217],
    }
    )
    substations_df = df
    substations_gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326"
    )
    return substations_gdf, substations_df




def get_buses_gdf(net, buses_df, substations_df):
    buses_merged = buses_df.merge(substations_df, on='Substation')
    # net.res_bus['Bus'] = net.bus['name']
    net_buses = net.res_bus
    net_buses = net_buses.rename(columns = {'Bus name': 'Bus'})
    net_buses['bus number'] = range(0, len(net_buses))
    buses_merged = buses_merged.merge(net_buses, on = 'Bus')
    buses_gdf = gpd.GeoDataFrame(
    buses_merged, 
    geometry=gpd.points_from_xy(buses_merged.Longitude, buses_merged.Latitude))
    buses_gdf.set_crs(epsg=4326, inplace=True)
    # buses_gdf['bus number'] = range(0, len(buses_merged))
    return buses_gdf

def add_10_60kV_layers(map, gdf_10kV, gdf_60kV):
    
    fg_60kV = folium.FeatureGroup(name='Buses 63 kV')

    for index, row in gdf_60kV.iterrows():
        # Get the coordinates of the point
        lat = row.Latitude
        lon = row.Longitude
            # color = colormap(row['LMP'])
        # Add a marker for the point
        if row['vm_pu'] > 1.05 or row['vm_pu'] < 0.95:
            color_bus = 'red'
            if index == 28:
                color_bus='black'
        else:
            color_bus = 'black'
        circlemarker = folium.CircleMarker(location=[lat, lon], radius =3, fill=True, color=color_bus, popup=f"Bus: {row['Bus']} ({row['vm_pu']} pu)")
        circlemarker.add_to(fg_60kV)

    map.add_child(fg_60kV)

    fg_10kV = folium.FeatureGroup(name='Buses 10.5 kV')

    for index, row in gdf_10kV.iterrows():
        # Get the coordinates of the point
        lat = row.Latitude
        lon = row.Longitude
        if row['vm_pu'] > 1.05 or row['vm_pu'] < 0.95:
            color_bus = 'red'
            if index == 28:
                color_bus='black'
        else:
            color_bus = 'black'
            # color = colormap(row['LMP'])
        # Add a marker for the point
        circlemarker = folium.CircleMarker(location=[lat, lon], radius =3, fill=True, color=color_bus, popup=f"Bus: {row['Bus']} ({row['vm_pu']} pu)")
        circlemarker.add_to(fg_10kV)

    map.add_child(fg_10kV)
    marker_layer_control = folium.LayerControl(position='topleft')
    return map

def add_lines(map, gpdf, from_bus, to_bus, line_loading):
    connections_df = pd.DataFrame()
    connections_df['from_bus'] = from_bus
    connections_df['to_bus'] = to_bus
    connections_df['line_loading'] = line_loading
    polyline_layer = folium.FeatureGroup(name='Lines')
    for index, row in connections_df.iterrows():
        from_point = [gpdf[gpdf['bus number']== row['from_bus']].geometry.values[0].y, gpdf[gpdf['bus number']== row['from_bus']].geometry.values[0].x]
        to_point = [gpdf[gpdf['bus number']== row['to_bus']].geometry.values[0].y, gpdf[gpdf['bus number']== row['to_bus']].geometry.values[0].x]
        color = get_color(row['line_loading'])
        polyline = folium.PolyLine(locations=[from_point, to_point], color=color, weight = 1, popup=f"Line {int(row['from_bus'])}-{int(row['to_bus'])}<br>Line loading:{round(row['line_loading'],1)}%")
        polyline.add_to(polyline_layer)

    legend_html = '''
     <div style="position: fixed; 
                 bottom: 300px; left: 800px; width: 130px; height: 100px; 
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color:white;
                 ">&nbsp; Line loadings (%) <br>
                  &nbsp; 0 - 80 &emsp;  <i class="fa fa-square fa-1x" style="color:rgb(0, 0, 0)"></i><br>
                  &nbsp; 80 - 99 &nbsp;  <i class="fa fa-square fa-1x" style="color:orange"></i><br>
                  &nbsp; 100 &emsp;&nbsp;&nbsp;&nbsp; <i class="fa fa-square fa-1x" style="color:red"></i>
      </div>
     '''
    map.get_root().html.add_child(folium.Element(legend_html))
    map.add_child(polyline_layer)
    # Add layer control
    # polyline_layer_control = folium.LayerControl(position='topleft')
    # polyline_layer_control.add_to(map)
    return map


def get_color(line_loading):
    if line_loading >= 100:
        return 'red'
    elif line_loading > 80:
        return 'orange'
    else:
        return 'black'

def get_buses_60_10_kV(buses_df, substations_df):
    buses_df = buses_df.merge(substations_df, on='Substation')
    buses_10kV = buses_df[buses_df['Voltage kV'] == 10.5]
    geometry_10kV = [Point(xy) for xy in zip(buses_10kV['Longitude'], buses_10kV['Latitude'])]
    gdf_10kV = gpd.GeoDataFrame(buses_10kV, geometry=geometry_10kV)
    gdf_10kV.set_crs(epsg=4326, inplace=True)

    # Convert Buses DataFrame to GeoDataFrame for 60 kV
    buses_60kV = buses_df[buses_df['Voltage kV'] == 63]
    geometry_60kV = [Point(xy) for xy in zip(buses_60kV['Longitude'], buses_60kV['Latitude'])]
    gdf_60kV = gpd.GeoDataFrame(buses_60kV, geometry=geometry_60kV)
    gdf_60kV.set_crs(epsg=4326, inplace=True)
    return gdf_10kV, gdf_60kV

def get_transformers_df(net):
    # Buses DataFrame
    transformer_df = pd.DataFrame({
    'Name': net.trafo['name'],
    'Substation': ['Borrby', 'Værket', 'Værket', 'Værket', 'Værket', 'Værket', 'Snorrebakken', 'Hasle', 'Hasle','Olsker', 'Olsker', 
                   'Østerlars', 'Åkirkeby', 'Nexø', 'Nexø', 'Bodilsker', 'Rønne Syd', 'Allinge', 'Allinge','Svaneke', 'Viadukten',
                    'Rønne Nord', 'Povlsker', 'Vesthavnen', 'Gudhjem']
        })
    return transformer_df

def get_transformer_gdf(transformer_df, substations_df):
    transformer_merged = transformer_df.merge(substations_df, on='Substation')
    transformer_gdf = gpd.GeoDataFrame(
    transformer_merged, 
    geometry=gpd.points_from_xy(transformer_merged.Longitude, transformer_merged.Latitude))
    transformer_gdf.set_crs(epsg=4326, inplace=True)
    transformer_gdf['trafo number'] = range(0, len(transformer_merged))
    return transformer_gdf

def add_trafo(map, transformer_gdf, transformer_loadings):
    transformer_loadings=transformer_loadings.rename(columns = {'name': 'Name'})
    transformer_gdf = transformer_gdf.merge(transformer_loadings, on = 'Name')
    trafo_layer = folium.FeatureGroup(name='Transformers')
    # # Add substations as markers
    for _, row in transformer_gdf.iterrows():
        if row['loading_percent'] > 100:
            color_trafo = 'red'
        else:
            color_trafo = 'turquoise'
        circlemarker = folium.CircleMarker(location=[row['Latitude'], row['Longitude']], radius =3, fill=True, color=color_trafo, popup=f"Trafo: {row['Name']} ({row['loading_percent']})")
        circlemarker.add_to(trafo_layer)
        # folium.Marker(
        #     location=[row['Latitude'], row['Longitude']],
        #     popup=f"Transformer: {row['Name']}",
        #     icon=folium.Icon(color='blue', icon='bolt', prefix='fa')
        # ).add_to(trafo_layer)

    map.add_child(trafo_layer)

    return map



# def add_transfomrers():

def create_data_for_time_slider(time_series_data):
    geojson_features = []

    # Loop through each timestamp and combine data
    for timestamp, data in time_series_data.items():
        # Buses
        for _, row in data['buses'].iterrows():
            feature = {
                "type": "Feature",
                "properties": {
                    "time": timestamp,
                    "Type": "Bus",
                    "BusID": row['BusID'],
                    "Voltage": row['Voltage'],
                    "style": {
                        "color": "blue" if row['Voltage'] == 10.5 else "black",
                        "radius": 6,
                        "opacity": 0.8
                    }
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['Longitude'], row['Latitude']]
                }
            }
            geojson_features.append(feature)
        
        # Lines
        for _, row in data['lines'].iterrows():
            # Assuming you have bus locations in a dictionary for simplicity
            bus_locations = {
                'BusA': [41.8902, 12.4924],
                'BusB': [38.1157, 13.3615],
                'BusC': [37.7749, 14.4453]
            }
            from_point = bus_locations[row['from_bus']]
            to_point = bus_locations[row['to_bus']]
            feature = {
                "type": "Feature",
                "properties": {
                    "time": timestamp,
                    "Type": "Line",
                    "LineID": row['LineID'],
                    "Loading": row['Loading'],
                    "style": {
                        "color": "black" if row['Loading'] < 80 else "red",
                        "weight": 2,
                        "opacity": 0.6
                    }
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [from_point, to_point]
                }
            }
            geojson_features.append(feature)
        
        # Transformers
        for _, row in data['transformers'].iterrows():
            feature = {
                "type": "Feature",
                "properties": {
                    "time": timestamp,
                    "Type": "Transformer",
                    "TransformerID": row['TransformerID'],
                    "Power": row['Power'],
                    "style": {
                        "color": "green",
                        "radius": 8,
                        "opacity": 0.7
                    }
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['Longitude'], row['Latitude']]
                }
            }
            geojson_features.append(feature)

    # Create the GeoJSON object
    geojson_data = {
        "type": "FeatureCollection",
        "features": geojson_features
    }



    # Convert to JSON string
    geojson_str = json.dumps(geojson_data)

