from scripts.initialize_app import app
from dash import dcc, html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from scripts.utils_data import df, inscription_df, rangeselector_param, tickformatstops_param, custom_legend_name, mime_category_order
#from scripts.utils_data import *
dcc_graph_fig1 = dcc.Graph(id="dynamic-fig-1")
dcc_graph_fig2 = dcc.Graph(id="dynamic-fig-2")
@app.callback(Output("dynamic-fig-1", "figure"), 
              Output("dynamic-fig-2", "figure"),
              Input("radio-fig3-BTCUSD", "value")
              )
def update_figure_fig1(value:str):
    if value == "BTC":
        fig1_y1 = df.Ord_Daily_fees
        fig1_y2 = df.Ord_Total_fees
        fig2_y = "Ord_Daily_fees"
        ylab = "Daily Fees (BTC)"
        ylab_tot = "Total Fees (BTC)"
    elif value == "USD":
        fig1_y1 = df.Ord_Daily_fees_USD
        fig1_y2 = df.Ord_Total_fees_USD
        fig2_y = "Ord_Daily_fees_USD"
        ylab = "Daily Fees (USD)"
        ylab_tot = "Total Fees (USD)"
    
    # Figure 1: Ordinal Fees paid in USD/BTC Over Time
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        go.Scatter(x=df.DATE, y=fig1_y1, name="Daily"),
        secondary_y=False,
    )
    fig1.add_trace(
        go.Scatter(x=df.DATE, y=fig1_y2, name="Total"),
        secondary_y=True,
    )
    fig1.update_layout(title_text="Ordinal Fees Paid")
    fig1.update_xaxes(
        title_text="Date",
        rangeslider_visible=True,
        rangeselector=rangeselector_param,
        tickformatstops=tickformatstops_param,
    )
    fig1.update_yaxes(title_text=ylab, secondary_y=False)
    fig1.update_yaxes(title_text=ylab_tot, secondary_y=True)
    custom_legend_name(fig1, ["Daily", "Cumulative"])


    # Figure 2: Inscription Fee per Category Over Time
    fig2 = px.line(
        inscription_df,
        x="DATE",
        y=fig2_y,
        color="MIME_types",
        title="Daily Fees by Inscription Type",
        category_orders=mime_category_order
    )
    fig2.update_xaxes(
        title="Date",
        type="date",
        rangeslider_visible=True,
        rangeselector=rangeselector_param,
        tickformatstops=tickformatstops_param,
    )
    fig2.update_yaxes(title_text=ylab)
    fig2.update_layout(legend_title_text="Inscription Type")
    custom_legend_name(
        fig2, ["text", "image", "application", "3D model", "video", "audio", "other"]
    )
    
    return fig1, fig2