# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days = 366)
most_active_station = "USC00519281"


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def hawaii_climate():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

@app.route("/api/v1.0/precipitation")
def preciptitation():
    precipitation_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()
    precipitation_data_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_data_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station_tobs = session.query(measurement.tobs).filter(measurement.station == most_active_station).filter(measurement.date >= one_year_ago).all()
    most_active_station_tobs_list = list(np.ravel(most_active_station_tobs))
    return jsonify(most_active_station_tobs_list)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    start_date_aggregations = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    start_date_aggregations_dict = {"min_temp": start_date_aggregations[0][0],
                                    "avg_temp": start_date_aggregations[0][1],
                                    "max_temp": start_date_aggregations[0][2]
    }
    return jsonify(start_date_aggregations_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    date_range_aggregations = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    date_range_aggregations_dict = {"min_temp": date_range_aggregations[0][0],
                                    "avg_temp": date_range_aggregations[0][1],
                                    "max_temp": date_range_aggregations[0][2]
    }
    return jsonify(date_range_aggregations_dict)

if __name__ == "__main__":
    app.run(debug = True)