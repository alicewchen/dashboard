# Import relevant libraries
from dash import dcc, html
import dash_bootstrap_components as dbc
from scripts.static_figures import (
    total_inscriptions,
    total_fees_BTC,
    total_fees_USD,
)
from scripts.dynamic_figures import (
    dcc_graph_fig1,
    dcc_graph_fig2,
)
from scripts.text import ordinal_intro, brc20
from scripts.layout_content import (
    num_inscripts_and_ord_size_usage,
)


tab_content = dbc.Card(
    dbc.CardBody(
        [
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
                            ),
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
                            ),
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
                            ),
                        ),
                    ],
                    align="center",
                    justify="center",
                    style={"width": "100%", "margin": "auto"},
                ),
            ),
            # Introduction
            html.Div(
                dcc.Markdown(ordinal_intro),
                style={"width": "95%", "margin": "auto", "text-align": "justify"},
            ),
            # Static Figures: Number of Inscriptions Over Time & Ordinal Size Usage Over Time
            num_inscripts_and_ord_size_usage,
            # Dynamic Figure 1: Ordinal Fees paid in USD/BTC Over Time
            # Dynamic Figure 2: Average Inscription Fee/Byte Over Time (BTC/USD) compare to Average Fees (Inscription+Non-Inscription)
            dbc.Row(
                [
                    dbc.Row(
                        dcc.RadioItems(
                            id="radio-fig1-BTCUSD",
                            options=["BTC", "USD"],
                            value="BTC",
                            labelStyle={"width": "3rem"},
                            inline=True,
                        ),
                        style={"align": "center", "text-align": "center"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc_graph_fig1, style={"width": "50%"}),
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
            ),
            # Highlight May 2023 BRC-20 minting spree
            html.Div(
                dbc.Row(
                    [
                        dbc.Card(
                            dcc.Markdown(brc20),
                            style={
                                "text-align": "justify",
                                "width": "50%",
                                "margin": "auto",
                            },
                        )
                    ],
                    justify="center",
                    align="center",
                ),
            ),
        ],
        className="mt-3",
    )
)
tab_overview = dbc.Tab(tab_content, label="Overview")
