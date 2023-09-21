import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials



scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('lastumico-3e895435cca2.json', scope)
client = gspread.authorize(creds)

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


@st.cache_data(ttl=3)  # Refresh every 60 seconds
def get_data():
    # Open the Google Spreadsheet by title
    spreadsheet = client.open('umico_responses')

    # Select a specific worksheet
    worksheet = spreadsheet.worksheet('Form Responses 1')  # Replace with your sheet name

    # Get the data from the worksheet
    data = worksheet.get_all_records()

    # Create a DataFrame from the data
    df = pd.DataFrame(data)
    
    return df

# Create a pie chart
def create_pie_chart(df):
    gender_counts = df['Cinsiyyət'].value_counts()
    
    # Define custom colors
    colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightsalmon']
    
    # Explode a specific slice (e.g., the first one)
    explode = [0.1 if i == 0 else 0 for i in range(len(gender_counts))]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140,
           colors=colors, explode=explode, shadow=True, textprops={'fontsize': 12})
    ax.set_title('Gender Distribution', fontsize=16)
    
    # Add a legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    
    # Set the background color to transparent
    fig.patch.set_alpha(0)
    
    return fig

# Initialize a placeholder for the pie chart
chart_placeholder = st.empty()

# Main Streamlit app
while True:
    df = get_data()
    fig = create_pie_chart(df)
    
    # Clear the previous chart by replacing it with the new one
    chart_placeholder.pyplot(fig)

    # Close the previous Matplotlib figure
    plt.close(fig)

    # Add a delay before refreshing (e.g., every 10 seconds)
    time.sleep(3)


