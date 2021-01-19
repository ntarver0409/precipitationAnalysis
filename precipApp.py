#importing relevant modules
import sqlalchemy
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#setting up my database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflecting my DB
Base = automap_base()

Base.prepare(engine, reflect=True)

#saving the references to the tables
m = Base.classes.measurement

s = Base.classes.station

#setting up my flask app
app = Flask(__name__)

#setting up Flask routes

@app.route("/")
def welcomePage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"For prcipitation in the last year of data go to /api/v1.0/precipitation<br/>"
        f"For a list of stations go to /api/v1.0/stations<br/>"
        f"For temps in the last year of data go to /api/v1.0/tobs<br/>"
        f"/api/v1.0/precipitation<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #making the session link to the DB
    session = Session(engine)
    #pulling the last day of data
    lastDate = session.query(m.date).order_by(m.date.desc()).first()
    print(f"The last day of the data is {lastDate}")
    #setting up dates to pull from
    prevDate = dt.datetime(2016, 8, 22)
    #making my query
    results = session.query(m.date, m.prcp).\
        filter(m.date > prevDate).\
        order_by(m.date).all()

    #closing session
    session.close()
    #setting up lists to make my json
    prcpList = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcpList.append(prcp_dict)

    return jsonify(prcpList)




@app.route("/api/v1.0/stations")
def stations():
    #session link
    session = Session(engine)

    #querying the station names and id's
    results = session.query(s.station, s.name).all()
    #closing session
    session.close()

    #converting our results into a normal list
    stations = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #session link
    session = Session(engine)
    #establishing the date to start pulling data from
    prevDate = dt.datetime(2016, 8, 22)
    #querying the station names and id's
    results = session.query(m.date,m.tobs).\
    filter(m.station == "USC00519281").\
    filter(m.date > prevDate).all()
    #closing session
    session.close()

    #converting our results into a normal list
    tobsList = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobsList.append(tobs_dict)

    return jsonify(tobsList)



if __name__ == '__main__':
    app.run(debug=True)
