import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from PIL import Image
import psycopg2

try:
    connection = psycopg2.connect(host="localhost", port="5434", database="master",
                                user="postgres", password="Toyotacamry1996#")
    crsr = connection.cursor()

    print('PostgreSQL database version: ')
    crsr.execute('SELECT version()')
    db_version = crsr.fetchone()
    print(db_version)

except:
    print("Connection Error")

##HISTORIC DATA
crsr.execute("Select * FROM historic_weather LIMIT 0")
colnames = [desc[0] for desc in crsr.description]
crsr.execute("""SELECT *
FROM historic_weather
WHERE upload_timestamp = (
    SELECT MAX(upload_timestamp)
    FROM historic_weather)""")

weather_data = crsr.fetchall()

if weather_data:
    columns = colnames  # Replace with your actual column names
    historic_weather_df = pd.DataFrame(weather_data, columns=columns)
    historic_weather_df.to_csv(r'C:\Users\307164\Desktop\Weather Chat Bot\historic_weather_data.csv')
    print(historic_weather_df)
else:
    print("No data fetched")

##CURRENT WEATHER
crsr.execute("Select * FROM current_weather LIMIT 0")
colnames = [desc[0] for desc in crsr.description]
crsr.execute("""SELECT *
FROM current_weather
WHERE upload_timestamp = (
    SELECT MAX(upload_timestamp)
    FROM current_weather)""")

current_weather = crsr.fetchall()

if current_weather:
    columns = colnames  # Replace with your actual column names
    current_weather_df = pd.DataFrame(current_weather, columns=columns)
    current_weather_df.to_csv(r'C:\Users\307164\Desktop\Weather Chat Bot\current_weather.csv')
    print(current_weather_df)
else:
    print("No data fetched")


##NWS WEATHER
crsr.execute("Select * FROM nws_weather_forecast LIMIT 0")
colnames = [desc[0] for desc in crsr.description]
crsr.execute("""SELECT *
FROM nws_weather_forecast
WHERE upload_timestamp = (
    SELECT MAX(upload_timestamp)
    FROM nws_weather_forecast)""")

forecast_df_nws = crsr.fetchall()

if forecast_df_nws:
    columns = colnames  # Replace with your actual column names
    nws_weather_forecast_df = pd.DataFrame(forecast_df_nws, columns=columns)
    nws_weather_forecast_df.to_csv(r'C:\Users\307164\Desktop\Weather Chat Bot\nws_weather_forecast.csv')
    print(nws_weather_forecast_df)
else:
    print("No data fetched")


##NWS WEATHER
crsr.execute("Select * FROM time_and_day_weather_forecast LIMIT 0")
colnames = [desc[0] for desc in crsr.description]
crsr.execute("""SELECT *
FROM time_and_day_weather_forecast
WHERE upload_timestamp = (
    SELECT MAX(upload_timestamp)
    FROM time_and_day_weather_forecast)""")

time_and_day_weather_forecast = crsr.fetchall()

if time_and_day_weather_forecast:
    columns = colnames  # Replace with your actual column names
    time_and_day_weather_forecast_df = pd.DataFrame(time_and_day_weather_forecast, columns=columns)
    time_and_day_weather_forecast_df.to_csv(r'C:\Users\307164\Desktop\Weather Chat Bot\time_and_day_weather_forecast.csv')
    print(time_and_day_weather_forecast_df)
else:
    print("No data fetched")


connection.close()

image_url = "https://www.spc.noaa.gov/public/state/images/RI_swody1.png"

# Send a GET request to the URL
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary write mode
    with open(r"C:\Users\307164\Desktop\Weather Chat Bot\RI_swody1.png", 'wb') as file:
        # Write the content of the response to the file
        file.write(response.content)
    print("Image downloaded successfully.")
else:
    print(f"Failed to retrieve image. Status code: {response.status_code}")

image_url = "https://www.spc.noaa.gov/public/state/images/RI_swody2.png"

# Send a GET request to the URL
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary write mode
    with open(r"C:\Users\307164\Desktop\Weather Chat Bot\RI_swody2.png", 'wb') as file:
        # Write the content of the response to the file
        file.write(response.content)
    print("Image downloaded successfully.")
else:
    print(f"Failed to retrieve image. Status code: {response.status_code}")

image_url = "https://www.spc.noaa.gov/public/state/images/RI_swody3.png"

# Send a GET request to the URL
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary write mode
    with open(r"C:\Users\307164\Desktop\Weather Chat Bot\RI_swody3.png", 'wb') as file:
        # Write the content of the response to the file
        file.write(response.content)
    print("Image downloaded successfully.")
else:
    print(f"Failed to retrieve image. Status code: {response.status_code}")

# Define function to filter data based on date range
def filter_data(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_data = weather_data[(pd.to_datetime(weather_data['local_time']) >= start_date) & (pd.to_datetime(weather_data['local_time']) <= end_date)]
    return filtered_data

# Streamlit app layout
st.title("Weather Bot")

st.subheader("Extract Historic Weather Based Metrics By Date Range")
start_date = st.date_input("Select start date:")
end_date = st.date_input("Select end date:")

# Filter and display data when button is clicked
if st.button("Generate Plots"):
    if start_date < end_date:
        filtered_data = filter_data(start_date, end_date)

        # Weather metrics to plot
        weather_metrics = ['t2m', 'prectotland', 'precsnoland', 'snomas', 'rhoa', 'swgdn', 'swtdn', 'cldtot']

        # Create subplots
        fig, axes = plt.subplots(nrows=len(weather_metrics), ncols=1, figsize=(10, 6 * len(weather_metrics)))
        fig.suptitle('Weather Metrics Over Time', fontsize=16)
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'purple']

        for i, (metric, color) in enumerate(zip(weather_metrics, colors)):
            ax = axes[i]
            ax.plot(filtered_data['local_time'], filtered_data[metric], color=color, marker='o', markersize=5, label=metric)
            ax.set_ylabel(metric)
            ax.grid(True)
            ax.set_title(metric)
            ax.legend()

            # Add marker labels (values) at specific data points
            for index, value in filtered_data[[metric, 'local_time']].iterrows():
                ax.text(value['local_time'], value[metric], round(float(value[metric]), 0), ha='left', va='bottom', fontsize=6)

        # Customize plot appearance
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.tight_layout(rect=[0, 0, 1, 0.97])  # Adjust the position of the suptitle
        st.pyplot(fig)
    else:
        st.error("End date must be after the start date.")

# Display current weather information
st.subheader("Current Weather in Providence, Rhode Island")

# Extract current weather from Google search
city = "providence+ri"
url = f"https://www.google.com/search?q=weather+{city}"
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
str_data = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
data = str_data.split('\n')
time = data[0]
sky = data[1]
list_div = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
str_data = list_div[5].text
pos = str_data.find('Wind')
other_data = str_data[pos:]
current_weather_info = f"Temperature: {temp} °C\nTime: {time}\nSky Description: {sky}\n{other_data}"

st.markdown(f"```{current_weather_info}```", unsafe_allow_html=True)
st.subheader("Storm Outlook for Today")
img1 = Image.open(r'C:\Users\307164\Desktop\Weather Chat Bot\RI_swody1.png')
st.image([img1], width=600, caption=["Image 1"], use_column_width=True)

# Display forecasts
st.subheader("Weather Forecasts")

# Display forecasts from CSV files as stylish tables with headers
print(forecast_df_nws)
st.dataframe(nws_weather_forecast_df.style
             .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
             .set_properties(**{'text-align': 'center', 'font-size': '12px'}), height=400, width=800)

st.dataframe(time_and_day_weather_forecast_df.style
             .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
             .set_properties(**{'text-align': 'center', 'font-size': '12px'}), height=400, width=800)

# Display images more prominently and larger
st.subheader("Severe Weather Outlook for Next 2 Days")

img2 = Image.open(r'C:\Users\307164\Desktop\Weather Chat Bot\RI_swody2.png')
img3 = Image.open(r'C:\Users\307164\Desktop\Weather Chat Bot\RI_swody3.png')

st.image([img2, img3], width=600, caption=["Image 2", "Image 3"], use_column_width=True)
