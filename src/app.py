import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
from utils import geocode_address, process_geodf, calculate_distances

# Load data
df = pd.read_csv('data/synth_data.csv')

# Page config
st.set_page_config(layout="wide", page_title="Childcare Facility Finder")
st.title("Childcare Facility Finder")

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    street = st.text_input("Street Address")
    city = st.text_input("City")
    
with col2:
    province = st.text_input("Province", value="BC")
    postal_code = st.text_input("Postal Code")

# Radius and services selection
col3, col4 = st.columns(2)

with col3:
    radius = st.selectbox(
        "Search Radius",
        options=[5, 10, 20],
        format_func=lambda x: f"{x} km"
    )

with col4:
    available_services = ['U36', '30SA', 'Family', 'Preschool']
    services = st.multiselect(
        "Filter by Services",
        options=available_services
    )

# Search button
if st.button("Search"):
    if street and city and province:
        # Geocode user address
        user_lat, user_lon = geocode_address(street, city, province, postal_code)
        
        try:            
            # Process the input DataFrame
            processed_df = process_geodf(df, "latitude", "longitude")

            # Calculate distances and filter facilities
            df_with_distances = calculate_distances(user_lat, user_lon, processed_df)
            filtered_df = df_with_distances[df_with_distances["distance_km"] <= radius]

            ### Script Check ###
            print(f"Found at least one site nearby the user: \n")
            print(filtered_df.head(1)[["facility_name", "address", "city", "distance_km", "U36", "30SA", "Family", "Preschool", "total_spaces"]])
            
            # Create two columns for map and results
            map_col, results_col = st.columns([2, 1])
            
            with map_col:
                # Create map centered on user location
                childcare_map = folium.Map(location=[user_lat, user_lon], zoom_start=12)
                
                # Add user marker
                folium.Marker(
                    [user_lat, user_lon],
                    popup="Your Location",
                    icon=folium.Icon(color='red')
                ).add_to(childcare_map)
                
                # Add facility markers
                for _, row in filtered_df.iterrows():
                    folium.Marker(
                        [row['latitude'], row['longitude']],
                        popup=row['facility_name'],
                        icon=folium.Icon(color='blue')
                    ).add_to(childcare_map)
                
                # Add radius circle
                folium.Circle(
                    [user_lat, user_lon],
                    radius=radius * 1000,  # Convert km to meters
                    color='red',
                    fill=True,
                    opacity=0.2
                ).add_to(childcare_map)
                
                folium_static(childcare_map)
            
            with results_col:
                st.write(f"Found {len(filtered_df)} facilities within {radius}km")
                
                # Sorting options
                sort_by = st.selectbox(
                    "Sort by",
                    options=["Distance", "Total Spaces"]
                )
                
                if sort_by == "Distance":
                    filtered_df = filtered_df.sort_values('distance_km')
                else:
                    filtered_df = filtered_df.sort_values('total_spaces', ascending=False)
                
                # Display results with pagination
                items_per_page = 5
                pages = len(filtered_df) // items_per_page + (1 if len(filtered_df) % items_per_page else 0)
                
                if pages > 0:
                    page = st.selectbox("Page", range(1, pages + 1))
                    start_idx = (page - 1) * items_per_page
                    end_idx = min(start_idx + items_per_page, len(filtered_df))
                    
                    for _, row in filtered_df.iloc[start_idx:end_idx].iterrows():
                        st.write("---")
                        st.write(f"**{row['facility_name']}**")
                        st.write(f"Distance: {row['distance_km']:.1f} km")
                        st.write(f"Address: {row['address']}, {row['city']}, BC {row['postal_code']}")
                        st.write(f"Total Spaces: {row['total_spaces']}")
                
        except Exception as e:
            st.error(f"Unable to locate the provided address {street}, {city}, {province}. Error in {e}")
    else:
        st.error("Please fill in all address fields.")