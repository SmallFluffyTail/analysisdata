

import numpy as np
import pandas as pd

def add_distance_velocity(df, lat_col='latitude', lon_col='longitude', time_col='timestamp'):
    """
    Adds distance (meters) and velocity (m/s) columns to a DataFrame
    using the Haversine formula.
    """
    
    df = df.copy()
    df = df.sort_values(time_col)
    # Earth radius in meters
    R = 6371000  
    # Convert degrees to radians
    lat = np.radians(df[lat_col])
    lon = np.radians(df[lon_col])
    # Shift coordinates
    lat_prev = lat.shift(1)
    lon_prev = lon.shift(1)
    # Haversine formula
    dlat = lat - lat_prev
    dlon = lon - lon_prev
    a = np.sin(dlat / 2)**2 + np.cos(lat_prev) * np.cos(lat) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c  # meters
    df['distance_m'] = distance
    df['total_distance'] = np.cumsum(distance)
    # Time difference in seconds
    time_diff = df[time_col].diff()#.dt.total_seconds()
    # Velocity in m/s
    df['velocity_mps'] = df['distance_m'] / time_diff
    #Ignore outliers
    threshold = 5 * df['velocity_mps'].std()
    df.loc[df['velocity_mps'] > threshold,'velocity_mps'] = np.nan
    return df

def step_count(df, acc_col= 'acc', time_col = 'Time'):
    """
    Calculate the number of steps from acceleration data
    """
    signal = df[acc_col]
    t = df[time_col] #Time in seconds
    N = len(signal) #Number of samples
    dt = np.max(t)/N #Sampling interval

    #Fourier-analysis
    fourier = np.fft.fft(signal,N) #Fourier
    psd = fourier*np.conj(fourier)/N #PSD
    freq = np.fft.fftfreq(N,dt) #Freq
    L = np.arange(1,int(N/2)) #Remove negative 
    f_max = freq[L][psd[L] == np.max(psd[L])][0] 
    #T = 1/f_max #Askeleeseen kuluva aika, eli jaksonaika (oletettaen, että dominoiva taajuus on askeltaajuus)
    steps =  f_max*np.max(t) #Askelmäärä. Voi laskema myös np.max(t)/T
    return steps