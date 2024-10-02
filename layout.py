from dash import html, dcc
import dash_bootstrap_components as dbc

from region_tools import get_region_tools
from site_tools   import get_popup_plots
#from river_tools  import popup_plots_river

def get_layout():

    map_region, control_data_sel, control_time_sel = get_region_tools()
    popup_plots = get_popup_plots()
    
    panel_layout = dbc.Container([
            dbc.Row([
                dbc.Col([html.Div([map_region, popup_plots])]),
                dbc.Col([
                    dbc.Row(control_data_sel),
                    dbc.Row(control_time_sel),
                ], width=3)
            ])
        ], fluid=True,
        style={'width': '98%', 'min-width': '1000px', 'height': '100%', 'min-height': '800px'}
    )

    return panel_layout

