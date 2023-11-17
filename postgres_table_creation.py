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


##Creating a Forecast Df With Timestamp

##Creating a current weather forecast df with timestamp

# Define the SQL statement to create the table
create_nws_forecast_table_query = """
CREATE TABLE IF NOT EXISTS nws_weather_forecast (
    day VARCHAR(20),
    weather_description VARCHAR(20),
    location VARCHAR(20),
    upload_timestamp TIMESTAMP
);
"""
create_historic_rhode_island_forecast_table_query = """
CREATE TABLE IF NOT EXISTS historic_weather (
    time TIMESTAMP,
    local_time TIMESTAMP,
    t2m NUMERIC,
    prectotland NUMERIC,
    precsnoland NUMERIC,
    snomas NUMERIC,
    rhoa NUMERIC,
    swgdn NUMERIC,
    swtdn NUMERIC,
    cldtot NUMERIC,
    location VARCHAR(20),
    upload_timestamp TIMESTAMP

);
"""
create_time_and_day_forecast_query = """
CREATE TABLE IF NOT EXISTS time_and_day_weather_forecast (
    day_and_date VARCHAR(20),
    temperature VARCHAR(20),
    weather_description TEXT,
    feels_like VARCHAR(20),
    wind VARCHAR(20),
    humidity VARCHAR(20),
    chance_of_precipitation VARCHAR(20),
    precipitation_amount VARCHAR(20),
    uv_index VARCHAR(20),
    sunrise VARCHAR(20),
    sunset VARCHAR(20),
    location VARCHAR(20),
    upload_timestamp TIMESTAMP

);
"""

create_current_weather_table_query = """
CREATE TABLE IF NOT EXISTS current_weather (
    temperature VARCHAR(50),
    sky_description VARCHAR(100),
    location VARCHAR(20),
    upload_timestamp TIMESTAMP

);
"""

# Execute the SQL statement
crsr.execute(create_nws_forecast_table_query)
crsr.execute(create_historic_rhode_island_forecast_table_query)
crsr.execute(create_time_and_day_forecast_query)
crsr.execute(create_current_weather_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()