import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---- �� ���� ----
st.title("??? Open-Meteo Interactive Weather Dashboard")
st.write("�������� ��ġ�� Ŭ���ϸ� �ش� ������ �ð��� ��� �����͸� �ҷ��ɴϴ�.")

# ---- ���� ǥ�� ----
st.subheader("1?? ���� ���� (������ Ŭ���ϼ���)")
clicked_point = st.map(on_click=True)

# ---- ���� Ŭ�� �̺�Ʈ ó�� ----
if clicked_point is not None:
    lat = clicked_point["lat"]
    lon = clicked_point["lon"]

    st.success(f"?? ���õ� ��ġ: ���� {lat:.4f}, �浵 {lon:.4f}")

    # ---- Open-Meteo API ��û ----
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

        # ---- JSON �� DataFrame ��ȯ ----
        df = pd.DataFrame({
            "time": data["hourly"]["time"],
            "temperature (��C)": data["hourly"]["temperature_2m"]
        })

        # ---- �ð�ȭ ----
        st.subheader("2?? �ð��� ��� ��ȭ �׷���")
        fig = px.line(df, x="time", y="temperature (��C)",
                      title=f"{lat:.2f}, {lon:.2f} ������ �ð��� ���",
                      labels={"time": "�ð�", "temperature (��C)": "���(��)"})
        st.plotly_chart(fig)

        # ---- ǥ�� ���� ----
        st.subheader("3?? ���� ������ ����")
        st.dataframe(df.head(24))

    except Exception as e:
        st.error(f"������ ��û �� ���� �߻�: {e}")

else:
    st.info("������ Ŭ���ϸ� �ش� ������ ���� �����͸� �����ɴϴ�.")
