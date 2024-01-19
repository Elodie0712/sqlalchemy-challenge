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
    