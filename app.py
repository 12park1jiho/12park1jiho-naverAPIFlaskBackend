# app.py
from flask import Flask
from flask_cors import CORS
from models import initialize_app
from routes import predict_trend, recommend_products, search_shopping

app = Flask(__name__)
CORS(app)

trend_model = None

@app.route('/predict_trend', methods=['GET'])
def trend_route():
    return predict_trend(trend_model)

@app.route('/recommend_products', methods=['POST'])
def recommend_route():
    return recommend_products()

@app.route('/search_shopping', methods=['POST'])
def shopping_route():
    return search_shopping()

if __name__ == '__main__':
    print("Main block executed")
    trend_model = initialize_app(trend_model)
    app.run(debug=True, host='0.0.0.0')