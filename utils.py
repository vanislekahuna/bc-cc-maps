import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut

def geocode_address(street, city, province, postal_code):
    """Geocode an address using Nominatim"""
    geolocator = Nominatim(user_agent="childcare_finder")
    address = f"{street}, {city}, {province} {postal_code}"
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        return None

def calculate_distances(user_lat, user_lon, facilities_df):
    """Calculate distances from user location to all facilities"""
    facilities_df['distance'] = facilities_df.apply(
        lambda row: geodesic((user_lat, user_lon), 
                           (row['latitude'], row['longitude'])).kilometers,
        axis=1
    )
    return facilities_df

def filter_facilities(df, max_distance, selected_services=None):
    """Filter facilities based on distance and services"""
    filtered_df = df[df['distance'] <= max_distance].copy()
    if selected_services:
        filtered_df = filtered_df[
            filtered_df['services'].apply(
                lambda x: any(service in x for service in selected_services)
            )
        ]
    return filtered_df