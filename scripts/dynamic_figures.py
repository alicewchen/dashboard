from scripts.initialize_app import app
from dash import dcc, html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from scripts.utils_data import (
    df,
    inscription_df,
    custom_legend_name,
    mime_category_order,
    default_update_xaxes,
)


####################################################################################################
# Figure 1: Ordinal Fees paid in USD/BTC Over Time
# Figure 2: Inscription Fee per Category Over Time
# Generate dcc Graph components with call backs
####################################################################################################
dcc_graph_fig1 = dcc.Graph(id="dynamic-fig-1")
dcc_graph_fig2 = dcc.Graph(id="dynamic-fig-2")


@app.callback(
    Output("dynamic-fig-1", "figure"),
    Output("dynamic-fig-2", "figure"),
    Input("radio-fig1-BTCUSD", "value"),
)
def update_figure_fig1(value: str):
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
    default_update_xaxes(fig1)
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
        category_orders=mime_category_order,
    )
    default_update_xaxes(fig2)
    fig2.update_yaxes(title_text=ylab)
    fig2.update_layout(legend_title_text="Inscription Type")
    custom_legend_name(
        fig2, ["text", "image", "application", "3D model", "video", "audio", "other"]
    )

    return fig1, fig2


####################################################################################################
# Figure 3: Average Inscription Fee/Byte Over Time (BTC/USD) compare to Average Fees (Inscription+Non-Inscription)
# Figure 4: Average Inscription Fee/Byte per Category Over Time
# Generate dcc Graph components with call backs
####################################################################################################

dcc_graph_fig3 = dcc.Graph(id="dynamic-fig-3")
dcc_graph_fig4 = dcc.Graph(id="dynamic-fig-4")


@app.callback(
    Output("dynamic-fig-3", "figure"),
    Output("dynamic-fig-4", "figure"),
    Input("radio-fig3-fig4-byte", "value"),
    Input("radio-fig3-fig4-BTCUSD", "value"),
)
def update_fig3_fig4(bytes_value: str, value: str):
    if bytes_value == "byte":
        ord_denominator = df.Ord_Size_Usage
        btc_denominator = df.btc_Size_Usage
        fig4_x = "Ord_Size_Per_Inscription"

    elif bytes_value == "vbyte":
        ord_denominator = df.Ord_vSize_Usage
        btc_denominator = df.btc_vSize_Usage
        fig4_x = "Ord_vSize_Per_Inscription"

    if value == "BTC":
        fig3_y1 = df.Ord_Daily_fees / ord_denominator * 100000000
        fig3_y2 = df.btc_Daily_fee / btc_denominator * 100000000
        fig3_ylab = f"Fees (sats/{bytes_value})"
        fig4_z = f"Ord_Daily_fees_{bytes_value}_Per_Inscription"
        fig4_zlab = f"Inscription Fees (sats/{bytes_value})"

    elif value == "USD":
        fig3_y1 = df.Ord_Daily_fees_USD / ord_denominator
        fig3_y2 = df.btc_Daily_fees_USD / btc_denominator
        fig3_ylab = f"Fees ($/{bytes_value})"
        fig4_z = f"Ord_Daily_fees_USD_{bytes_value}_Per_Inscription"
        fig4_zlab = f"Fees ($/{bytes_value})"

    fig4_xlab = f"{bytes_value}s per Inscription"
    # Figure 3: Average Inscription Fee/Byte Over Time (BTC/USD) compare to Average Fees (Inscription+Non-Inscription)

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(
        go.Scatter(x=df.DATE, y=fig3_y1, name="Inscription"),
        secondary_y=False,
    )
    fig3.add_trace(
        go.Scatter(x=df.DATE, y=fig3_y2, name="All"),
        secondary_y=False,
    )
    fig3.update_layout(title_text="Daily Average Transaction " + fig3_ylab)
    default_update_xaxes(fig3)
    fig3.update_yaxes(title_text=fig3_ylab, secondary_y=False)

    # Figure 4: Relationship between Average Inscription Fee/Byte and Ord_Size per Category
    fig4 = px.scatter_3d(
        data_frame=inscription_df,
        x=fig4_x,
        y="Inscriptions",
        z=fig4_z,
        color="MIME_types",
        log_x=True,
        log_y=True,
        log_z=True,
    )
    fig4.update_traces(marker=dict(size=2))
    # default_update_xaxes(fig4)
    fig4.update_layout(scene = dict(
                    xaxis_title=fig4_xlab,
                    yaxis_title="Inscriptions",
                    zaxis_title=fig4_zlab))
    return fig3, fig4
