import pandas as pd
from geopy.distance import great_circle
from datetime import datetime

file_path = 'sample_data.csv'
data = pd.read_csv(file_path)

print(data.head())

def haversine_distance(lat1, lon1, lat2, lon2):
    return great_circle((lat1, lon1), (lat2, lon2)).meters

lat1, lon1 = 52.2296756, 21.0122287
lat2, lon2 = 41.8919300, 12.5113300
distance = haversine_distance(lat1, lon1, lat2, lon2)
print(f"Distance: {distance} meters")

data['timestamp'] = pd.to_datetime(data['timestamp'])

distance_threshold = 1000

proximity_events = []

for i, row1 in data.iterrows():
    for j, row2 in data.iterrows():
        if i != j and row1['mmsi'] != row2['mmsi']:
            distance = haversine_distance(row1['lat'], row1['lon'], row2['lat'], row2['lon'])
            if distance <= distance_threshold:
                proximity_events.append({
                    'mmsi': row1['mmsi'],
                    'vessel_proximity': row2['mmsi'],
                    'timestamp': row1['timestamp']
                })

print("Data shape:", data.shape)
proximity_df = pd.DataFrame(proximity_events)
print(proximity_df)

proximity_df.to_csv('proximity_events.csv', index=False)
