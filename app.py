import dash
import dash_core_components as dcc
import dash_html_components as html
from callbacks import register_callbacks
from components.summary_info import *
from components.reviews import *
from components.keywords import *

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        }
    ]
)

# TODO: replace placeholder data
product_list = [ 
    {'label': 'Mascara', 'value': 'mascara'},
    {'label': 'Lipstick', 'value': 'lipstick'},
]

app.layout = html.Div(
    [
        # app bar
        html.Div(
            children=[
                # logo
                html.Div(
                    children=[    
                        html.Img(
                            src=app.get_asset_url("ds4a-wide.svg")
                        )
                    ],
                    style={
                        "height": "auto",
                        "width": "20%",
                    }
                ),
                html.Div(
                    html.H2("CleaReview")
                ),
                # user
                html.Div(
                    children=[
                        html.Img(
                            src=app.get_asset_url("user.svg"),
                            style={
                                "height": "40px",
                            }
                        ),
                        html.Div(
                            html.H6("Jane Doe")
                        )
                    ],
                    className="user"
                )
            ],
            className="app-bar"
        ),
        # Dropdown
        html.Div(
            dcc.Dropdown(
                clearable=False,
                id='product_list',
                options=product_list,
                placeholder="Select a product"
            ),
            style={
                "margin": "12px 0px 8px",
            }
        ),
        # Components
        html.Div(
            summary_info(),
        ),
        html.Div(
            top_reviews(),
        ),
        html.Div(
            word_clouds(),
        )
    ]
)

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)