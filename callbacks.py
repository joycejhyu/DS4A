import base64
from dash.dependencies import Input, Output, State
import dash_html_components as html
from io import BytesIO
from wordcloud import WordCloud, STOPWORDS

def register_callbacks(app):
    # Product Selection
    @app.callback(
        [
            Output('rating_text', 'children'),
            Output('quantity_text', 'children'),
        ],
        [
            Input('product_list','value')
        ]
    )
    def update_product_data(value):
        # TODO: Update to use real data
        if value == 'mascara':
            return 1, 2
        elif value == 'lipstick':
            return 3, 4
        else:
            return 'N/A', 'N/A'

    # Show Top Reviews
    @app.callback(
        [
            Output('reviews', 'children')
        ],
        [
            Input('product_list', 'value'),
            Input('review_type', 'value')
        ]
    )
    def update_product_reviews(product, review_type):
        response = []
        # TODO: Update to use real data instead of hardcoded placeholders
        if product == 'mascara':
            if review_type == 'pos':
                response.append(
                        [
                            create_review('Pos Review 1 for mascara', '4.3', 'test 1', 'N/A'),
                            create_review('Pos Review 2 for mascara', '4.5', 'test 2', 'N/A'),
                            create_review('Pos Review 3 for mascara', '4.6', 'test 3', 'N/A'),
                            create_review('Pos Review 4 for mascara', '4.7', 'test 4', 'N/A'),
                            create_review('Pos Review 5 for mascara', '4.8', 'test 5', 'N/A'),
                        ]
                )
            else:
                response.append(
                    [
                        create_review('Neg Review 1 for mascara', '2.3', 'test 6', 'N/A'),
                        create_review('Neg Review 2 for mascara', '1.5', 'test 7', 'N/A'),
                    ]
                )
        elif product == 'lipstick':
            if review_type == 'pos':
                response.append(
                    [
                        create_review('Pos Review 1 for lipstick', '4.3', 'test 8', 'N/A'),
                        create_review('Pos Review 2 for lipstick', '4.5', 'test 9', 'N/A'),
                    ]
                )
            else:
                response.append(
                    [
                        create_review('Neg Review 1 for lipstick', '2.3', 'test 10', 'N/A'),
                        create_review('Neg Review 2 for lipstick', '1.5', 'test 11', 'N/A'),
                    ]
                )
        else:
            response.append([html.P('N/A')])
        
        return response
    
    def create_review(summary, rating, review_text, style):
        return html.Details(
            [
                html.Summary(
                    children=summary, 
                    style={
                        "marginBottom": "12px",
                        "marginTop": "12px"
                    }
                ),
                html.Div(
                    [
                        html.Div('Rating: ' + rating),
                        html.Div('Review Text: ' + review_text),
                        html.Div('Style: ' + style),
                    ],
                    className="review"
                )
            ],
            open=False
        )

    # Show Keyword Insights
    stopwords = set(STOPWORDS)

    @app.callback(
        [
            Output('keywords_label', 'children'),
            Output('keywords_img', 'src')
        ],
        [
            Input('product_list', 'value'),
            Input('keyword_type', 'value')
        ]
    )
    def update_product_keywords(product, keyword_type):
        img = BytesIO()
        # TODO: Update to use real data instead of hardcoded placeholders
        words = 'I am absolutely amazed by this product. I have very dry sensitive skin, large pours that tend to get dirty. I mixed with apple cider vinegar and applied with a paint brush. I waited 10 minutes as I have sensitive skin, while feeling it pulsate and deep clean. I then wiped off with a warm wet cloth. As the container says your face will be red after which is fine as it feels very refreshed and clean. The red will go away within 30 minutes. I did this before bed. The results are amazing, the big pours are completely cleaned out no dirt what so ever. I applied my daily facial oils and moisturizers and from just one use I already see results. Because of moisturizing after it did not dry my face out, I’m sure if you don’t it may cause dryness. I also have tried this product on my pits with apple cider vinegar. I wanted to see if it would get rid of the body odour so I don’t have to wear deodorant. I left it on for 10 minutes and wiped off. I have gone 2 full days with no deodorant and no odour has occurred to me!! I will continue to use this product once a week as the results really do come out how I expected if not better.'
        if product == 'mascara':
            if keyword_type == 'pos':
                generate_wordcloud(words).save(img, format='PNG')
                return '', 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
            else:
                generate_wordcloud(words).save(img, format='PNG')
                return '', 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
        elif product == 'lipstick':
            if keyword_type == 'pos':
                generate_wordcloud(words).save(img, format='PNG')
                return '', 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
            else:
                generate_wordcloud(words).save(img, format='PNG')
                return '', 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
        else:
            return html.P('N/A'), ''
    
    def generate_wordcloud(words):
        return WordCloud(width = 926, height = 200, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(words).to_image()