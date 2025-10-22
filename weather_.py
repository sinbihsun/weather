import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---- 앱 제목 ----
st.title("??? Open-Meteo Interactive Weather Dashboard")
st.write("지도에서 위치를 클릭하면 해당 지역의 시간별 기온 데이터를 불러옵니다.")

# ---- 지도 표시 ----
st.subheader("1?? 지역 선택 (지도를 클릭하세요)")
clicked_point = st.map(on_click=True)

# ---- 지도 클릭 이벤트 처리 ----
if clicked_point is not None:
    lat = clicked_point["lat"]
    lon = clicked_point["lon"]

    st.success(f"?? 선택된 위치: 위도 {lat:.4f}, 경도 {lon:.4f}")

    # ---- Open-Meteo API 요청 ----
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # ---- JSON → DataFrame 변환 ----
        df = pd.DataFrame({
            "time": data["hourly"]["time"],
            "temperature (°C)": data["hourly"]["temperature_2m"]
        })

        # ---- 시각화 ----
        st.subheader("2?? 시간별 기온 변화 그래프")
        fig = px.line(df, x="time", y="temperature (°C)",
                      title=f"{lat:.2f}, {lon:.2f} 지역의 시간별 기온",
                      labels={"time": "시간", "temperature (°C)": "기온(℃)"})
        st.plotly_chart(fig)

        # ---- 표로 보기 ----
        st.subheader("3?? 원시 데이터 보기")
        st.dataframe(df.head(24))

    except Exception as e:
        st.error(f"데이터 요청 중 오류 발생: {e}")

else:
    st.info("지도를 클릭하면 해당 지역의 날씨 데이터를 가져옵니다.")
