import psycopg2
import pandas as pd

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

historic_weather = crsr.fetchall()

if historic_weather:
    columns = colnames  # Replace with your actual column names
    historic_weather_df = pd.DataFrame(historic_weather, columns=columns)
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

nws_weather_forecast = crsr.fetchall()

if nws_weather_forecast:
    columns = colnames  # Replace with your actual column names
    nws_weather_forecast_df = pd.DataFrame(nws_weather_forecast, columns=columns)
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