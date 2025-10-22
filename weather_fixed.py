# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Open-Meteo Interactive Weather Dashboard", layout="wide")

# ---- 앱 제목 ----
st.title("🌦️ Open-Meteo Interactive Weather Dashboard")
st.write("지도를 클릭하면 해당 지역의 시간별 기온 데이터를 불러옵니다.")

# ---- 지도 표시 ----
st.subheader("1️⃣ 지역 선택 (지도를 클릭하세요)")
m = folium.Map(location=[37.5665, 126.9780], zoom_start=5, control_scale=True)
folium.LatLngPopup().add_to(m)

ret = st_folium(m, height=520)

# ---- 지도 클릭 이벤트 처리 ----
if ret and ret.get("last_clicked"):
    lat = ret["last_clicked"]["lat"]
    lon = ret["last_clicked"]["lng"]
    st.success(f"📍 선택된 위치: 위도 {lat:.4f}, 경도 {lon:.4f}")

    # ---- Open-Meteo API 요청 ----
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        hourly = data.get("hourly", {})
        times = hourly.get("time")
        temps = hourly.get("temperature_2m")

        if not times or not temps:
            st.error("API 응답에 시간/기온 데이터가 없습니다.")
        else:
            # ---- JSON → DataFrame 변환 ----
            df = pd.DataFrame({"time": times, "temperature (°C)": temps})
            df["time"] = pd.to_datetime(df["time"])

            # ---- 시각화 ----
            st.subheader("2️⃣ 시간별 기온 변화 그래프")
            fig = px.line(
                df,
                x="time",
                y="temperature (°C)",
                title=f"{lat:.2f}, {lon:.2f} 지역의 시간별 기온",
                labels={"time": "시간", "temperature (°C)": "기온(℃)"},
            )
            st.plotly_chart(fig, use_container_width=True)

            # ---- 표로 보기 ----
            st.subheader("3️⃣ 원시 데이터 보기 (최근 24시간)")
            st.dataframe(df.head(24), use_container_width=True)

    except requests.exceptions.RequestException as e:
        st.error(f"데이터 요청 중 네트워크 오류 발생: {e}")
    except ValueError as e:
        st.error(f"응답 파싱 오류: {e}")
    except Exception as e:
        st.error(f"예기치 못한 오류: {e}")
else:
    st.info("지도를 클릭하면 해당 지역의 날씨 데이터를 가져옵니다.")
