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
        ylab = "Fees (sats/vB)"
        fig1_y1 = df.Ord_Daily_fees
        fig1_y2 = df.Ord_Total_fees
        fig1_ylab_tot = "Total Fees (\u20BF)"
        fig2_y1 = df.Ord_Daily_fees_vSize 
        fig2_y2 = df.btc_Daily_fees_vSize 
        
        
    elif value == "USD":
        ylab = "Fees ($/vB)"
        fig1_y1 = df.Ord_Daily_fees_USD
        fig1_y2 = df.Ord_Total_fees_USD
        fig1_ylab_tot = "Total Fees (USD)"
        fig2_y1 = df.Ord_Daily_fees_vSize_USD
        fig2_y2 = df.btc_Daily_fees_vSize_USD
        


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
    fig1.update_yaxes(title_text=fig1_ylab_tot, secondary_y=True)
    custom_legend_name(fig1, ["Daily", "Cumulative"])

    # Figure 2: Average Inscription Fee/Byte Over Time (BTC/USD) compare to Average Fees (Inscription+Non-Inscription)

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Scatter(x=df.DATE, y=fig2_y1, name="Inscription"),
        secondary_y=False,
    )
    fig2.add_trace(
        go.Scatter(x=df.DATE, y=fig2_y2, name="All"),
        secondary_y=False,
    )
    fig2.update_layout(title_text="Daily Average Transaction " + ylab)
    default_update_xaxes(fig2)
    fig2.update_yaxes(title_text=ylab, secondary_y=False)

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
    Input("radio-fig3-fig4-BTCUSD", "value"),
)
def update_fig3_fig4(value: str):

    if value == "BTC":
        fig3_y = "Ord_Daily_fees"
        fig3_ylab = "Daily Fees (\u20BF)"
        fig4_z = f"Ord_Daily_fees_vbyte_Per_Inscription"
        fig4_zlab = f"Inscription Fees (sats/vB)"

    elif value == "USD":
        fig3_y = "Ord_Daily_fees_USD"
        fig3_ylab = "Daily Fees (USD)"
        
        fig4_z = f"Ord_Daily_fees_USD_vbyte_Per_Inscription"
        fig4_zlab = f"Fees ($/vB)"
    fig4_x = "Ord_vSize_Per_Inscription"
    fig4_xlab = "vB per Inscription"
    
    # Figure 2: Inscription Fee per Category Over Time
    fig3 = px.line(
        inscription_df,
        x="DATE",
        y=fig3_y,
        color="MIME_types",
        title="Daily Fees by Inscription Type",
        category_orders=mime_category_order,
    )
    default_update_xaxes(fig3)
    fig3.update_yaxes(title_text=fig3_ylab)
    fig3.update_layout(legend_title_text="Inscription Type")
    custom_legend_name(
        fig3, ["text", "image", "application", "3D model", "video", "audio", "other"]
    )
    
    

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
    fig4.update_layout(legend_title_text="Inscription Type")
    # default_update_xaxes(fig4)
    fig4.update_layout(scene = dict(
                    xaxis_title=fig4_xlab,
                    yaxis_title="Inscriptions",
                    zaxis_title=fig4_zlab))
    return fig3, fig4
