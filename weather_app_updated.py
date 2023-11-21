import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from PIL import Image
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

image_url = "https://www.spc.noaa.gov/public/state/images/RI_swody1.png"

# Send a GET request to the URL
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary write mode
    with open(r"./RI_swody1.png", 'wb') as file:
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
    with open(r"./RI_swody2.png", 'wb') as file:
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
    with open(r"./RI_swody3.png", 'wb') as file:
        # Write the content of the response to the file
        file.write(response.content)
    print("Image downloaded successfully.")
else:
    print(f"Failed to retrieve image. Status code: {response.status_code}")

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 41.824,
	"longitude": -71.418884,
	"current": ["temperature_2m", "relative_humidity_2m"],
	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "evapotranspiration", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",
	"past_days": 31,
	"forecast_days": 14
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current relative_humidity_2m {current_relative_humidity_2m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
hourly_rain = hourly.Variables(6).ValuesAsNumpy()
hourly_showers = hourly.Variables(7).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(8).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(9).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(10).ValuesAsNumpy()
hourly_pressure_msl = hourly.Variables(11).ValuesAsNumpy()
hourly_surface_pressure = hourly.Variables(12).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(13).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(14).ValuesAsNumpy()
hourly_cloud_cover_mid = hourly.Variables(15).ValuesAsNumpy()
hourly_cloud_cover_high = hourly.Variables(16).ValuesAsNumpy()
hourly_visibility = hourly.Variables(17).ValuesAsNumpy()
hourly_evapotranspiration = hourly.Variables(18).ValuesAsNumpy()
hourly_et0_fao_evapotranspiration = hourly.Variables(19).ValuesAsNumpy()
hourly_vapour_pressure_deficit = hourly.Variables(20).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(21).ValuesAsNumpy()
hourly_wind_speed_80m = hourly.Variables(22).ValuesAsNumpy()
hourly_wind_speed_120m = hourly.Variables(23).ValuesAsNumpy()
hourly_wind_speed_180m = hourly.Variables(24).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(25).ValuesAsNumpy()
hourly_wind_direction_80m = hourly.Variables(26).ValuesAsNumpy()
hourly_wind_direction_120m = hourly.Variables(27).ValuesAsNumpy()
hourly_wind_direction_180m = hourly.Variables(28).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(29).ValuesAsNumpy()
hourly_temperature_80m = hourly.Variables(30).ValuesAsNumpy()
hourly_temperature_120m = hourly.Variables(31).ValuesAsNumpy()
hourly_temperature_180m = hourly.Variables(32).ValuesAsNumpy()
hourly_soil_temperature_0cm = hourly.Variables(33).ValuesAsNumpy()
hourly_soil_temperature_6cm = hourly.Variables(34).ValuesAsNumpy()
hourly_soil_temperature_18cm = hourly.Variables(35).ValuesAsNumpy()
hourly_soil_temperature_54cm = hourly.Variables(36).ValuesAsNumpy()
hourly_soil_moisture_0_to_1cm = hourly.Variables(37).ValuesAsNumpy()
hourly_soil_moisture_1_to_3cm = hourly.Variables(38).ValuesAsNumpy()
hourly_soil_moisture_3_to_9cm = hourly.Variables(39).ValuesAsNumpy()
hourly_soil_moisture_9_to_27cm = hourly.Variables(40).ValuesAsNumpy()
hourly_soil_moisture_27_to_81cm = hourly.Variables(41).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["precipitation"] = hourly_precipitation
hourly_data["rain"] = hourly_rain
hourly_data["showers"] = hourly_showers
hourly_data["snowfall"] = hourly_snowfall
hourly_data["snow_depth"] = hourly_snow_depth
hourly_data["weather_code"] = hourly_weather_code
hourly_data["pressure_msl"] = hourly_pressure_msl
hourly_data["surface_pressure"] = hourly_surface_pressure
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
hourly_data["visibility"] = hourly_visibility
hourly_data["evapotranspiration"] = hourly_evapotranspiration
hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["temperature_80m"] = hourly_temperature_80m
hourly_data["temperature_120m"] = hourly_temperature_120m
hourly_data["temperature_180m"] = hourly_temperature_180m
hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
hourly_data["soil_temperature_54cm"] = hourly_soil_temperature_54cm
hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
hourly_data["soil_moisture_1_to_3cm"] = hourly_soil_moisture_1_to_3cm
hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
hourly_data["soil_moisture_9_to_27cm"] = hourly_soil_moisture_9_to_27cm
hourly_data["soil_moisture_27_to_81cm"] = hourly_soil_moisture_27_to_81cm

hourly_dataframe = pd.DataFrame(data = hourly_data)
hourly_dataframe.head(5)

weather_data = pd.read_csv(r'./historic_weather_data.csv')
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
img1 = Image.open(r'./RI_swody1.png')
st.image([img1], width=600, caption=["Image 1"], use_column_width=True)

# Display forecasts
st.subheader("Weather Forecasts")

# Weather Foreacst - NWS
url = 'https://forecast.weather.gov/MapClick.php?lat=41.8239&lon=-71.412'
content = requests.get(url).content
soup = BeautifulSoup(content, "html.parser")
detailed_forecast = soup.find('div', id='detailed-forecast-body')

html_content = """<div class="panel-body" id="detailed-forecast-body">
<!-- Your HTML content goes here -->
</div>"""

soup = BeautifulSoup(html_content, 'html.parser')
rows = soup.find_all('div', class_='row-forecast')
days = []
weathers = []
rows = detailed_forecast.find_all('div', class_='row-forecast')
for row in rows:
    # Extract the day
    day = row.find('b').get_text(strip=True)
    days.append(day)
    weather = row.find('div', class_='forecast-text').get_text(strip=True)
    weathers.append(weather)
nws_weather_forecast_df = pd.DataFrame({
    'Day': days,
    'Weather': weathers
})
nws_weather_forecast_df['location'] = 'RhodeIsland'

url = 'https://www.timeanddate.com/weather/usa/providence/ext'

content = requests.get(url).content
soup = BeautifulSoup(content, "html.parser")

forecast_table = soup.find('table', id='wt-ext')

data = []
for row in forecast_table.select('table#wt-ext tbody tr'):
    cols = row.find_all('td')
    day = row.th.get_text(strip=True) if row.th else 'N/A'
    temperature = cols[1].get_text(strip=True) if len(cols) > 1 else 'N/A'
    weather = cols[2].get_text(strip=True) if len(cols) > 2 else 'N/A'
    feels_like = cols[3].get_text(strip=True) if len(cols) > 3 else 'N/A'
    wind = cols[4].get_text(strip=True) if len(cols) > 4 else 'N/A'
    humidity = cols[6].get_text(strip=True) if len(cols) > 6 else 'N/A'
    chance_of_precipitation = cols[7].get_text(strip=True) if len(cols) > 7 else 'N/A'
    precipitation_amount = cols[8].get_text(strip=True) if len(cols) > 8 else 'N/A'
    uv_index = cols[9].get_text(strip=True) if len(cols) > 9 else 'N/A'
    sunrise = cols[10].get_text(strip=True) if len(cols) > 10 else 'N/A'
    sunset = cols[11].get_text(strip=True) if len(cols) > 11 else 'N/A'

    data.append({
        'Day': day,
        'Temperature': temperature,
        'Weather': weather,
        'Feels Like': feels_like,
        'Wind': wind,
        'Humidity': humidity,
        'Chance of Precipitation': chance_of_precipitation,
        'Precipitation Amount': precipitation_amount,
        'UV Index': uv_index,
        'Sunrise': sunrise,
        'Sunset': sunset
    })

time_day_forecast = pd.DataFrame(data)
time_day_forecast['location'] = 'RhodeIsland'

st.subheader("National Weather Service: ")
st.dataframe(nws_weather_forecast_df.style
             .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
             .set_properties(**{'text-align': 'center', 'font-size': '12px'}), height=400, width=800)

st.subheader("Time&Date Weather Service: ")
st.dataframe(time_day_forecast.style
             .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
             .set_properties(**{'text-align': 'center', 'font-size': '12px'}), height=400, width=800)

# Display images more prominently and larger
st.subheader("Severe Weather Outlook for Next 2 Days")

img2 = Image.open(r'./RI_swody2.png')
img3 = Image.open(r'./RI_swody3.png')

st.image([img2, img3], width=600, caption=["Image 2", "Image 3"], use_column_width=True)

def filter_forecast_data(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_data = hourly_dataframe[(pd.to_datetime(hourly_dataframe['date']) >= start_date) & (pd.to_datetime(hourly_dataframe['date']) <= end_date)]
    return filtered_data

st.subheader("Extract Forecast Weather Information Based On Metrics By Date Range")
start_date = st.date_input("Select forecast start date:")
end_date = st.date_input("Select forecast end date:")

# Filter and display data when button is clicked
if st.button("Generate Forecast Plots"):
    if start_date < end_date:
        filtered_data = filter_forecast_data(start_date, end_date)

        # Weather metrics to plot
        weather_metrics = ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
       'apparent_temperature', 'precipitation', 'rain', 'snowfall',
       'snow_depth', 'weather_code', 'pressure_msl']

        # Create subplots
        fig, axes = plt.subplots(nrows=len(weather_metrics), ncols=1, figsize=(10, 6 * len(weather_metrics)))
        fig.suptitle('Weather Metrics Over Time', fontsize=16)
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'purple', 'orange', 'brown']

        for i, (metric, color) in enumerate(zip(weather_metrics, colors)):
            ax = axes[i]
            ax.plot(filtered_data['date'], filtered_data[metric], color=color, marker='o', markersize=5, label=metric)
            ax.set_ylabel(metric)
            ax.grid(True)
            ax.set_title(metric)
            ax.legend()

            # Add marker labels (values) at specific data points
            for index, value in filtered_data[[metric, 'date']].iterrows():
                ax.text(value['date'], value[metric], round(float(value[metric]), 0), ha='left', va='bottom', fontsize=6)

        # Customize plot appearance
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.tight_layout(rect=[0, 0, 1, 0.97])  # Adjust the position of the suptitle
        st.pyplot(fig)
    else:
        st.error("End date must be after the start date.")
