from main import app
from config import all_stations, fnf_stations

from dash.dependencies import ClientsideFunction, Input, Output, State
from datetime import datetime, timedelta
import pandas as pd

from site_tools import draw_retro, draw_mofor, draw_table, draw_table_all
from basin_tools import draw_basin_ts_nrt
## Callbacks from here on

# callback to update data var in the title section
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_title_var'
    ),
    Output('title-var', 'children'),
    Input(component_id='data-sel',  component_property='value'),
    Input(component_id='met-vars',  component_property='value'),
    Input(component_id='hydro-vars', component_property='value')
)

# callback to update data date in the title section
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_title_date'
    ),
    Output('title-date', 'children'),
    Input('datepicker', 'date')
)

# callback to update url of image overlay
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_img_url'
    ),
    Output('data-img', 'url'),
    Input('datepicker', 'date'),
    Input(component_id='data-sel',  component_property='value'),
    Input(component_id='met-vars',  component_property='value'),
    Input(component_id='hydro-vars', component_property='value')
)

# callback to update url of color bar
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_cbar'
    ),
    Output('data-cbar-img', 'src'),
    Input(component_id='data-sel',  component_property='value'),
    Input(component_id='met-vars',  component_property='value'),
    Input(component_id='hydro-vars', component_property='value')
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_cbar_visibility'
    ),
    Output('data-cbar', 'style'),
    Input(component_id='data-map-ol', component_property='checked')
)

# callback to update datepicker and slider on button clicks
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_date'
    ),
    Output('datepicker', 'date'),
    Input('button-forward-day',  'n_clicks_timestamp'),
    Input('button-backward-day', 'n_clicks_timestamp'),
    Input('button-forward-month',   'n_clicks_timestamp'),
    Input('button-backward-month',  'n_clicks_timestamp'),
    Input('datepicker', 'date'),
    Input('datepicker', 'min_date_allowed'),
    Input('datepicker', 'max_date_allowed')
)

# update system status periodically
@app.callback(Output(component_id='datepicker', component_property='max_date_allowed'),
              Input('interval-check_system', 'n_intervals'))
def update_system_status(basin):
    fcsv = 'data/system_status.csv'
    df_status = pd.read_csv(fcsv, parse_dates=True)
    return datetime.fromisoformat(df_status['WRF-Hydro NRT'][1]).date()

# callback to switch river vector sources according to zoom level
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='switch_river_vector'
    ),
    Output('nwm-rivers', 'url'),
    Output('nwm-rivers', 'zoomToBoundsOnClick'),
    Input('map-region', 'zoom')
)

# create/update historic time series graph in popup
@app.callback(Output(component_id='graph-retro', component_property='figure'),
              Output(component_id='graph-mofor', component_property='figure'),
              Output(component_id='div-table', component_property='children'),
              Output('popup-plots', 'is_open'),
              Output('popup-plots', 'title'),
              Input('b120-points', 'clickData'),
              Input('slider_updates', 'value'),
              Input('radio_pp', 'value'))
def update_flows(fcst_point, yday_update, pp):
    fcsv = 'data/system_status.csv'
    df_system_status = pd.read_csv(fcsv, parse_dates=True)
    fcst_t1 = datetime.fromisoformat(df_system_status['ESP-WWRF Fcst'][0]).date()
    fcst_t2 = datetime.fromisoformat(df_system_status['ESP-WWRF Fcst'][1]).date()
    if fcst_point==None:
        staid = 'FTO'
        stain = 'FTO: Feather River at Oroville'
    else:
        staid = fcst_point['properties']['Station_ID']
        stain = fcst_point['properties']['tooltip']
    fcst_update = datetime(fcst_t1.year, 1, 1) + timedelta(days=yday_update-1)
    fcst_type = f'{pp}'
    fig_retro = draw_retro(staid)
    fig_mofor = draw_mofor(staid, fcst_type, fcst_t1, fcst_t2, fcst_update)
    if staid!='TNL':
        table_fcst = draw_table(staid, all_stations[staid], fcst_type, fcst_t1, fcst_t2, fcst_update)
    else:
        table_fcst = draw_table_all(fcst_type, fcst_t1, fcst_t2, fcst_update)
    
    return [fig_retro, fig_mofor, table_fcst, True, stain]

# create/update historic time series graph in popup
@app.callback(Output(component_id='basin-graph-nrt', component_property='figure'),
              Output('basin-popup-plots', 'is_open'),
              Output('basin-popup-plots', 'title'),
              Input('b120-watersheds', 'clickData'))
def update_basin(basin):
    if basin==None:
        staid = 'FTO'
        stain = 'FTO: Feather River at Oroville'
    else:
        staid = basin['properties']['Station']
        stain = basin['properties']['tooltip']
    fig_nrt = draw_basin_ts_nrt(staid)
    
    return [fig_nrt, True, stain]

