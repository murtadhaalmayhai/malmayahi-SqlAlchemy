
###################################################################################################
#   Step 2 - Climate App
#
#   Now that you have completed your initial analysis, design a Flask API 
#   based on the queries that you have just developed.
#
#      * Use FLASK to create your routes.
#
#   Routes
#
#       * `/api/v1.0/precipitation`
#           * Query for the dates and precipitation observations from the last year.
#           * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#           * Return the json representation of your dictionary.
#       * `/api/v1.0/stations`
#           * Return a json list of stations from the dataset.
#       * `/api/v1.0/tobs`
#           * Return a json list of Temperature Observations (tobs) for the previous year
#       * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#           * Return a json list of the minimum temperature, the average temperature, and
#               the max temperature for a given start or start-end range.
#           * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates 
#               greater than and equal to the start date.
#           * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
#               for dates between the start and end date inclusive.
###################################################################################################

# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Create Engine
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask app
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home_route():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"

    )

# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route('/api/v1.0/precipitation/')
def retrieve_precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = str(last_date)[2:-3]
    last_year = str(eval(last_date[0:4])-1) + last_date[4:]

    prcp_query = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= last_year).all()
    prcp_dict = dict(prcp_query)
    print()
    print("Precipitation:")
    print()
    return jsonify(prcp_dict)

# Return a JSON list of stations from the dataset.

@app.route('/api/v1.0/stations/')
def retrieve_stations():
    station_list = session.query(Station.station).order_by(Station.station).all()
    print()
    print("Stations:")
    print()  
    for row in station_list:
        print (row[0])     
    return jsonify(station_list)

# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route('/api/v1.0/tobs/')
def retrieve_tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = str(last_date)[2:-3]
    last_year = str(eval(last_date[0:4])-1) + last_date[4:]

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year).all()
    print()
    print("Tobs:")
    print()
    return jsonify(tobs)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for 
# all dates greater than and equal to the start date.

@app.route('/api/v1.0/<start>/')
def retrieve_by_start(start):
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = str(last_date)[2:-3]
    last_year = str(eval(last_date[0:4])-1) + last_date[4:]
    
    start = last_year

    start_date_query = session.query(
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.date >= start).all()
    print()
    print("Results from start date:")
    print()
    for row in start_date_query:
        print(row)              
    return jsonify(start_date_query)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
# for dates between the start and end date inclusive.

@app.route('/api/v1.0/<start>/<end>/')
def retrieve_by_daterange(start,end):
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = str(last_date)[2:-3]
    last_year = str(eval(last_date[0:4])-1) + last_date[4:]
    
    start = last_year
    end = last_date

    date_range_query = session.query(
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.date <= end)\
                  .filter(Measurement.date >= start).all()
    print()
    print("Results from start date:")
    print()
    for row in date_range_query:
        print(row)
    return jsonify(date_range_query)

if __name__ == "__main__":
    app.run(debug=True)