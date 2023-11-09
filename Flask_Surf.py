# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import datetime as dt


#################################################
# Database Setup
#################################################
# path to engine, POST
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"<h1>Home: Climate Analysis API</h1><br/>"
        f"<br />"
        f"<h3>Available Routes:</h3><br/>"
        f"<b><a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation</a></b> <br />"
        f"<br />"
        f"<b><a href=\"/api/v1.0/stations\">/api/v1.0/stations</a></b><br />"
        f"<br />"
        f"<b><a href=\"/api/v1.0/tobs\">/api/v1.0/tobs</a></b> <br />"
        f"<br />"
        f"<b><a href=\"/api/v1.0/start/2016-03-12\">/api/v1.0/start</a></b> <br />"
        f"<br />"
        f"<b><a href=\"/api/v1.0/range?start=2016-03-12&end=2016-08-19\">/api/v1.0/range</a></b> <br />"
        f"You can enter a range or specify only a start date to retrieve min, max and avg temps. "
        f"If only one date is specified, all dates from the available data up to that date will be returned.<br />"
        f"Dates should follow yyyy-mm-dd format using <strong>start</strong> and <strong>end</strong> parameters.<br />"
        f"(for example: /api/v1.0/range?start=2016-03-12&end=2016-08-19<br />"
        f"(start and end dates should be chronological in order)<br />"
        f"I did not make a testing table for this, so please don't be <i>that</i> user.<br />"
    )

# pathing
@app.route("/api/v1.0/precipitation")
# create precipitation query function
def precipitation():
    # session creation
    session = Session(engine)
    # data obs stop at 2017.8.23, managing year increment with timedelta, BCA is magic
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # selecting two cols, date and prcp
    # filter alters query by filtering rows greater than or equal to the date calc on prev_year
    # all appends rows that match our conditions, returns as a list of tuples
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()
    # dictionary setup, iterates over each tuple pair in precipitation
    # precip dictionary, date is our key, prcp is a value
    precip = {date: prcp for date, prcp in precipitation}
    # session close
    session.close()
    # def return, using jsonify yo convert precip list into json
    return jsonify(precip)

 
# pathing
@app.route("/api/v1.0/stations")
def stations():
    # session creation
    session = Session(engine)
    # simple list of all the stations
    results = session.query(station.station).all()
    # i need to look at this again*********************
    stations = list(np.ravel(results))
    session.close()
    # stations=stations will auto format to json 
    return jsonify(stations=stations)

#pathing
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # session creation
    session = Session(engine)
    # data obs stop at 2017.8.23, managing year increment with timedelta, BCA is magic
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #listing for tobs data
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= prev_year).all()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    session.close()
    # Return the results
    return jsonify(temps)

#pathing
@app.route("/api/v1.0/start/<start>")
def single_date(start):
    session = Session(engine)
    sel = [measurement.date, func.min(measurement.prcp), func.avg(measurement.prcp), func.max(measurement.prcp)]
    date_range = session.query(*sel).\
                filter(measurement.date >= start).\
                group_by(measurement.date).all()
    range_temps = list(np.ravel(date_range))
    session.close()
    return jsonify(range_temps)

# daterange pathing
@app.route("/api/v1.0/range")
def range():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    # Set variables for query even if no start/end is specified
    if end_date is None:
        end_date = "2018-01-01"
    if start_date is None:
        start_date = "2010-01-01" 
    session = Session(engine)
    sel = [measurement.date, func.min(measurement.prcp), func.avg(measurement.prcp), func.max(measurement.prcp)]
    date_range = session.query(*sel).\
                filter(measurement.date >= start_date).\
                filter(measurement.date <= end_date).\
                group_by(measurement.date).all()
    range_temps = list(np.ravel(date_range))
    session.close()
    
    return jsonify(range_temps)

if __name__ == "__main__":
    app.run(debug=True)