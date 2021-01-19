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
        f"For precipitation in the last year of data go to /api/v1.0/precipitation<br/>"
        f"For a list of stations go to /api/v1.0/stations<br/>"
        f"For temps in the last year of the most active station's data go to /api/v1.0/tobs<br/>"
        f"For High, low, and average temps from a certain date go to /api/v1.0/start date<br/>"
        f"For High, low, and average temps from a certain date range go to /api/v1.0/start date/end date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #making the session link to the DB
    session = Session(engine)
    #pulling the last day of data
    lastDate = session.query(m.date).order_by(m.date.desc()).first()
    print(f"The last day of the data is {lastDate}")
    #setting up dates to pull from
    prevDate = dt.datetime(2016, 8, 23)
    #making my query
    results = session.query(m.date, m.prcp).\
        filter(m.date >= prevDate).\
        order_by(m.date).all()

    #closing session
    session.close()
    #setting up lists to make my json
    prcpList = []
    for date, prcp in results:
        prcpDict = {}
        prcpDict["Date"] = date
        prcpDict["prcp"] = prcp
        prcpList.append(prcpDict)

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
        stationDict = {}
        stationDict["Station"] = station
        stationDict["name"] = name
        stations.append(stationDict)

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
        tobsDict = {}
        tobsDict["Date"] = date
        tobsDict["tobs"] = tobs
        tobsList.append(tobsDict)

    return jsonify(tobsList)

@app.route("/api/v1.0/<start>")
def startDate(start):
    #session link
    session = Session(engine)

    #querying the data
    results = session.query(m.date, func.min(m.tobs),
    func.avg(m.tobs), func.max(m.tobs)).\
    filter(m.date >= start).\
    group_by(m.date).all()
    #closing session
    session.close()

    #converting our results into a normal list
    dateTemps = []
    for date, minT, avgT, maxT in results:
        dTempsDict = {}
        dTempsDict["Date"] = date
        dTempsDict["TMIN"] = minT
        dTempsDict["TAVG"] = avgT
        dTempsDict["TMAX"] = maxT
        dateTemps.append(dTempsDict)

    return jsonify(dateTemps)

@app.route("/api/v1.0/<start>/<end>")
def dateRange(start,end):
    #session link
    session = Session(engine)

    #querying the data
    results = session.query(m.date, func.min(m.tobs),
    func.avg(m.tobs), func.max(m.tobs)).\
    filter(m.date >= start).\
    filter(m.date <= end).\
    group_by(m.date).all()
    #closing session
    session.close()

    #converting our results into a normal list
    rangeTemps = []
    for date, minT, avgT, maxT in results:
        rTempsDict = {}
        rTempsDict["Date"] = date
        rTempsDict["TMIN"] = minT
        rTempsDict["TAVG"] = avgT
        rTempsDict["TMAX"] = maxT
        rangeTemps.append(rTempsDict)

    return jsonify(rangeTemps)

if __name__ == '__main__':
    app.run(debug=True)
