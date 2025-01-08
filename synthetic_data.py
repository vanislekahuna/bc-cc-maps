import pandas as pd
import numpy as np
import random

# Define some realistic data components
cities = [
    ('Victoria', 0.3),
    ('Nanaimo', 0.2),
    ('Duncan', 0.1),
    ('Courtenay', 0.1),
    ('Campbell River', 0.1),
    ('Port Alberni', 0.05),
    ('Parksville', 0.05),
    ('Comox', 0.05),
    ('Qualicum Beach', 0.05)
]

street_types = ['Street', 'Avenue', 'Road', 'Drive', 'Way']
facility_types = ['Little Stars', 'Sunshine', 'Rainbow', 'Happy Kids', 'Growing Hearts',
                 'Tiny Tots', 'Island', 'Discovery', 'Learning Tree', 'Creative Kids']
facility_suffixes = ['Childcare', 'Daycare', 'Early Learning Centre', 'Family Childcare',
                    'Child Development']

service_options = ['U36', '30SA', 'Family', 'Preschool']

# Approximate Vancouver Island coordinates
lat_range = (48.3, 50.1)
lon_range = (-125.5, -123.3)

# Generate synthetic data
data = []
for i in range(20):
    # Generate facility name
    facility_name = f"{random.choice(facility_types)} {random.choice(facility_suffixes)}"

    # Select city based on weighted probabilities
    city, _ = random.choices(cities, weights=[w for _, w in cities])[0]

    # Generate address components
    street_num = random.randint(100, 9999)
    street_name = random.choice(['Cedar', 'Pine', 'Maple', 'Oak', 'Douglas', 'Island',
                               'Ocean', 'Beach', 'Mountain', 'Forest'])
    street_type = random.choice(street_types)

    # Generate postal code (Vancouver Island starts with V)
    postal_code = f"V{random.randint(0, 9)}R {random.randint(0, 9)}K{random.randint(0, 9)}"

    # Generate full address
    address = f"{street_num} {street_name} {street_type}, {city}, BC {postal_code}"

    # Generate coordinates (slight variation based on city)
    latitude = random.uniform(lat_range[0], lat_range[1])
    longitude = random.uniform(lon_range[0], lon_range[1])

    # Generate total spaces
    total_spaces = []
    for i in range(0, len(service_options)):
        spaces = random.randint(0, 100)
        total_spaces.append(spaces)

    data.append({
        'facility_name': facility_name,
        'address': address,
        'city': city,
        'province': 'BC',
        'postal_code': postal_code,
        'latitude': round(latitude, 6),
        'longitude': round(longitude, 6),
        'U36': total_spaces[0],
        '30SA': total_spaces[1],
        'Family': total_spaces[2],
        'Preschool': total_spaces[3]
    })

# Create DataFrame
providers_df = pd.DataFrame(data)

# Generate total spaces as a sum of other services
providers_df['total_spaces'] = providers_df[service_options].sum(axis=1)

# Save to CSV
providers_df.to_csv('data/synth_data.csv', index=False)

# Display first few rows
print(f"Data successfully generated! \n \n {providers_df.head()}")