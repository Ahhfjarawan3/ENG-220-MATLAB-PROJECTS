import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Finance Visualizations for Air Quality Projects")

# State name mapping
state_mapping = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Function to load air quality applications data
def load_applications_data():
    url = 'https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/main/datasets/finanace/airqualityapplications2024.csv?raw=true'
    data = pd.read_csv(url)
    data.columns = [col.strip() for col in data.columns]  # Strip any extra spaces from column names
    data['Proposed EPA Funding'] = data['Proposed EPA Funding'].replace('[\$,]', '', regex=True).astype(float)  # Clean funding values
    return data

# Function to load awards granted data
def load_awards_data():
    url = 'https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/main/datasets/finanace/AirQualityDirectAwards2022.csv?raw=true'
    data = pd.read_csv(url)
    return data

# Function to load EPA budget data
def load_budget_data():
    url = 'https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/main/datasets/finanace/EPAbudget.csv?raw=true'
    data = pd.read_csv(url)
    return data

# Function to plot bar chart
def plot_bar_chart(data, x, y, title, x_label, y_label):
    plt.figure(figsize=(12, 6))
    plt.bar(data[x], data[y], color='skyblue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=90)
    plt.grid(True)
    st.pyplot(plt)

# Function to filter applications data by state
def filter_applications_by_state(data, state):
    return data[data['Project State(s)'].str.contains(state)]

# Visualization for Dataset 1
def visualize_applications():
    applications_data = load_applications_data()
    states = applications_data['Project State(s)'].str.split(', ', expand=True).stack().unique()
    state_options = {abbr: state_mapping.get(abbr, abbr) for abbr in states}
    selected_state_abbr = st.selectbox("Select a State", list(state_options.keys()), format_func=lambda x: state_options[x])
    
    filtered_data = filter_applications_by_state(applications_data, selected_state_abbr)
    
    st.write("### Applications Data")
    st.dataframe(filtered_data)
    
    filtered_data['Proposed EPA Funding'] *= 1000  # Convert to actual amounts
    plot_bar_chart(filtered_data, 'Primary Applicant', 'Proposed EPA Funding', 
                   f'Proposed EPA Funding for {state_options[selected_state_abbr]}', 'Primary Applicant', 'Proposed EPA Funding ($)')
    
    total_funding = filtered_data['Proposed EPA Funding'].sum()
    st.write(f"### Total Proposed EPA Funding for {state_options[selected_state_abbr]}: ${total_funding:,.2f}")

# Function to filter awards data by EPA region
def filter_awards_by_region(data, region):
    return data[data['EPA Region'] == region]

# Visualization for Dataset 2
def visualize_awards():
    awards_data = load_awards_data()
    regions = awards_data['EPA Region'].unique()
    selected_region = st.selectbox("Select an EPA Region", regions)
    
    filtered_data = filter_awards_by_region(awards_data, selected_region)
    
    st.image('https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/main/datasets/eparegions.png?raw=true', caption='EPA Regions Map', use_column_width=True)
    
    st.write("### Awards Data")
    st.dataframe(filtered_data)
    
    filtered_data['Amount Awarded'] *= 1000  # Convert to actual amounts
    plot_bar_chart(filtered_data, 'Grant Recipient', 'Amount Awarded', 
                   f'Amount Awarded in EPA Region {selected_region}', 'Grant Recipient', 'Amount Awarded ($)')
    
    total_awarded = filtered_data['Amount Awarded'].sum()
    st.write(f"### Total Amount Awarded in EPA Region {selected_region}: ${total_awarded:,.2f}")

# Visualization for Dataset 3
def visualize_budget():
    budget_data = load_budget_data()
    
    st.write("### EPA Budget Data")
    st.dataframe(budget_data)
    
    # Budget Trend
    plot_bar_chart(budget_data, 'Fiscal Year', 'Enacted Budget', 
                   'EPA Budget Over the Years', 'Fiscal Year', 'Enacted Budget ($)')
    
    # Workforce Trend
    plt.figure(figsize=(12, 6))
    plt.plot(budget_data['Fiscal Year'], budget_data['Workforce'], marker='o', color='orange')
    plt.xlabel('Fiscal Year')
    plt.ylabel('Workforce')
    plt.title('EPA Workforce Over the Years')
    plt.grid(True)
    st.pyplot(plt)

# Add new tabs for finance datasets
finance_tabs = st.tabs(["Air Quality Applications", "Awards Granted", "EPA Budget"])

with finance_tabs[0]:
    st.markdown("## Air Quality Applications and Funding")
    visualize_applications()

with finance_tabs[1]:
    st.markdown("## Awards Granted in 2022")
    visualize_awards()

with finance_tabs[2]:
    st.markdown("## EPA Budget from 2000-2023")
    visualize_budget()
