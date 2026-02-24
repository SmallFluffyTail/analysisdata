import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from sensor_data_module import add_distance_velocity, step_count

# Load data
loc_url = "https://raw.githubusercontent.com/SmallFluffyTail/analysisdata/main/Location.csv"
acc_url = "https://raw.githubusercontent.com/SmallFluffyTail/analysisdata/main/Linear%20Acceleration.csv"

df_loc = pd.read_csv(loc_url)
df_acc = pd.read_csv(acc_url)

# Calculate distance and velocity from GPS data
df_loc = add_distance_velocity(df_loc, lat_col='Latitude (°)', lon_col='Longitude (°)', time_col='Time (s)')

# Calculate acceleration magnitude for step counting
df_acc['acc'] = np.sqrt(
    df_acc['Linear Acceleration x (m/s^2)']**2 +
    df_acc['Linear Acceleration y (m/s^2)']**2 +
    df_acc['Linear Acceleration z (m/s^2)']**2
)
df_acc = df_acc.rename(columns={'Time (s)': 'Time'})

# Calculate step count
steps = step_count(df_acc, acc_col='acc', time_col='Time')

st.title('Topi Heinämäki')

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Average Speed", f"{df_loc['velocity_mps'].mean():.2f} m/s")
col2.metric("Total Distance", f"{df_loc['total_distance'].max() / 1000:.2f} km")
col3.metric("Step Count", f"{int(steps)}")

# Distance over time chart
st.subheader("Distance over time")
st.line_chart(df_loc, x='Time (s)', y='total_distance', y_label='Distance (m)', x_label='Time (s)')

# Speed over time chart
st.subheader("Speed over time")
st.line_chart(df_loc, x='Time (s)', y='velocity_mps', y_label='Speed (m/s)', x_label='Time (s)')

# Map
st.subheader("Route on map")
start_lat = df_loc['Latitude (°)'].mean()
start_long = df_loc['Longitude (°)'].mean()
map = folium.Map(location=[start_lat, start_long], zoom_start=14)
folium.PolyLine(df_loc[['Latitude (°)', 'Longitude (°)']], color='blue', weight=3.5, opacity=1).add_to(map)
st_map = st_folium(map, width=900, height=650)