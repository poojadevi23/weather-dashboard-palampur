import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
st.set_page_config(page_title="Palampur Weather Dashboard", layout="wide")

API_KEY = "9d9c6e744e4244ae9e2163407262903"
CITY = "Palampur"
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1e1e2f, #2c3e50);
        color: white;
    }
    .card {
        background-color: #262730;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

def get_current_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=yes"
    return requests.get(url).json()

def get_forecast():
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=3&aqi=yes"
    return requests.get(url).json()

weather = get_current_weather()
forecast = get_forecast()

st.title("🌦️ Palampur Live Weather Dashboard")

if st.button("Refresh Data"):
    st.rerun()

st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if "current" in weather:
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"<div class='card'><h3>🌡️ Temperature</h3><h1>{weather['current']['temp_c']}°C</h1></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h3>💧 Humidity</h3><h1>{weather['current']['humidity']}%</h1></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><h3>🌬️ Wind</h3><h1>{weather['current']['wind_kph']} kph</h1></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='card'><h3>☁️ Condition</h3><h1>{weather['current']['condition']['text']}</h1></div>", unsafe_allow_html=True)

st.markdown("---")

forecast_data = []
for day in forecast["forecast"]["forecastday"]:
    for hour in day["hour"]:
        forecast_data.append({
            "time": hour["time"],
            "temp": hour["temp_c"],
            "humidity": hour["humidity"]
        })

df = pd.DataFrame(forecast_data)

fig = px.line(df, x="time", y="temp", title="Temperature Forecast (Next 3 Days)")
st.plotly_chart(fig, use_container_width=True)

fig2 = px.bar(df, x="time", y="humidity", title="Humidity Trend")
st.plotly_chart(fig2, use_container_width=True)

if "current" in weather and "air_quality" in weather["current"]:
    aqi = weather["current"]["air_quality"]["pm2_5"]

    st.subheader("Air Quality Insights")

    col1, col2 = st.columns(2)

    col1.metric("PM2.5 Level", round(aqi, 2))

    if aqi <= 12:
        col2.success("Air quality is Good")
    elif aqi <= 35:
        col2.warning("Air quality is Moderate")
    else:
        col2.error("Air quality is Poor")

st.markdown("---")

st.subheader("Smart Insights")

if "current" in weather:
    temp = weather["current"]["temp_c"]
    humidity = weather["current"]["humidity"]

    if temp > 30:
        st.warning("High temperature. Stay hydrated and avoid sun exposure.")
    elif temp < 10:
        st.info("Cold weather. Wear warm clothes.")

    if humidity > 80:
        st.warning("High humidity. Might feel uncomfortable.")
    else:
        st.success("Weather conditions are comfortable.")
