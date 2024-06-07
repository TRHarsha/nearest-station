import streamlit as st
from geopy.distance import geodesic
from geopy.geocoders import OpenCage
import folium
from streamlit_folium import folium_static
import json

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Function to get coordinates using OpenCage
def get_coordinates(place_name):
    geolocator = OpenCage(api_key=st.secrets["OPENCAGE_API_KEY"])
    location = geolocator.geocode(place_name)
    if location:
        return location.latitude, location.longitude
    return None

# Function to find nearest power or fuel station
def find_nearest_station(lat, lon, station_type='fuel'):
    min_distance = float('inf')
    nearest_station = None
    user_location = (lat, lon)
    
    for station in data["stations"]:
        if station["type"] == station_type:
            station_location = (station["lat"], station["lon"])
            distance = geodesic(user_location, station_location).kilometers
            if distance < min_distance:
                min_distance = distance
                nearest_station = station

    return nearest_station, min_distance

# Streamlit UI
st.title("Nearest Power or Fuel Station Finder")

st.markdown("""
    Enter a place name to find the nearest power or fuel station.
""")

place = st.text_input("Enter a place name")

if st.button("Find Nearest Station"):
    coordinates = get_coordinates(place)
    if coordinates:
        lat, lon = coordinates
        station_type = st.radio("Select station type", ('fuel', 'power'))
        nearest_station, distance = find_nearest_station(lat, lon, station_type)
        
        if nearest_station:
            st.write(f"The nearest {station_type} station is {nearest_station['name']} located at ({nearest_station['lat']}, {nearest_station['lon']}) which is {distance:.2f} km away.")
            st.write(f"Address: {nearest_station['address']}")
            st.write(f"Phone: {nearest_station['phone'] if nearest_station['phone'] else 'N/A'}")
            
            # Create a map
            map_center = [lat, lon]
            m = folium.Map(location=map_center, zoom_start=10)

            # Add user location marker
            folium.Marker(
                location=[lat, lon],
                popup="Your Location",
                icon=folium.Icon(color="blue")
            ).add_to(m)

            # Add nearest station marker
            folium.Marker(
                location=[nearest_station['lat'], nearest_station['lon']],
                popup=f"Nearest {station_type.capitalize()} Station: {nearest_station['name']}",
                icon=folium.Icon(color="red")
            ).add_to(m)

            folium_static(m)
        else:
            st.write(f"No {station_type} station found within 50 km of {place}.")
    else:
        st.write("Place not found. Please enter a valid place name.")
        st.write(f"Available places: {', '.join(data['places'].keys())}")
