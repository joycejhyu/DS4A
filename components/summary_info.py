import dash_core_components as dcc
import dash_html_components as html

def summary_info():
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.P(id="rating_text"),
                    html.Div(
                        html.P("Average Rating"),
                        style={
                            "fontSize": "small",
                        }
                    )
                ],
                className="card",
            ),
            html.Div(
                children=[
                    html.P(id="quantity_text"), 
                    html.Div(
                        html.P("Total Reviews"),
                        style={
                            "fontSize": "small",
                        }
                    )
                ],
                className="card",
            ),
        ],
        className="component-horizontal",
    )