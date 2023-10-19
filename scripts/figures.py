#!/usr/bin/env python
# coding: utf-8
# Import
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

RAW_DATA_DIR = "data/raw_data"
agg_inscription = pd.read_csv(f"{RAW_DATA_DIR}/agg_inscription.csv")
btc_avg_fee = pd.read_csv(f"{RAW_DATA_DIR}/btc_avg_fee.csv")
daily_btcusd = pd.read_csv(f"{RAW_DATA_DIR}/daily_btcusd.csv")
inscription_df = pd.read_csv(f"{RAW_DATA_DIR}/inscription_by_category.csv")

# Merge the dataframes on the 'DATE' column
df = pd.merge(agg_inscription, btc_avg_fee, on="DATE")
df = pd.merge(df, daily_btcusd, on="DATE")
df["ord_sat_vSize"] = df["Ord_vSize_Usage"] / df["Daily_fees"]
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

# Statistics



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
custom_legend_name(fig2, ["bytes", "vbytes"])

# Figure 3: Inscription Fees Over Time

fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(
    go.Scatter(x=df.DATE, y=df.Daily_fees, name="Daily"),
    secondary_y=False,
)
fig3.add_trace(
    go.Scatter(x=df.DATE, y=df.Total_fees, name="Total"),
    secondary_y=True,
)
fig3.update_layout(title_text="Inscription Fees")
fig3.update_xaxes(
    title_text="Date",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig3.update_yaxes(title_text="Daily Volume", secondary_y=False)
fig3.update_yaxes(title_text="Total Volume", secondary_y=True)
custom_legend_name(fig3, ["Daily", "Cumulative"])

# Figure 4: Inscription Fee per Category Over Time

fig4 = px.line(
    inscription_df,
    x="DATE",
    y="Ord_Daily_fees",
    color="MIME_types",
    title="Daily Fees by Inscription Type",
)
fig4.update_xaxes(
    title="Date",
    type = "date",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig4.update_yaxes(title_text="Daily Fees")
# Figure 5: Inscriptions by Category Over Time

fig5 = px.bar(
    inscription_df,
    x="DATE",
    y="Inscriptions",
    color="MIME_types",
    title="Number of Inscriptions by Type",
)
fig5.update_xaxes(
    
    title="Date",
    rangeslider_visible=True,
    rangeselector=rangeselector_param,
    tickformatstops=tickformatstops_param,
)
fig5.update_yaxes(title_text="Number of Inscriptions")


# Figure 6: Distribution of Different Inscription Categories

fig6 = px.pie(
    inscription_df,
    values="Inscriptions",
    names="MIME_types",
    title="Proportion of Inscription Types",
)

# Figure 7: Ordinal Sat/vB 
