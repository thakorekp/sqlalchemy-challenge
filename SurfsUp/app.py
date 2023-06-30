# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import numpy as np
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the date and precipitation scores
    precip_data = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()
    
    session.close()

    # Create a dictionary from results and append to list
    precipitation_list = []
    for date,prcp in precip_data:
        precip_data_dict = {}
        precip_data_dict["date"] = date
        precip_data_dict["precip"] = prcp
        precipitation_list.append(precip_data_dict)

    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to list the stations from the dataset
    stations = session.query(Station.station).all()
    session.close()

    # Convert to list
    all_stations_list = list(np.ravel(stations))

    return jsonify(all_stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query for the last 12 months of temperature observation data for the most active station  
    active_station_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date <= '2017-08-18').filter(Measurement.date >= '2016-08-18').all()
    session.close()
    
    # Convert to list
    active_station_temp_list = list(np.ravel(active_station_data))

    return jsonify(active_station_temp_list)

@app.route("/api/v1.0/start")
def dynamic_start():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query
    start_date = ""
    station_temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= {start_date}).all()
    session.close()
    
    return jsonify(station_temps)

@app.route("/api/v1.0/start/end")
def dynamic_start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query
    start_date = ""
    end_date = ""
    station_temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= {start_date}).filter(Measurement.date <= {end_date}).all()
    session.close()
    
    return jsonify(station_temps)


if __name__ == "__main__":
    app.run(debug=True)