import dash_core_components as dcc
import dash_html_components as html

def top_reviews():
    return html.Div(
        children=[
            # Subheading
            html.Div(
                children=[
                    html.P("Top Reviews")
                ],
                style={ # Using inline css instead of heading font to manage spacing
                    "fontSize": "large",
                    "fontWeight": "bold",
                }
            ),
            # Tab bar to toggle pos/neg
            dcc.Tabs(
                children=[
                    dcc.Tab(
                        label="Positive Reviews",
                        value='pos'
                    ),
                    dcc.Tab(
                        label="Negative Reviews",
                        value='neg'
                    )
                ],
                id='review_type',
                value='pos'
            ),
            html.Div(id='reviews'),
        ],
        className="component-vertical"
    )