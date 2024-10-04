import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
hour_df = pd.read_csv("./Dashboard/hour_cleaned.csv")

# Convert the 'date' column to datetime format if it's not already
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Check the min and max dates
min_date = hour_df['date'].min().date()  # Extracting the date part
max_date = hour_df['date'].max().date()  # Extracting the date part

# Set the title for the app
st.title('🚲 Bike Sharing Data Dashboard')

# Add a date range filter using date_input
selected_dates = st.date_input("Select Date Range", 
                                value=(min_date, max_date), 
                                min_value=min_date, 
                                max_value=max_date)

# Handle the case where a single date is selected
if isinstance(selected_dates, tuple):
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates  # If only one date is selected

# Filter the data based on the selected date range
filtered_hour_df = hour_df[(hour_df['date'] >= pd.to_datetime(start_date)) & 
                            (hour_df['date'] <= pd.to_datetime(end_date))]

# Check if there are any entries for the selected date range
if filtered_hour_df.empty:
    st.warning("No data available for the selected date range.")
else:
    # Pie chart for user comparison
    st.subheader('Total Casual vs Registered Users')
    total_casual = filtered_hour_df['casual_user'].sum()
    total_registered = filtered_hour_df['registered_user'].sum()

    labels = ['Casual User', 'Registered User']
    sizes = [total_casual, total_registered]
    colors = ['#FFA500', '#800000']

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('Comparison of Casual and Registered Users', fontsize=15)
    ax.axis('equal')  # To ensure the pie chart is circular

    # Display the pie chart in Streamlit
    st.pyplot(fig)

    # Point plot for bike-sharing productivity based on time
    st.subheader('Bike Sharing Productivity Based on Time')
    fig, ax = plt.subplots(figsize=(20, 5))
    sns.pointplot(data=filtered_hour_df, x='hour', y='total_user', hue='workingday', errorbar=None, ax=ax)
    ax.set(title='Bike Sharing Productivity Based on Time')
    ax.set_ylabel('Total User')
    ax.set_xlabel('Hour')

    # Display the point plot in Streamlit
    st.pyplot(fig)

    # Bar plot for weather conditions
    st.subheader('Effect of Weather Conditions on Users')
    byweather_df = filtered_hour_df.groupby("weather").total_user.sum().sort_values(ascending=False).reset_index()

    colors_weather = ["#00008B", "#C9C0BB", "#C9C0BB", "#C9C0BB"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        y="total_user", 
        x="weather",
        data=byweather_df.sort_values(by="total_user", ascending=False),
        palette=colors_weather
    )
    ax.set_title("Effect of Weather Conditions on Users", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=12)

    # Display the bar chart in Streamlit
    st.pyplot(fig)

    # Bar plot for total users by day of the week
    st.subheader('Bike Sharing Users by Day of the Week')
    bydays_df = filtered_hour_df.groupby("day").total_user.sum().sort_values(ascending=False).reset_index()

    colors_day = ["#800000", "#C9C0BB", "#C9C0BB", "#C9C0BB", "#C9C0BB", "#C9C0BB", "#C9C0BB"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        y="total_user", 
        x="day",
        data=bydays_df.sort_values(by="total_user", ascending=False),
        palette=colors_day
    )
    ax.set_title("Bike Sharing Users by Day of the Week", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=12)

    # Display the bar chart in Streamlit
    st.pyplot(fig)

    # Bar plot for total users by season
    st.subheader('Bike Sharing Users by Season')
    byseason_df = filtered_hour_df.groupby("season").total_user.sum().sort_values(ascending=False).reset_index()

    colors_season = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x="total_user", 
        y="season",
        data=byseason_df.sort_values(by="total_user", ascending=False),
        palette=colors_season
    )
    ax.set_title("Bike Sharing Users by Season", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=12)

    # Display the bar chart in Streamlit
    st.pyplot(fig)
