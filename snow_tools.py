from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace, arrow_function

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from config import snow_course_stations, snow_pillow_stations, graph_config

# start to build maps
ns = Namespace('dashExtensions', 'default')


# draw snow course time series
def draw_course(staid):
    if staid in snow_course_stations:
        fcsv = f'data/cdec/snow_course/SWE_monthly_{staid}.csv'
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date')
        fig_course = go.Figure()
        fig_course.add_trace(go.Scatter(x=df.index, y=df['SWE'], name='Snow Water Equivalent', mode='lines+markers', line=go.scatter.Line(color='magenta')))
    else:
        fig_course = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': ''})
    fig_course.update_layout(margin=dict(l=15, r=15, t=15, b=5),
                          plot_bgcolor='#eeeeee',
                          legend=dict(title='', yanchor='top', y=0.99, xanchor='right', x=0.92),
                          hovermode='x unified') #, font=dict(size=20))
    fig_course.update_yaxes(title='Snow Water Equivalent (in)')
    fig_course.update_traces(hovertemplate=None)
    return fig_course

# draw snow pillow time series
def draw_pillow(staid):
    if staid in snow_pillow_stations:
        fcsv = f'data/cdec/snow_pillow/SWE_daily_{staid}.csv'
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date')
        df.drop(df[(df['SWE']<-10)|(df['SWE']>100)].index, inplace=True)
        fig_course = go.Figure()
        fig_course.add_trace(go.Scatter(x=df.index, y=df['SWE'], name='Snow Water Equivalent', mode='lines', line=go.scatter.Line(color='magenta')))
    else:
        fig_course = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': ''})
    fig_course.update_layout(margin=dict(l=15, r=15, t=15, b=5),
                          plot_bgcolor='#eeeeee',
                          legend=dict(title='', yanchor='top', y=0.99, xanchor='right', x=0.92),
                          hovermode='x unified') #, font=dict(size=20))
    fig_course.update_yaxes(title='Snow Water Equivalent (in)')
    fig_course.update_traces(hovertemplate=None)
    return fig_course

    
def get_snow_tools():

    # tool panel
    tool_style  = {'min-height': '312px', 'background-color': 'white', 'font-size': 'small', 'border': '1px solid lightgray', 'border-top-style': 'none'}

    tabtitle_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
    tabtitle_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

    ## pop-up window and its tabs/graphs
    fig_course  = draw_course('GRZ')
    fig_pillow  = draw_pillow('RTL')
    graph_course = dcc.Graph(id='snow-graph-course', figure=fig_course, style={'height': '360px'}, config=graph_config)
    graph_pillow = dcc.Graph(id='snow-graph-pillow', figure=fig_pillow, style={'height': '360px'}, config=graph_config)

    tabtitle_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
    tabtitle_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

    tab_course = dcc.Tab(label='Snow Course', value='snow-course', children=[dcc.Loading(id='loading-snow-course', children=graph_course)], style=tabtitle_style, selected_style=tabtitle_selected_style)
    tab_pillow = dcc.Tab(label='Snow Pillow', value='snow-pillow', children=[dcc.Loading(id='loading-snow-pillow', children=graph_pillow)], style=tabtitle_style, selected_style=tabtitle_selected_style)

    popup_tabs_course = dcc.Tabs([tab_course], id='course-popup-tabs', value='snow-course')
    popup_tabs_pillow = dcc.Tabs([tab_pillow], id='pillow-popup-tabs', value='snow-pillow')
    
    course_popup_plots = dbc.Offcanvas([popup_tabs_course],
        title='Snow Courses', placement='top', is_open=False, scrollable=True, id='course-popup-plots',
        style={'opacity': '0.9', 'width': '90%', 'min-width': '1000px', 'min-height': '540px', 'margin-top': '150px', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': 'smaller'}
    )
    pillow_popup_plots = dbc.Offcanvas([popup_tabs_pillow],
        title='Snow Pillows', placement='top', is_open=False, scrollable=True, id='pillow-popup-plots',
        style={'opacity': '0.9', 'width': '90%', 'min-width': '1000px', 'min-height': '540px', 'margin-top': '150px', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': 'smaller'}
    )

    return course_popup_plots, pillow_popup_plots
