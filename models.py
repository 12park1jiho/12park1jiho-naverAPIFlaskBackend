# models.py
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import requests
import datetime
import json

CLIENT_ID = "PnfJSQbzGHzV1Ngdefmm"
CLIENT_SECRET = "4ACw8JKmQ6"

# 트렌드 예측 모델 학습 (통합 검색어 트렌드 API 및 쇼핑인사이트 API)
def train_trend_model(trend_data, shopping_data):
    try:
        trend_df = pd.DataFrame(trend_data['results'][0]['data'])
        shopping_df = pd.DataFrame(shopping_data['results'][0]['data'])

        if trend_df.empty or shopping_df.empty:
            return None

        trend_df['period'] = pd.to_datetime(trend_df['period'])
        trend_df.set_index('period', inplace=True)
        trend_full_index = pd.date_range(start=trend_df.index.min(), end=trend_df.index.max(), freq='D')
        trend_df = trend_df.reindex(trend_full_index, fill_value=0)
        trend_df['ratio'] = pd.to_numeric(trend_df['ratio'])
        trend_df.rename(columns={'ratio': 'trend_ratio'}, inplace=True)

        shopping_df['period'] = pd.to_datetime(shopping_df['period'])
        shopping_df.set_index('period', inplace=True)
        shopping_full_index = pd.date_range(start=shopping_df.index.min(), end=shopping_df.index.max(), freq='D')
        shopping_df = shopping_df.reindex(shopping_full_index, fill_value=0)
        shopping_df['ratio'] = pd.to_numeric(shopping_df['ratio'])
        shopping_df.rename(columns={'ratio': 'shopping_ratio'}, inplace=True)

        merged_df = pd.merge(trend_df, shopping_df, left_index=True, right_index=True, how='outer').fillna(0)

        # SARIMAX 모델 사용
        model = SARIMAX(merged_df['trend_ratio'], exog=merged_df['shopping_ratio'], order=(5, 1, 0))
        model_fit = model.fit()
        return model_fit
    except Exception as e:
        print(f"Error during trend model training: {e}")
        return None

# 상품 추천 모델 학습 (예시)
def train_recommendation_model(user_data):
    try:
        if not user_data:
            return None
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(user_data, reader)
        trainset, testset = train_test_split(data, test_size=0.25)
        model = SVD()
        model.fit(trainset)
        return model
    except Exception as e:
        print(f"Error during recommendation model training: {e}")
        return None

def initialize_app(trend_model):
    if trend_model is None:
        today = datetime.date.today().strftime("%Y-%m-%d")
        start_date = (datetime.date.today() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
        trend_url = "https://openapi.naver.com/v1/datalab/search"
        shopping_url = "https://openapi.naver.com/v1/datalab/shopping/categories"
        trend_body = {
            "startDate": start_date,
            "endDate": today,
            "timeUnit": "date",
            "keywordGroups": [
                {"groupName": "오늘의 트렌드", "keywords": ["오늘의 트렌드", "인기 검색어"]},
            ],
            "device": "pc",
            "ages": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
            "gender": "m",
        }
        shopping_body = {
            "startDate": start_date,
            "endDate": today,
            "timeUnit": "date",
            "category": [{"name": "패션의류", "param": ["50000000"]}]
        }
        headers = {
            "X-Naver-Client-Id": CLIENT_ID,
            "X-Naver-Client-Secret": CLIENT_SECRET,
            "Content-Type": "application/json",
        }
        try:
            trend_response = requests.post(trend_url, headers=headers, json=trend_body)
            trend_response.raise_for_status()
            trend_data = trend_response.json()
            shopping_response = requests.post(shopping_url, headers=headers, json=shopping_body)
            shopping_response.raise_for_status()
            shopping_data = shopping_response.json()
            if trend_data["results"][0]["data"] and shopping_data["results"][0]["data"]:
                trend_model = train_trend_model(trend_data, shopping_data)
                if trend_model:
                    print("Trend model trained successfully.")
                else:
                    print("Failed to train trend model.")
            else:
                print("No data available from Naver API.")
            return trend_model
        except requests.exceptions.RequestException as e:
            print(f"Naver API error during initialization: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error during initialization: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during initialization: {e}")
    return trend_model