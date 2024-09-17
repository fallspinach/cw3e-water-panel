from dash import html, dcc
import dash_bootstrap_components as dbc

from region_tools import map_region, control_data_sel, control_time_sel
#from site_tools   import popup_plots
#from river_tools  import popup_plots_river

panel_layout = dbc.Container([
        dbc.Row([
            dbc.Col([html.Div(map_region)]),
            dbc.Col([
                dbc.Row(control_data_sel),
                dbc.Row(control_time_sel),
            ], width=3)
        ])
    ], fluid=True,
    style={'width': '98%', 'min-width': '1000px', 'height': '100%', 'min-height': '800px'}
)

