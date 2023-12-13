from scripts.static_figures import static_fig
from dash import dcc, html

# Static Figures: Table of contents
static_fig_toc = [
    {comp_id: fig.layout.title.text for comp_id, fig in static_fig.items()}
]


####################################################################################################
# Custom functions
####################################################################################################
def static_graph_html_div(static_fig: dict, comp_id: list):
    """Generate html Div components by row"""
    width = f"{100/len(comp_id)}%"

    def get_dcc_graph(figure, comp_id, custom_width: str):
        """Generate dcc Graph components"""
        dcc_graph = dcc.Graph(id=comp_id, figure=figure, style={"width": custom_width})
        return dcc_graph

    graphs = [(k, v) for k, v in static_fig.items() if k in comp_id]
    dcc_graph_list = []
    for graph in graphs:
        comp_id, figure = graph
        dcc_graph_list += [
            get_dcc_graph(figure=figure, comp_id=comp_id, custom_width=width)
        ]
    html_div = html.Div(
        dcc_graph_list, style={"display": "flex", "flex-direction": "row"}
    )

    return html_div


####################################################################################################
# Static Figures: Generate html Div components by row
####################################################################################################

num_inscripts_and_ord_size_usage = static_graph_html_div(
    static_fig, comp_id=["static-fig-1", "static-fig-2"]
)

num_inscr_and_p_inscr_type = static_graph_html_div(
    static_fig, comp_id=["static-fig-3", "static-fig-4"]
)
