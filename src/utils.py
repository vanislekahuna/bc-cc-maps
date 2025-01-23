import os
import googlemaps
import pandas as pd
from geopy.distance import geodesic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEOCODER_KEY = os.environ["geocoder_key"]

def geocode_address(street, city, province, postal_code):
    """Geocode an address using Google Maps"""
    gmaps = googlemaps.Client(key=GEOCODER_KEY)
    address = f"{street}, {city}, {province} {postal_code}"

    print(f"Geocoding the address at {address}....")

    try:
        location = gmaps.geocode(address)
        latitude = location[0]['geometry']['location']['lat']
        longitude = location[0]['geometry']['location']['lng']

        print(f"Success! The coordinates for {address} are the following latitude and longitude coordinates: ({latitude}, {longitude})")
            
        return latitude, longitude          

    except Exception as e:
        print(f"The following location was not found: {address}")
        print(e)


def process_geodf(df, lat_col, lon_col):
  """
  A function to process the reference df and remove any null or non-float values.
  
  Parameters:
  df: DataFrame
  lat_col: str
  lon_col: str
  
  Returns:
  df: DataFrame
  """

  df = df.dropna(axis=0, subset=[lat_col, lon_col])
  df[lat_col] = df[lat_col].astype(float)
  df[lon_col] = df[lon_col].astype(float)

  return df


def calculate_distances(user_lat, user_lon, facilities_df, round_by=2, col_name="distance_km"):
    """
    Calculate distances from user location to all facilities
    
    Parameters:
    df: DataFrame
    lat_col: str
    lon_col: str
    
    Returns:
    df: DataFrame
    """
    
    facilities_df["distance_km"] = facilities_df.apply(
        lambda row: round(
            geodesic(
                (user_lat, user_lon), 
                (row["latitude"], row["longitude"])
            ).kilometers,
            round_by
        ),
        axis=1
    )

    print(f"The distance calculations yielded the following results: \n\n \
    {facilities_df[col_name].head(3)}")

    return facilities_df