# Import relevant libraries
import pandas as pd
import numpy as np
import plotly.express as px
from scripts.initialize_app import app
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from scripts.static_figures import (
    total_inscriptions,
    total_fees_BTC,
    total_fees_USD,
)
from scripts.dynamic_figures import (
    dcc_graph_fig1,
    dcc_graph_fig2,
    dcc_graph_fig3,
    dcc_graph_fig4,
)
from scripts.text import ordinal_intro, brc20
from scripts.layout_content import (
    num_inscripts_and_ord_size_usage,
    num_inscr_and_p_inscr_type,
)
from content.tabs.overview import tab_overview 
from content.tabs.inscription_type import tab_inscription_type
from content.tabs.fee_estimator import tab_fee_estimator

# Create the Dash app
server = app.server


# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("Bitcoin Ordinals", style={"text-align": "center"}),
        html.Div(
            dcc.Markdown(
                "*Data was last updated on Oct 18,2023*"
            ),
            style={"text-align": "center"},
        ),
        dbc.Tabs([tab_overview,tab_inscription_type,tab_fee_estimator]),
    ],
    style={
        "width": "95%",
        "align": "center",
        "text-align": "center",
    },
)

if __name__ == "__main__":
    app.run_server(debug=True)
