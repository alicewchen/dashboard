# Import relevant libraries
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from scripts.figures import fig1, fig2, fig3, fig4, fig5, fig6

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server


# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("Bitcoin Ordinal Analysis", style = {"text-align": "center"}),
        html.Div(
            [
                dcc.Graph(
                    id="figure-fig1",
                    figure=fig1,
                    style={
                        "display": "flex",
                        "width": "50%",
                    },
                ),
                dcc.Graph(
                    id="figure-fig2",
                    figure=fig2,
                    style={
                        "display": "flex",
                        "width": "50%",
                    },
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
        html.Div(
            [
                dcc.Graph(
                    id="figure-fig3",
                    figure=fig3,
                    style={
                        "display": "flex",
                        "width": "50%",
                    },
                ),
                dcc.Graph(
                    id="figure-fig4",
                    figure=fig4,
                    style={
                        "display": "flex",
                        "width": "50%",
                    },
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
        html.Div(
            dbc.Row(
                dbc.Col(
                    [
                        dcc.Graph(
                            id="figure-fig5",
                            figure=fig5,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "width": "50%",
                            },
                        ),
                        dcc.Graph(
                            id="figure-fig6",
                            figure=fig6,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "width": "50%",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                    },
                ),
                style={"height": "600px"},
            ),
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
