import pandas as pd
import numpy as np
import random

# Dictionary to change some column headers
rename_dict = {
    "NAME": "facility_name",
    "ADDRESS_1": "address",
    "LATITUDE": "latitude",
    "LONGITUDE": "longitude",
    "CITY": "city",
    "POSTAL_CODE": "postal_code"
}

# Reading in test data from BC's Open Data Catalogue:
# Source: https://catalogue.data.gov.bc.ca/dataset/child-care-map-data
bc_data = pd.read_csv('https://catalogue.data.gov.bc.ca/dataset/4cc207cc-ff03-44f8-8c5f-415af5224646/resource/9a9f14e1-03ea-4a11-936a-6e77b15eeb39/download/childcare_locations.csv')
df = bc_data[["NAME", "ADDRESS_1", "CITY", "POSTAL_CODE",  "LATITUDE", "LONGITUDE"]]
df.rename(columns=rename_dict, inplace=True)


# Generate synthetic data related to child care spaces
service_options = ['U36', '30SA', 'Family', 'Preschool']
data = []

for i in range(df.shape[0]):
    # Generate total spaces
    total_spaces = []
    for i in range(0, len(service_options)):
        spaces = random.randint(0, 100)
        total_spaces.append(spaces)

    data.append({
        'U36': total_spaces[0],
        '30SA': total_spaces[1],
        'Family': total_spaces[2],
        'Preschool': total_spaces[3]
    })

# Create DataFrame
joint_df = pd.DataFrame(data)

providers_df = pd.concat([df, joint_df], axis=1)

# Generate total spaces as a sum of other services
providers_df['total_spaces'] = providers_df[service_options].sum(axis=1)

# Save to CSV
providers_df.to_csv('data/synth_data.csv', index=False)

# Display first few rows
print(f"Data successfully generated! \n \n {providers_df.head()}")