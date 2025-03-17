# routes.py
import pandas as pd
from flask import jsonify, request
import requests
import base64
from models import train_recommendation_model
CLIENT_ID = "PnfJSQbzGHzV1Ngdefmm"
CLIENT_SECRET = "4ACw8JKmQ6"

def predict_trend(trend_model):
    if trend_model:
        try:
            forecast = trend_model.forecast(steps=7)
            return jsonify({"forecast": forecast.tolist()})
        except Exception as e:
            return jsonify({"error": f"Error during prediction: {e}"}), 500
    else:
        return jsonify({"error": "Trend model not trained yet."}), 400

def recommend_products():
    try:
        user_data = request.get_json()
        model = train_recommendation_model(pd.DataFrame(user_data))
        if model:
            user_id = user_data[0]['uid']
            recommended_products = []
            for i in range(1, 10):
                prediction = model.predict(user_id, i)
                if prediction.est > 3:
                    recommended_products.append(i)
            return jsonify({"recommended_products": recommended_products})
        else:
            return jsonify({"error": "No data for product recommendation"}), 400
    except Exception as e:
        return jsonify({"error": f"Error during product recommendation: {e}"}), 500

def search_shopping():
    search_term = request.json['search_term']
    url = "https://openapi.naver.com/v1/search/shop?query=" + search_term
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    response = requests.get(url, headers=headers)
    print("API Response:", response.json())
    if 'items' in response.json():
        items = response.json()['items']
        for item in items:
            if item.get('image'):
                try:
                    image_response = requests.get(item['image'], stream=True)
                    image_response.raise_for_status()
                    encoded_image = base64.b64encode(image_response.content).decode('utf-8')
                    item['image_base64'] = encoded_image
                    del item['image']
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading image: {e}")
                    item['image_base64'] = None
        return jsonify({'items': items})
    else:
        return jsonify({'error': 'No items found'}), 404