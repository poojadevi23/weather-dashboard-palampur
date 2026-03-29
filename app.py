import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Palampur Weather Dashboard", layout="wide")

API_KEY = "9d9c6e744e4244ae9e2163407262903"
CITY = "Palampur"

def get_current_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=yes"
    return requests.get(url).json()
def get_forecast():
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=3&aqi=yes&alerts=no"
    return requests.get(url).json()
weather = get_current_weather()
forecast = get_forecast()
st.title("Live Weather Dashboard - Palampur")
if st.button("Refresh Data"):
    st.rerun()
st.write("Last Updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
if "current" in weather:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperature (°C)", weather["current"]["temp_c"])
    col2.metric("Humidity (%)", weather["current"]["humidity"])
    col3.metric("Wind (kph)", weather["current"]["wind_kph"])
    col4.metric("Condition", weather["current"]["condition"]["text"])

st.markdown("---")
forecast_data = []
for day in forecast["forecast"]["forecastday"]:
    for hour in day["hour"]:
        forecast_data.append({
            "time": hour["time"],
            "temp": hour["temp_c"]
        })
df = pd.DataFrame(forecast_data)
fig = px.line(df, x="time", y="temp", title="Temperature Forecast (Next 3 Days)")
st.plotly_chart(fig, use_container_width=True)

if "current" in weather and "air_quality" in weather["current"]:
    aqi = weather["current"]["air_quality"]["pm2_5"]
    st.subheader("Air Quality (PM2.5)")
    st.metric("PM2.5 Level", round(aqi, 2))

    if aqi <= 12:
        st.success("Air quality is Good")
    elif aqi <= 35:
        st.warning("Air quality is Moderate")
    else:
        st.error("Air quality is Poor")
