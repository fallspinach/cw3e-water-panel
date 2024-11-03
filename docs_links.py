from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_extensions.javascript import Namespace, arrow_function

from datetime import date, datetime, timedelta

from config import tool_style, tabtitle_style, tabtitle_selected_style

# start to build maps
ns = Namespace('dashExtensions', 'default')
    
def get_docs_links():

    gdoc = html.Iframe(src='https://docs.google.com/document/d/e/2PACX-1vRpsWbx0SGVU6PXPeVBkQdB9rG2AT5AixiVeoLCw5srjblHIYv1HzBDTmBL3hvaQsU69rkfUt0RyyM3/pub?embedded=true',
                       width='98%', height='98%')
    gdoc_popup = dbc.Offcanvas([gdoc],
        title='CW3E WRF-Hydro Environment Documentation', placement='top', is_open=False, scrollable=True, id='gdoc-popup',
        style={'opacity': '1', 'width': '900px', 'height': '95%', 'margin-top': '50px', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': 'smaller'}
    )

    tab_style = tool_style.copy()
    tab_style.update({'min-height': '180px', 'padding-top': '20px', 'text-align': 'center'})
    
    docs = html.Div([dbc.Button('Documentation', id='gdoc-button', outline=True, color='primary', className='me-1'),
                     html.P('Click the button to open the Google Doc in a pop-up window, then click "5. Web app (Dash) for interactive visualizations" in the "Table of Contents" to go to Section 5.'),
    ], style=tab_style)

    links = html.Div([''], style=tab_style)
    
    docs_links = html.Div(dcc.Tabs([
        dcc.Tab(docs,  label='Documentation', value='tab-docs',  style=tabtitle_style, selected_style=tabtitle_selected_style),
        dcc.Tab(links, label='Links',         value='tab-links', style=tabtitle_style, selected_style=tabtitle_selected_style),
    ], style={'margin-top': '10px'}, value='tab-docs'))

    return gdoc_popup, docs_links
