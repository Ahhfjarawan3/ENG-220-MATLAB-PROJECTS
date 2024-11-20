import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Air Quality Trends by City")

# Load the cleaned CSV dataset
def load_city_data():
    url = 'https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/30664fb22520cf1fbdab0ecaf20734a4932ad18f/datasets/airqualitybycity2000-2023.csv?raw=true'
    city_data = pd.read_csv(url)
    # Fill forward the CBSA column to handle empty city names
    city_data['CBSA'].fillna(method='ffill', inplace=True)
    return city_data

# Preprocess city data to focus on required pollutants and trend statistics
def preprocess_city_data(city_data):
    st.write("Original Data Shape:", city_data.shape)
    
    required_pollutants = ['CO', 'NO2', 'O3', 'PM10', 'PM2.5']
    required_statistics = ['2nd Max', 'Annual Mean', '4th Max', 'Weighted Annual Mean']
    
    filtered_data = city_data[(city_data['Pollutant'].isin(required_pollutants)) &
                              (city_data['Trend Statistic'].isin(required_statistics))]
    
    st.write("Filtered Data Shape:", filtered_data.shape)
    
    return filtered_data

# Function to plot pollutants for a selected city
def plot_city_pollutants(city_data, city_name):
    st.write(f"Selected City: {city_name}")
    
    city_data = city_data[city_data['Core Based Statistical Area'] == city_name]
    st.write("Filtered Data for Selected City:", city_data)
    
    years = [str(year) for year in range(2000, 2023 + 1)]
    pollutants = {
        'CO': '2nd Max',
        'NO2': 'Annual Mean',
        'O3': '4th Max',
        'PM10': '2nd Max',
        'PM2.5': 'Weighted Annual Mean'
    }
    
    plt.figure(figsize=(12, 6))
    
    for pollutant, statistic in pollutants.items():
        pollutant_data = city_data[(city_data['Pollutant'] == pollutant) & (city_data['Trend Statistic'] == statistic)]
        
        if pollutant_data.empty:
            st.write(f"No data available for {pollutant} ({statistic})")
            continue
        
        # Convert to numeric and handle missing values
        data_values = pd.to_numeric(pollutant_data.iloc[0, 4:], errors='coerce').fillna(0)
        
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

# City selection
city_options = city_data['Core Based Statistical Area'].unique()
selected_city = st.sidebar.selectbox("Choose a city", city_options)

# Plot city pollutants
plot_city_pollutants(city_data, selected_city)
