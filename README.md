SURFUP 
![image](https://github.com/Elodie0712/sqlalchemy-challenge/assets/148305373/4e2deb17-8768-4f79-83b7-37c61084a419)
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area.
Part 1: Analyze and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. 
-Use the SQLAlchemy create_engine() function to connect to your SQLite database.
![image](https://github.com/Elodie0712/sqlalchemy-challenge/assets/148305373/908779f8-a5f8-4bd3-ab75-f2b08a0e2371)

-Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
![image](https://github.com/Elodie0712/sqlalchemy-challenge/assets/148305373/530e44c9-e1e9-4a0b-b462-d87a3d24c3f9)

-Link Python to the database by creating a SQLAlchemy session.
![image](https://github.com/Elodie0712/sqlalchemy-challenge/assets/148305373/1eb0b65e-0ce2-44fb-8d2a-ba5e0e1b6fd8)
____________________________________________________________________________________________________________________
1. Find the most recent date in the dataset.
2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
3. Load the query results into a Pandas DataFrame. 
4.Plot the results by using the DataFrame plot method, as the following image shows:
![image](https://github.com/Elodie0712/sqlalchemy-challenge/assets/148305373/13dd0c8e-c4a0-46a6-bf5c-907e2d2e00b1)

Station Analysis

1. Design a query to calculate the total number of stations in the dataset.
2. Design a query to find the most-active stations 
3. Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
4. Query the previous 12 months of TOBS data for that station.
5. Plot the results as a histogram with bins=12
![image](https://github.com/Elodie0712/sqlalchemy-challenge/assets/148305373/0c809ef9-4730-454a-9ce6-7ab2da22af3f)

Part 2 - Designing your Climate App
/
1. Start at the homepage.
2, List all the available routes.

3. /api/v1.0/precipitation
Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
   a) Return the JSON representation of your dictionary.

4. /api/v1.0/stations
    a)Return a JSON list of stations from the dataset.
5. /api/v1.0/tobs
Query the dates and temperature observations of the most-active station for the previous year of data.
    a)Return a JSON list of temperature observations for the previous year.

6. /api/v1.0/<start> and /api/v1.0/<start>/<end>
    a)Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    b)For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
     c) For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt




# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import Query
from flask import Flask
 
#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement=Base.classes.measurement
station= Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
#create an app
app= Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home_page():
    return (
        f"Welcome to my Climate Analasis<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database.
    last_12_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Calculate the date one year from the last date in the data set.
    previous_year = dt.date(last_12_months.year, last_12_months.month, last_12_months.day)
    
    # Perform a query to retrieve the data and precipitation scores
    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= previous_year).order_by(measurement.date).all()

    # Convert query results to a dictionary
    r_dict = dict(query)

    # Close the session
    session.close()

    # Return the JSON response
    return jsonify(r_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data for stations
    query = session.query(station.id, station.station, station.name, station.latitude, station.longitude).all()

    # Close the session
    session.close()

    # Create a list for stations
    station_list = []

    # Iterate through the query results and create a dictionary for each station
    for id, station, name, latitude, longitude in query:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude

        # Append the station dictionary to the list
        station_list.append(station_dict)

    # Return the JSON response containing the list of stations
    return jsonify(station_list)

    
@app.route("/api/v1.0/tobs")
def tobs():  
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the dates and temperature observations of the most-active station for the previous year of data
    temps_results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= '2016-08-23').all()

    # Close the session
    session.close()

    # Create a list for temperature observations
    to_list = []

    # Iterate through the query results and create a dictionary for each temperature observation
    for result in temps_results:
        to_dict = {}
        to_dict["tobs"] = result[0]  # Assuming the result is a tuple, get the first element
        to_list.append(to_dict)

    # Return the JSON response containing the list of temperature observations
    return jsonify(to_list)

@app.route("/api/v1.0/<start>")

def temps_start(start):
       # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date >= start).all()
    # Close the session
    session.close()
# Iterate through the query results
    temps=[]
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)

@app.route("/api/v1.0/end")
def temps_end(end):
       # Create our session (link) from Python to the DB
    session = Session(engine)
     #Query
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date <= end).all()
    # Close the session
    session.close()
# Iterate through the query results
    temps = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)
