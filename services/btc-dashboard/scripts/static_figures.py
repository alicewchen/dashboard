#!/usr/bin/env python
# coding: utf-8
# Import
import plotly.express as px
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scripts.utils_data import (
    inscription_df,
    df,
    rangeselector_param,
    tickformatstops_param,
    mime_category_order,
    custom_legend_name,
    default_update_xaxes,
)

pio.templates.default = "simple_white"


####################################################################################################
# Statistics
####################################################################################################

# Total Inscriptions to Date
total_inscriptions = int(max(df.Total_Inscriptions))

# Total Inscription Fees (BTC) to Date
total_fees_BTC = np.round(max(df.Ord_Total_fees), 2)

# Total Inscription Fees (USD to Date)
total_fees_USD = np.round(sum(df.Ord_Daily_fees * df.Price), 2)

# Correlation between 

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
default_update_xaxes(fig1)
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
default_update_xaxes(fig2)
fig2.update_yaxes(title_text="Size Usage")
fig2.update_layout(legend_title_text="Size")
custom_legend_name(fig2, ["bytes", "vbytes"])


# Figure 3: Inscriptions by Category Over Time

fig3 = px.bar(
    inscription_df,
    x="DATE",
    y="Inscriptions",
    color="MIME_types",
    title="Number of Inscriptions by Type",
    category_orders=mime_category_order,
)
default_update_xaxes(fig3)
fig3.update_yaxes(title_text="Number of Inscriptions")
fig3.update_layout(legend_title_text="Inscription Type")
custom_legend_name(
    fig3, ["text", "image", "application", "3D model", "video", "audio", "other"]
)

# Figure 4: Distribution of Different Inscription Categories

fig4 = px.pie(
    inscription_df,
    values="Inscriptions",
    names="MIME_types",
    category_orders=mime_category_order,
    title="Proportion of Inscription Types",
)
fig4.update_layout(legend_title_text="Inscription Type")

#####################################################################################################
# Store All Static Figures in Dictionary
#####################################################################################################
all_fig = [fig1, fig2, fig3, fig4]
static_fig = {}
for idx, f in enumerate(all_fig):
    static_fig.update({f"static-fig-{idx+1}": f})
