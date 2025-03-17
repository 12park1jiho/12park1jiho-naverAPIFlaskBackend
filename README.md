# Naver API Flask Application

## 📌 프로젝트 개요
이 프로젝트는 Flask를 기반으로 네이버 API를 활용하여 트렌드 예측, 상품 추천, 쇼핑 검색 기능을 제공하는 웹 애플리케이션입니다. 또한, JWT 기반의 로그인 기능을 포함하고 있어 인증된 사용자만 특정 API를 사용할 수 있도록 구성되었습니다.

## 🚀 주요 기능
- **트렌드 예측** (`/predict_trend`): 네이버 데이터랩 API를 활용하여 검색 트렌드를 예측
- **상품 추천** (`/recommend_products`): SVD 추천 알고리즘을 사용하여 개인화된 상품 추천
- **쇼핑 검색** (`/search_shopping`): 네이버 쇼핑 API를 통해 키워드 기반 상품 검색
- **회원가입 및 로그인** (`/auth/register`, `/auth/login`): JWT 기반 사용자 인증

## 🛠️ 설치 방법
### 1️⃣ 필수 패키지 설치
```bash
pip install Flask Flask-Cors Flask-JWT-Extended Flask-SQLAlchemy bcrypt requests pandas statsmodels surprise
```

### 2️⃣ 프로젝트 클론 및 실행
```bash
git clone https://github.com/your-repo/naverAPI.git
cd naverAPI
python app.py
```

## 🔑 API 사용 방법
### 1️⃣ 회원가입
```http
POST /auth/register
Content-Type: application/json
{
  "email": "test@example.com",
  "password": "1234"
}
```

### 2️⃣ 로그인
```http
POST /auth/login
Content-Type: application/json
{
  "email": "test@example.com",
  "password": "1234"
}
```
응답 예시:
```json
{
  "access_token": "your_jwt_token"
}
```

### 3️⃣ 트렌드 예측 (보호된 API)
```http
GET /predict_trend
Authorization: Bearer <ACCESS_TOKEN>
```

### 4️⃣ 상품 추천 (보호된 API)
```http
POST /recommend_products
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
{
  "uid": 1,
  "data": [ ... ]
}
```

### 5️⃣ 쇼핑 검색
```http
POST /search_shopping
Content-Type: application/json
{
  "search_term": "노트북"
}
```

## ⚠️ 보안 주의사항
- `CLIENT_ID` 및 `CLIENT_SECRET`은 코드에서 직접 사용하지 않고 `.env` 파일이나 환경 변수에서 관리하세요.
- `debug=True` 설정을 프로덕션 환경에서는 사용하지 마세요.

## 📄 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.
