import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from sensor_data_module import add_distance_velocity

url = "https://raw.githubusercontent.com/SmallFluffyTail/analysisdata/main/Location.csv"

df = pd.read_csv(url)

# Check your actual column names — adjust these to match your CSV
# Common Phyphox column names:
df = add_distance_velocity(df, lat_col='Latitude (°)', lon_col='Longitude (°)', time_col='Time (s)')

st.title('My journey to home')

st.write("Average speed:", df['velocity_mps'].mean(), 'm/s')
st.write("Total distance:", df['total_distance'].max() / 1000, 'km')

st.line_chart(df, x='Time (s)', y='total_distance', y_label='Distance (m)', x_label='Time (s)')

start_lat = df['Latitude (°)'].mean()
start_long = df['Longitude (°)'].mean()
map = folium.Map(location=[start_lat, start_long], zoom_start=14)
folium.PolyLine(df[['Latitude (°)', 'Longitude (°)']], color='blue', weight=3.5, opacity=1).add_to(map)

st_map = st_folium(map, width=900, height=650)