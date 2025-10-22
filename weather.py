import requests
import json

# Open-Meteo API endpoint
url = "https://api.open-meteo.com/v1/forecast"

# ��û�� �Ķ���� (���� ����: ���� 37.5665, �浵 126.9780)
params = {
    "latitude": 37.5665,
    "longitude": 126.9780,
    "hourly": "temperature_2m",  # �ð��� 2m ������ ���
    "timezone": "Asia/Seoul"     # �ѱ� �ð��� ����
}

# API ��û
response = requests.get(url, params=params)

# ���� ������(JSON) �Ľ�
data = response.json()

# ��� ���
print(json.dumps(data, indent=2, ensure_ascii=False))

# ���÷� ù 5���� �ð��� ��� ���
print("\n=== ù 5���� �ð��� ��� ������ ===")
for time, temp in zip(data["hourly"]["time"][:5], data["hourly"]["temperature_2m"][:5]):
    print(f"{time} �� {temp}��")
