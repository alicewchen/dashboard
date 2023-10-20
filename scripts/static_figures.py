#!/usr/bin/env python
# coding: utf-8
# Import
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

pio.templates.default = "simple_white"

RAW_DATA_DIR = "data/raw_data"
agg_inscription = pd.read_csv(f"{RAW_DATA_DIR}/agg_inscription.csv")
btc_fee_size = pd.read_csv(f"{RAW_DATA_DIR}/btc_fee_size.csv")
daily_btcusd = pd.read_csv(f"{RAW_DATA_DIR}/daily_btcusd.csv")
inscription_df = pd.read_csv(f"{RAW_DATA_DIR}/inscription_by_category.csv")

# Merge the dataframes on the 'DATE' column
df = pd.merge(agg_inscription, btc_fee_size, on="DATE")
df = pd.merge(df, daily_btcusd, on="DATE")
df["ord_sat_vSize"] = df["Ord_vSize_Usage"] / df["Ord_Daily_fees"]
# Graph params

rangeselector_param = dict(
    buttons=[
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all"),
    ]
)
tickformatstops_param = [
    dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
    dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
    dict(dtickrange=[60000, 3600000], value="%H:%M m"),
    dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
    dict(dtickrange=[86400000, 604800000], value="%y-%b-%e"),
    dict(dtickrange=[604800000, "M1"], value="%b %Y"),
    dict(dtickrange=["M1", "M12"], value="%b %Y"),
    dict(dtickrange=["M12", None], value="%Y"),
]


####################################################################################################
# Custom functions
####################################################################################################
def custom_legend_name(figure, new_names: list):
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name


####################################################################################################
# Statistics
####################################################################################################

# Total Inscriptions to Date
total_inscriptions = int(max(df.Total_Inscriptions))

# Total Inscription Fees (BTC) to Date
total_fees_BTC = np.round(max(df.Ord_Total_fees), 2)

# Total Inscription Fees (USD to Date)
total_fees_USD = np.round(sum(df.Ord_Daily_fees * df.Price), 2)


####################################################################################################
# Static Graphs
####################################################################################################

# Figure 1: Number of Inscriptions Over Time

fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(
    go.Scatter(x=df.DATE, y=df.Daily_Inscriptions, name="Daily"),
    secondary_y=False,
)
fig1.add_trace(
    go.Scatter(x=df.DATE, y=df.Total_Inscriptions, name="Total"),
    secondary_y=True,
)
fig1.update_layout(title_text="Number of Inscriptions")
fig1.update_xaxes(
    title_text="Date",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig1.update_yaxes(title_text="Daily Volume", secondary_y=False)
fig1.update_yaxes(title_text="Total Volume", secondary_y=True)
custom_legend_name(fig1, ["Daily", "Cumulative"])

# Figure 2: Ordinal Size Usage Over Time

fig2 = px.line(
    df,
    x="DATE",
    y=["Ord_Size_Usage", "Ord_vSize_Usage"],
    title="Ordinal Size Usage",
)
fig2.update_xaxes(
    title="Date",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig2.update_yaxes(title_text="Size Usage")
fig2.update_layout(legend_title_text="Size")
custom_legend_name(fig2, ["bytes", "vbytes"])

# Ordinal Fees paid in USD/BTC Over Time
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(
    go.Scatter(x=df.DATE, y=df.Ord_Daily_fees, name="Daily"),
    secondary_y=False,
)
fig3.add_trace(
    go.Scatter(x=df.DATE, y=df.Ord_Total_fees, name="Total"),
    secondary_y=True,
)
fig3.update_layout(title_text="Ordinal Fees Paid")
fig3.update_xaxes(
    title_text="Date",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig3.update_yaxes(title_text="Daily Fees", secondary_y=False)
fig3.update_yaxes(title_text="Total Fees", secondary_y=True)
custom_legend_name(fig3, ["Daily", "Cumulative"])


# Figure 4: Inscription Fee per Category Over Time

fig4 = px.line(
    inscription_df,
    x="DATE",
    y="Ord_Daily_fees",
    color="MIME_types",
    title="Daily Fees by Inscription Type",
    category_orders={
        "MIME_types": [
            "text",
            "image",
            "application",
            "model",
            "video",
            "audio",
            "other",
        ]
    },
)
fig4.update_xaxes(
    title="Date",
    type="date",
    categoryorder="category descending",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig4.update_yaxes(title_text="Daily Fees")
fig4.update_layout(legend_title_text="Inscription Type")
custom_legend_name(
    fig4, ["text", "image", "application", "3D model", "video", "audio", "other"]
)
# Figure 5: Inscriptions by Category Over Time

fig5 = px.bar(
    inscription_df,
    x="DATE",
    y="Inscriptions",
    color="MIME_types",
    title="Number of Inscriptions by Type",
    category_orders={
        "MIME_types": [
            "text",
            "image",
            "application",
            "model",
            "video",
            "audio",
            "other",
        ]
    },
)
fig5.update_xaxes(
    title="Date",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig5.update_yaxes(title_text="Number of Inscriptions")
fig5.update_layout(legend_title_text="Inscription Type")
custom_legend_name(
    fig5, ["text", "image", "application", "3D model", "video", "audio", "other"]
)

# Figure 6: Distribution of Different Inscription Categories

fig6 = px.pie(
    inscription_df,
    values="Inscriptions",
    names="MIME_types",
    category_orders={
        "MIME_types": [
            "text",
            "image",
            "application",
            "model",
            "video",
            "audio",
            "other",
        ]
    },
    title="Proportion of Inscription Types",
)
fig6.update_layout(legend_title_text="Inscription Type")

#####################################################################################################
# Store All Static Figures in Dictionary
#####################################################################################################
all_fig = [fig1, fig2, fig3, fig4, fig5, fig6]
static_fig = {}
for idx, f in enumerate(all_fig):
    static_fig.update({f"static-fig-{idx+1}": f})

# custom_legend_name(fig6, ['text', 'image', 'application', '3d model', 'video', 'audio', 'other'])
# Figure 7: Ordinal Sat/vB

#####################################################################################################
# Dynamic Figures
#####################################################################################################
# def get_fig_callbacks(app):
    
#     # Ordinal Fees paid in USD/BTC Over Time
#     @app.callback(
        
#     )
#     def fig3_callback():
#         fig3 = make_subplots(specs=[[{"secondary_y": True}]])
#         fig3.add_trace(
#             go.Scatter(x=df.DATE, y=df.Ord_Daily_fees, name="Daily"),
#             secondary_y=False,
#         )
#         fig3.add_trace(
#             go.Scatter(x=df.DATE, y=df.Ord_Total_fees, name="Total"),
#             secondary_y=True,
#         )
#         fig3.update_layout(title_text="Ordinal Fees Paid")
#         fig3.update_xaxes(
#             title_text="Date",
#             rangeslider_visible=True,
#             rangeselector=rangeselector_param,
#             tickformatstops=tickformatstops_param,
#         )
#         fig3.update_yaxes(title_text="Daily Fees", secondary_y=False)
#         fig3.update_yaxes(title_text="Total Fees", secondary_y=True)
#         custom_legend_name(fig3, ["Daily", "Cumulative"])
#         return fig3