from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from scripts.dynamic_figures import (
    dcc_graph_fig3,
    dcc_graph_fig4,
)
from scripts.layout_content import (
    num_inscr_and_p_inscr_type,
)

tab_content = dbc.Card(
    dbc.CardBody(
        [
            # Static Figures: Inscriptions by Category Over Time
            num_inscr_and_p_inscr_type,
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.RadioItems(
                                    id="radio-fig3-fig4-BTCUSD",
                                    options=["BTC", "USD"],
                                    value="BTC",
                                    inline=True,
                                    labelStyle={"width": "4rem"},
                                    style={"marginRight": "20px"},
                                ),
                                style={
                                    "width": "50%",
                                    "text-align": "center",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "align": "center",
                            "text-align": "center",
                            "width": "100%",
                        },
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc_graph_fig3, style={"width": "50%"}),
                            dbc.Col(
                                dcc_graph_fig4,
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
        ]
    )
)
tab_inscription_type = dbc.Tab(tab_content, label="Inscription Types")