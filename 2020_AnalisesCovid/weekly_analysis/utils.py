# Data Manipulation
import pandas as pd

# I/O
from os import getcwd, makedirs
from os.path import exists
import json
from io import StringIO

# Visualization
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ChartLine:
    def __init__(self, legend, column, color):
        self.legend = legend
        self.column = column
        self.color = color

class Marker:
    def __init__(self, date, legend, x_column, y_column, color):
        self.date = date
        self.legend = legend
        self.x_column = x_column
        self.y_column = y_column
        self.color = color

class GeoMap:
    def __init__(self, data, geojson, color_column, locations_column, featureid_key, level_colors, level_labels, title):
        self.data = data
        self.geojson = geojson
        self.color_column = color_column
        self.locations_column = locations_column
        self.featureid_key = featureid_key
        self.level_labels = level_labels
        self.level_colors = level_colors
        self.title = title

def load_csv_data(data_file, remote_data_url=None, download_data_anew=False, verbose=False):
    # Identify Data Directory
    data_dir_path = "{}/data".format(getcwd())
    data_file_path = "{}/{}".format(data_dir_path, data_file)
    
    # Check if remote download possible for missing data
    if remote_data_url is not None and not exists(data_file_path):
        download_data_anew = True

    # Load Data
    if download_data_anew:
        # Download Data from Server
        if verbose:
            print("Downloading data from server...")

        full_data = pd.read_csv(remote_data_url)

        # Save Data Locally
        if not exists(data_dir_path):
            makedirs(data_dir_path)

        full_data.to_csv(data_file_path)

        if verbose:
            print("Download complete!\n\nData saved to: /data/{}".format(data_file))
    else:
        # Use Local Data
        if verbose:
            print("Data loaded from local file.")

        full_data = pd.read_csv(data_file_path)

    return full_data

def load_json_data(data_file, verbose=False):
    # Identify Data Directory
    data_dir_path = "{}/data".format(getcwd())
    data_file_path = "{}/{}".format(data_dir_path, data_file)

    # Read Data
    with open(data_file_path) as json_file:
        data = json.load(json_file)
    
    if verbose:
        print("Data successfully loaded.")
    
    return data

def geopandas_to_geojson(geopandas_df):
    # Convert Geopandas Dataframe to GeoJSON
    # (For use with Plotly)
    stream = StringIO(geopandas_df.to_json())
    geojson = json.load(stream)

    return geojson


def display_line_chart(df, x_data, chart_lines, markers, title, x_axis, y_axis, include_annotations=False,
                      save_HTML=False):
    fig = go.Figure()

    # Plot Lines 
    for line in chart_lines:
        fig.add_trace(go.Scatter(x= df[x_data], 
                                 y= df[ line.column ], 
                                 name= line.legend, 
                                 line= dict(color=line.color) )
                              )
    # Plot Markers
    for marker in markers:
        # Format Date according to Dataframe Convention
        formatted_date_str = "{:%Y-%m-%d}".format(marker.date)
        
        # Capture Marker Y value
        y_value = float(df[ df[marker.x_column] ==formatted_date_str ][marker.y_column])
        
        # Build Annotation Strings
        if include_annotations:
            annotation_formated_value = "{:,.0f}".format(y_value).replace(",", ".")
            annotation = f"<b>{annotation_formated_value}</b>"
        else:
            annotation = ""

        # Add Marker on Plot
        fig.add_trace(go.Scatter(x= [formatted_date_str], 
                                 y= [y_value], 
                                 mode= 'markers+text',
                                 marker= dict(color=marker.color),
                                 showlegend= False,
                                 name= marker.legend,
                                 text=annotation,
                                 textposition="bottom center",
                                 textfont_size=15,
                                 textfont_color = marker.color
                                )
                    )

    fig.update_layout(title=title,
                      xaxis_title=x_axis,
                      yaxis_title=y_axis,
                      legend=dict(yanchor="bottom", xanchor="left", y=-0.2,x=-0.01)
                     )
    fig.show()
    
    # Save Interactive HTML?
    if save_HTML:
        fig.write_html(f"{getcwd()}/{title}.html")


def display_bar_chart(df, title, x_axis, y_axis, showlegend=False, orientation="v"):
    fig = px.bar(df, title=title, orientation=orientation)

    fig.update_layout(showlegend=showlegend,
                      xaxis_title=x_axis, yaxis_title=y_axis)

    fig.show()

def build_choropleth_maps(geomaps, general_title, center_lon=-47.92, center_lat=-15.82, default_zoom=2):
    # Prepare Subplot Figure
    subplot_types = [ {'type': 'mapbox'} for i in geomaps ]
    subplot_titles = [ geomap.title for geomap in geomaps]
    
    fig_maps = make_subplots(rows=1, cols=len(geomaps), specs=[subplot_types], 
                             subplot_titles=subplot_titles)

    # Add Categorical Choropleth Maps
    for i, geomap in enumerate(geomaps):
        categories = enumerate(geomap.data[geomap.color_column].unique())
        
        # Build Plotly Discrete Color Scale
        color_dict = {}
        for level, color in geomap.level_colors.items():
            color_dict[level] = [ [0.0, color], [1.0, color] ]

        # Add Colors One by One
        for j, category in categories:
            dfp = geomap.data[ geomap.data[ geomap.color_column] == category ]
            fig_maps.add_trace(go.Choroplethmapbox(geojson=geomap.geojson, 
                                                   locations=dfp[geomap.locations_column],
                                                   z=[category,] * len(dfp), 
                                                   featureidkey= geomap.featureid_key,
                                                   showlegend=False,
                                                   name=geomap.level_labels[category],
                                                   colorscale=color_dict[category], 
                                                   showscale=False
                                                  ), 
                               row=1, col=i+1
                              )

    # Format Maps
    fig_maps.update_layout({ 'title' : general_title}, showlegend=True)
    fig_maps.update_mapboxes(style="white-bg", center={"lon" : center_lon ,"lat" : center_lat}, zoom=default_zoom)

    fig_maps.show()