import streamlit as st
import folium
from streamlit_folium import folium_static  # Import folium_static
from geopy.geocoders import Nominatim
import requests

# Google Maps API Key
GOOGLE_MAPS_API_KEY = 'AIzaSyBJ_XlxltqRMHEaqUxKak6LkIb0jt4qRWM'

# Function to get nearby fuel stations
def get_nearby_fuel_stations(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&type=gas_station&key={GOOGLE_MAPS_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            st.error("Failed to fetch nearby fuel stations. Please try again later.")
            return []
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []

# Streamlit App
st.title('Fuel Stations and Parking Reservation')

# Get user location
geolocator = Nominatim(user_agent="geoapiExercises")
location = st.text_input('Enter your location (e.g., "New York, USA")', 'New York, USA')
user_location = geolocator.geocode(location)

if user_location:
    lat, lon = user_location.latitude, user_location.longitude
    st.write(f"Latitude: {lat}, Longitude: {lon}")

    # Display map with fuel stations
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], tooltip="Your Location").add_to(m)

    fuel_stations = get_nearby_fuel_stations(lat, lon)
    for station in fuel_stations:
        station_location = station['geometry']['location']
        folium.Marker(
            [station_location['lat'], station_location['lng']],
            tooltip=station['name']
        ).add_to(m)

    st.write("Nearest Fuel Stations:")
    st.markdown(folium_static(m))  # Use folium_static to display the map
