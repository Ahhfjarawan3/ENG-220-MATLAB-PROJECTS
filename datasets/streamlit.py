import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Air Quality Trends in Albuquerque")

# Load the cleaned CSV dataset
def load_city_data():
    url = 'https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/30664fb22520cf1fbdab0ecaf20734a4932ad18f/datasets/airqualitybycity2000-2023.csv?raw=true'
    city_data = pd.read_csv(url)
    return city_data

# Preprocess city data to focus on Albuquerque and required pollutants
def preprocess_city_data(city_data):
    st.write("Original Data Shape:", city_data.shape)
    
    # Fill forward the CBSA column to handle empty city names
    city_data['CBSA'].fillna(method='ffill', inplace=True)
    
    albuquerque_data = city_data[city_data['CBSA'] == 'Albuquerque, NM'].copy()
    st.write("Filtered Data for Albuquerque Shape:", albuquerque_data.shape)
    
    # Filter for required pollutants
    albuquerque_data = albuquerque_data[(albuquerque_data['Pollutant'] == 'CO') | 
                                        (albuquerque_data['Pollutant'] == 'NO2') |
                                        (albuquerque_data['Pollutant'] == 'O3') |
                                        (albuquerque_data['Pollutant'] == 'PM10') |
                                        (albuquerque_data['Pollutant'] == 'PM2.5')]
    st.write("Filtered Data for Pollutants Shape:", albuquerque_data.shape)
    
    # Filter for required trend statistics
    albuquerque_data = albuquerque_data[albuquerque_data['Trend Statistic'].isin(['2nd Max', 'Annual Mean', '4th Max', 'Weighted Annual Mean'])]
    st.write("Filtered Data for Trend Statistics Shape:", albuquerque_data.shape)
    
    # Debug: Display the filtered data for Albuquerque
    st.write("Filtered Data for Albuquerque:", albuquerque_data)
    
    return albuquerque_data

# Function to plot pollutants for Albuquerque
def plot_city_pollutants(city_data):
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
    plt.title('Pollutant Trends in Albuquerque (2000-2023)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Main Streamlit app
st.sidebar.header("Upload Dataset")

# Load data
city_data = load_city_data()

# Preprocess data
city_data = preprocess_city_data(city_data)

# Plot city pollutants
plot_city_pollutants(city_data)
