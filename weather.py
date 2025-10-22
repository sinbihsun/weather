import requests
import json

# Open-Meteo API endpoint
url = "https://api.open-meteo.com/v1/forecast"

# 요청할 파라미터 (서울 기준: 위도 37.5665, 경도 126.9780)
params = {
    "latitude": 37.5665,
    "longitude": 126.9780,
    "hourly": "temperature_2m",  # 시간별 2m 높이의 기온
    "timezone": "Asia/Seoul"     # 한국 시간대 설정
}

# API 요청
response = requests.get(url, params=params)

# 응답 데이터(JSON) 파싱
data = response.json()

# 결과 출력
print(json.dumps(data, indent=2, ensure_ascii=False))

# 예시로 첫 5개의 시간별 기온 출력
print("\n=== 첫 5개의 시간별 기온 데이터 ===")
for time, temp in zip(data["hourly"]["time"][:5], data["hourly"]["temperature_2m"][:5]):
    print(f"{time} → {temp}℃")
