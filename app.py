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
from scripts.dynamic_figures import dcc_graph_fig1, dcc_graph_fig2
from scripts.text import ordinal_intro, brc20
from scripts.layout_content import num_inscripts_and_ord_size_usage, num_inscr_and_p_inscr_type

# Create the Dash app
server = app.server


# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("Bitcoin Ordinals", style={"text-align": "center"}),
        html.Div(
            dcc.Markdown(
                "*Data was collected from [Dune](https://dune.com) on Oct 18,2023*"
            ),
            style={"text-align": "center"},
        ),
        # Stats Overview
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2(
                                        "{:,}".format(total_inscriptions),
                                        style={"text-align": "center"},
                                    ),
                                    html.H5(
                                        "Total Inscriptions to Date",
                                        style={"text-align": "center"},
                                    ),
                                ]
                            )
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2(
                                        "\u20BF{:,.2f}".format(total_fees_BTC),
                                        style={"text-align": "center"},
                                    ),
                                    html.H5(
                                        "Total Inscription Fees (BTC) to Date",
                                        style={"text-align": "center"},
                                    ),
                                ]
                            )
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2(
                                        "${:,.2f}".format(total_fees_USD),
                                        style={"text-align": "center"},
                                    ),
                                    html.H5(
                                        "Total Inscription Fees (USD) to Date",
                                        style={"text-align": "center"},
                                    ),
                                ]
                            )
                        )
                    ),
                ],
                align="center",
            ),
        ),
        # Introduction
        html.Div(
            dcc.Markdown(ordinal_intro), style={"width": "95%", "text-align": "justify"}
        ),
        # Static Figures: Number of Inscriptions Over Time & Ordinal Size Usage Over Time
        num_inscripts_and_ord_size_usage,
        # Highlight May 2023 BRC-20 minting spree
        html.Div(dcc.Markdown(brc20), style={"width": "95%", "text-align": "justify"}),
        # Dynamic Figures: Ordinal Fees paid in USD/BTC Over Time & Inscription Fee USD/BTC per Category Over Time
        html.Div(
            [
                dbc.Row(
                    dcc.RadioItems(
                        id="radio-fig3-BTCUSD",
                        options=["BTC", "USD"],
                        value="BTC",
                        inline=True,
                    ),
                    style={"align": "center", "text-align": "center"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc_graph_fig1,
                            style={"width": "50%"}
                        ),
                        dbc.Col(
                            dcc_graph_fig2,
                            style={"width": "50%"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "width": "100%",
                        "align": "center",
                        "text-align": "center",
                    },
                ),
            ],
            style={
                # "width": "95%",
                "align": "center",
                "text-align": "center",
            },
        ),
        num_inscr_and_p_inscr_type,
        #html.Div(dcc.Markdown(footnotes), style={"width": "95%", "text-align": "left"}),
    ],
    style={
        # "display": "flex",
        "width": "95%",
        "align": "center",
    },
)

if __name__ == "__main__":
    app.run_server(debug=True)
