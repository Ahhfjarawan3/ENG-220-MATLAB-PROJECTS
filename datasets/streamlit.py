import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Air Quality Trends by City")

# Baseline information for pollutant levels
st.markdown("""
## Baseline Air Quality Levels

- **Safe levels (in green):**
  - **O3 (Ozone):** ≤ 100 µg/m³ (8-hour mean)
  - **SO2 (Sulfur Dioxide):** ≤ 75 µg/m³ (1-hour mean)
  - **PM2.5 (Fine Particulate Matter):** ≤ 5 µg/m³ (annual mean)
  - **PM10 (Coarse Particulate Matter):** ≤ 15 µg/m³ (annual mean)
  - **NO2 (Nitrogen Dioxide):** ≤ 40 µg/m³ (annual mean)
  - **CO (Carbon Monoxide):** ≤ 9 ppm (8-hour mean)
  - **Pb (Lead):** ≤ 0.15 µg/m³ (rolling 3-month average)

- **Normal levels (in orange):**
  - **O3 (Ozone):** 100-150 µg/m³
  - **SO2 (Sulfur Dioxide):** 75-150 µg/m³
  - **PM2.5 (Fine Particulate Matter):** 5-15 µg/m³
  - **PM10 (Coarse Particulate Matter):** 15-45 µg/m³
  - **NO2 (Nitrogen Dioxide):** 40-80 µg/m³
  - **CO (Carbon Monoxide):** 9-15 ppm
  - **Pb (Lead):** 0.15-0.5 µg/m³

- **Dangerous levels (in red):**
  - **O3 (Ozone):** > 150 µg/m³
  - **SO2 (Sulfur Dioxide):** > 150 µg/m³
  - **PM2.5 (Fine Particulate Matter):** > 15 µg/m³
  - **PM10 (Coarse Particulate Matter):** > 45 µg/m³
  - **NO2 (Nitrogen Dioxide):** > 80 µg/m³
  - **CO (Carbon Monoxide):** > 15 ppm
  - **Pb (Lead):** > 0.5 µg/m³
""")

# Load the cleaned CSV dataset
def load_city_data():
    url = 'https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/30664fb22520cf1fbdab0ecaf20734a4932ad18f/datasets/airqualitybycity2000-2023.csv?raw=true'
    city_data = pd.read_csv(url)
    # Fill forward the CBSA and Core Based Statistical Area columns to handle empty values
    city_data['CBSA'].fillna(method='ffill', inplace=True)
    city_data['Core Based Statistical Area'].fillna(method='ffill', inplace=True)
    return city_data

# Preprocess city data to focus on required pollutants and trend statistics
def preprocess_city_data(city_data):
    # Remove the debug text displaying data shapes
    filtered_data = city_data.dropna(subset=['Pollutant', 'Trend Statistic'])
    return filtered_data

# Function to plot pollutants for a selected city
def plot_city_pollutants(city_data, city_info):
    st.write(f"Selected City: {city_info}")
    
    city_cbs_code, city_name = city_info.split(" - ", 1)
    city_data = city_data[city_data['CBSA'] == city_cbs_code]
    st.write(f"Filtered Data for Selected City ({city_name}):", city_data)
    
    years = [str(year) for year in range(2000, 2023 + 1)]
    
    plt.figure(figsize=(12, 6))
    
    for index, row in city_data.iterrows():
        pollutant = row['Pollutant']
        statistic = row['Trend Statistic']
        data_values = pd.to_numeric(row[4:], errors='coerce').fillna(0)  # Convert data to numeric and handle missing values
        
        plt.plot(years, data_values, label=f'{pollutant} ({statistic})')
    
    plt.xlabel('Year')
    plt.ylabel('Pollutant Level')
    plt.title(f'Pollutant Trends in {city_name} (2000-2023)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Main Streamlit app
st.sidebar.header("Select City")

# Load data
city_data = load_city_data()

# Preprocess data
city_data = preprocess_city_data(city_data)

# Create a dictionary mapping CBSA to city names
city_options_dict = {f"{row['CBSA']} - {row['Core Based Statistical Area']}": row['CBSA']
                     for _, row in city_data.iterrows()}

# City selection
city_options = list(city_options_dict.keys())
selected_city_info = st.sidebar.selectbox("Choose a city", city_options)

# Plot city pollutants
plot_city_pollutants(city_data, selected_city_info)
