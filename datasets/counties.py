import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load and clean all datasets
def load_and_clean_data():
    base_url = "https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/ace503643ae54f6486fe708d856a01c95961489e/datasets/county_datasets/conreport"
    all_data = []

    for year in range(2000, 2023 + 1):
        url = f"{base_url}{year}.csv?raw=true"
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(url)
        
        # Replace '.' with NaN
        df.replace('.', pd.NA, inplace=True)
        
        # Add a 'Year' column
        df['Year'] = year
        
        # Append to the list
        all_data.append(df)
    
    # Concatenate all dataframes
    merged_data = pd.concat(all_data, ignore_index=True)
    
    return merged_data

# Function to check if there is enough data to plot
def has_enough_data(data, pollutant):
    # Check if there are at least 3 non-NaN values
    return data[pollutant].count() >= 3

# Function to plot pollutants for a selected county and pollutant
def plot_pollutant(data, pollutant):
    data = data[['Year', pollutant]].dropna()
    
    if not has_enough_data(data, pollutant):
        st.write("No data available for this pollutant in the selected county.")
    else:
        plt.figure(figsize=(12, 6))
        plt.plot(data['Year'], data[pollutant], marker='o')
        plt.xlabel('Year')
        plt.ylabel(f'{pollutant} Level')
        plt.title(f'Trend of {pollutant} in {selected_county} (2000-2023)')
        plt.grid(True)
        st.pyplot(plt)

# Title of the app
st.title("County Air Quality Trends")

# Load and clean data
merged_data = load_and_clean_data()

# Select a county
county_options = merged_data['County'].unique()
selected_county = st.sidebar.selectbox("Choose a county", county_options)

# Select a pollutant
pollutant_options = merged_data.columns[2:-1]  # Exclude 'County Code', 'County', and 'Year'
selected_pollutant = st.sidebar.selectbox("Choose a pollutant", pollutant_options)

# Filter data based on selections
county_data = merged_data[merged_data['County'] == selected_county]

# Plot data for the selected pollutant
plot_pollutant(county_data, selected_pollutant)
