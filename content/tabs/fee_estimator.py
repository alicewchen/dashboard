from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import skops.io as sio
from scripts.initialize_app import app
from math import log10
import numpy as np
from sklearn import *

import pandas as pd
tab_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.H4("Size (vB) Per Inscription"),
                    dcc.Input(
                        id="ord_size",
                        type="number",
                        value=None,
                        required=True,
                        inputMode="numeric",
                    ),
                    html.H4("Number of Inscriptions"),
                    dcc.Input(
                        id="n",
                        type="number",
                        value=None,
                        required=True,
                        inputMode="numeric",
                        step = 1
                    ),
                    html.H4("Total Inscription Fee"),
                    html.Div(id="fee"),
                ]
            ),
        ]
    )
)

tab_fee_estimator = dbc.Tab(tab_content, label="Fee Estimator")

@app.callback(Output("fee", "children"), Input("ord_size", "value"), Input("n", "value"))
def estimate_fee(ord_size, n):
    if ord_size is None or n is None:
        return None
    elif ord_size <= 0 or n <= 0:
        return "Enter a non-zero positive number"
    elif type(n)!=int:
        return "Enter an integer"
    else: 
        model = sio.load("models/linear_model.skops", trusted=True)
        data = pd.DataFrame({"Ord_vSize_Per_Inscription": [log10(ord_size)], "Inscriptions": [log10(n)]})
        y_pred = model.predict(data).reshape(-1,1)
        total_fee = 10**y_pred[0][0]*n*ord_size
        output = f"{y_pred[0][0]:.2f} sats/vB/Inscription \n {total_fee:.2f} sats"
        return output
