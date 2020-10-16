import base64
from dash.dependencies import Input, Output, State
import dash_html_components as html
from io import BytesIO
import nltk
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

df = pd.read_csv('dashboard_data.csv', low_memory=False)

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
        if value:
            reviews = df.loc[df['asin'] == value]
            return round(reviews['overall'].mean(), 2), len(reviews.index)
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
        top_reviews = []
        reviews = df.loc[df['asin'] == product]
        if product:
            if review_type == 'pos':
                reviews = reviews.loc[df['sentiment'] > 0]
            else:
                reviews = reviews.loc[df['sentiment'] < 1]
            
            ranked_reviews = reviews.sort_values(by=['prob1'], ascending=False).head(5)
            for ind in ranked_reviews.index:
                top_reviews.append(
                    create_review(
                        ranked_reviews['summary'][ind],
                        ranked_reviews['overall'][ind],
                        ranked_reviews['reviewText'][ind],
                        ranked_reviews['style'][ind]
                    )
                )
            response.append(top_reviews)
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
                        html.Div('Rating: ' + str(rating)),
                        html.Div('Review Text: ' + str(review_text)),
                        html.Div('Style: ' + str(style)),
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
        reviews = df.loc[df['asin'] == product]
        if product:
            if keyword_type == 'pos':
                reviews = reviews.loc[df['sentiment'] > 0]
            else:
                reviews = reviews.loc[df['sentiment'] < 1]
            
            text = ' '.join(reviews['reviewText'])
            if not text:
                return html.P('N/A'), ''
            else:
                tokens = nltk.word_tokenize(text)
                tags = nltk.pos_tag(tokens)
                keywords = [word for word, pos in tags if (pos == 'JJ' or pos == 'JJR' or pos == 'JJS' or pos == 'RBS')]

                generate_wordcloud(' '.join(keywords)).save(img, format='PNG')
                return '', 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
        else:
            return html.P('N/A'), ''
    
    def generate_wordcloud(words):
        return WordCloud(width = 926, height = 200, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(words).to_image()