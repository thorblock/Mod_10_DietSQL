# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
# path to engine, POST
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def welcome():
    return (
        f"Home: Climate Analysis API<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

# pathing
@app.route("/api/v1.0/precipitation")
# create precipitation query function
def precipitation():
    # data obs stop at 2017.8.23, managing year increment with timedelta, BCA is magic
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # listing for date and prcp data, using filter to clean it down based on the above
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    # dictionary, so we can write and store as a json
    precip = {date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)

 
# pathing
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # i need to look at this again*********************
    stations = list(np.ravel(results))
    session.close()
    # stations=stations will auto format to json 
    return jsonify(stations=stations)

#pathing
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # data obs stop at 2017.8.23, managing year increment with timedelta, BCA is magic
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #listing for tobs data
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    session.close()
    # Return the results
    return jsonify(temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    ##Return TMIN, TAVG, TMAX.

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    print ("=============")
    print (start)
    print (end)
    print ("=============")
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    session.close()
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)