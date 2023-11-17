import psycopg2
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

try:
    connection = psycopg2.connect(host="localhost", port=, database="master",
                                user="postgres", password="")
    crsr = connection.cursor()

    print('PostgreSQL database version: ')
    crsr.execute('SELECT version()')
    db_version = crsr.fetchone()
    print(db_version)

except:
    print("Connection Error")
cursor = connection.cursor()

# Extract current weather from Google search
city = "providence+ri"
url = f"https://www.google.com/search?q=weather+{city}"
current_weather = pd.DataFrame(columns=['time_description','temperature','sky_description','location','upload_timestamp'])
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
current_weather.at[0,'temperature'] = str(temp)
current_weather.at[0,'sky_description'] = sky
current_weather.at[0,'location'] = "RhodeIsland"
for index, row in current_weather.iterrows():
    cursor.execute(
        "INSERT INTO current_weather (temperature, sky_description, location, upload_timestamp) VALUES (%s, %s, %s, NOW())",
        (row['temperature'], row['sky_description'], row['location'])
    )

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
forecast_df = pd.DataFrame({
    'Day': days,
    'Weather': weathers
})
forecast_df['location'] = 'RhodeIsland'
for index, row in forecast_df.iterrows():
    cursor.execute(
        "INSERT INTO nws_weather_forecast (day, weather_description, location, upload_timestamp) VALUES (%s, %s, %s, NOW())",
        (row['Day'], row['Weather'], row['location'])
    )


#Weather Forecast time&day
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
for index, row in time_day_forecast.iterrows():
    cursor.execute(
        "INSERT INTO time_and_day_weather_forecast (day_and_date, temperature, weather_description, feels_like, wind, humidity, chance_of_precipitation, precipitation_amount, uv_index, sunrise, sunset, location, upload_timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())",
        (row['Day'], row['Temperature'], row['Weather'], row['Feels Like'], row['Wind'], row['Humidity'], row['Chance of Precipitation'], row['Precipitation Amount'], row['UV Index'], row['Sunrise'], row['Sunset'], row['location'])
    )

historic_weather_data = pd.read_csv(r'C:\Users\307164\Desktop\Weather Chat Bot\weather_data.csv')
historic_weather_data['location'] = 'RhodeIsland'
for index, row in historic_weather_data.iterrows():
    cursor.execute(
        "INSERT INTO historic_weather (time, local_time, t2m, prectotland, precsnoland, snomas, rhoa, swgdn, swtdn, cldtot, location, upload_timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())",
        (row['time'], row['local_time'], row['t2m'], row['prectotland'], row['precsnoland'], row['snomas'], row['rhoa'], row['swgdn'], row['swtdn'], row['cldtot'] ,row['location'])
    )

# Commit the changes and close the connection
connection.commit()
connection.close()

