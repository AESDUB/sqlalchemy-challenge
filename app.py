#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set Up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

@app.route("/")
def index():
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/Precipitation<br>"
        f"/api/v1.0/Stations<br>"
        f"/api/v1.0/Tobs<br>"
        f"/api/v1.0/Start<br>"
        f"/api/v1.0/Start/End<br>"
    )

@app.route("/api/v1.0/Precipitation")
#  Get date and prcp values
#  Return in JSON
def precipitation():
    session = Session(engine)
    results_ = session.query(
        Measurement.date, 
        Measurement.prcp
    ).all()
    
    session.close()
    both = []
    for date, pcrp in results_:
        dict_ = {}
        dict_["date"] = date
        dict_["pcrp"] = pcrp
        both.append(results_)

    return jsonify(both)

@app.route("/api/v1.0/stations")
#  Return JSON
def stations():
    session = Session(engine)
    station_results = session.query(
        Station.id,
        Station.name
    ).all()

    session.close()

    station_names = []
    for id, name in station_results:
        dict_name = {}
        dict_name["id"] = id
        dict_name["name"] = name
        station_names.append(dict_name)

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
#  query previous year Tobs
#  Return JSON
def tobs():
    session = Session(engine)
    results_tobs = session.query(
        Measurement.id, 
        Measurement.station, 
        Measurement.date, 
        Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).order_by(Measurement.date.asc()).all()

    session.close()

    tobs_py = []
    for ids, station, date, tobs in results_tobs:
        dict_tobs = {}
        dict_tobs["id"] = ids
        dict_tobs["station"] = station
        dict_tobs["date"] = date
        dict_tobs["tobs"] = tobs
        tobs_py.append(dict_tobs)
    
    return jsonify(tobs_py)

@app.route("/api/v1.0/start")
#  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#  When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def start():
    session = Session(engine)
    results_temp_start = session.query(
        func.distinct(Measurement.station),
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.round(func.avg(Measurement.tobs),2)
    ).filter(Measurement.date == '2016-08-23').group_by(Measurement.station).all()

    session.close()
    
    temps_start = []
    for station, tmin, tmax, tavg in results_temp_start:
        dict_start = {}
        dict_start["station"] = station
        dict_start["temp_min"] = tmin
        dict_start["temp_max"] = tmax
        dict_start["temp_avg"] = tavg
        temps_start.append(dict_start)

    return jsonify(temps_start)

@app.route("/api/v1.0/start/end")
#  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#  When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def end():
    session = Session(engine)
    results_temp_end = session.query(
        func.distinct(Measurement.station),
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.round(func.avg(Measurement.tobs),2)
    ).filter(Measurement.date == '2017-08-23').group_by(Measurement.station).all()

    session.close()
    
    temps_end = []
    for station, tmin, tmax, tavg in results_temp_end:
        dict_end = {}
        dict_end["station"] = station
        dict_end["temp_min"] = tmin
        dict_end["temp_max"] = tmax
        dict_end["temp_avg"] = tavg
        temps_end.append(dict_end)

    return jsonify(temps_end)

if __name__=="__main__":
    app.run(debug=True)