import flask
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = flask.Flask(__name__)
app.config["DEBUG"] = True

today = str(datetime.today())
print(today)
def calc_temps(start_date, end_date=today):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


@app.route('/', methods=['GET'])
def home():
    return """<h1>Hawaii Climate: Available APIs</h1>
<ul>
<li>/api/v1.0/precipitation</li>
<li>/api/v1.0/stations</li>
<li>/api/v1.0/tobs</li>
<li>/api/v1.0/&ltstart&gt</li>
<li>/api/v1.0/&ltstart&gt>/&ltend&gt</li>
</ul>
"""

@app.route('/api/v1.0/precipitation', methods=['GET'])
def prcp():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp)
    results = {date:prcp for date,prcp in results}
    return results

@app.route('/api/v1.0/precipitation', methods=['GET'])
def stations():
    session = Session(engine)
    results = session.query(Station.station)
    results = [station  for station in results]
    return flask.jsonify(results)

@app.route('/api/v1.0/precipitation', methods=['GET'])
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measuremnt.date >= "2016-08-24")
    results = [tobs[0] for tobs in results]
    return flask.jsonify(results)


@app.route('/api/v1.0/<start>', methods=['GET'])
def stats_from_start_date(start):
    results = calc_temps(start)
    return flask.jsonify(results[0])

@app.route('/api/v1.0/<start>/<end>', methods=['GET'])
def stats_from_start_end_date(start, end):
    results = calc_temps(start, end)
    return flask.jsonify(results[0])

app.run()