import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///meter_restaurant.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
meters = Base.classes.meters
restaurant_yelp = Base.classes.restaurant_yelp
meter_restaurant = Base.classes.meter_restaurant

# Create our session (link) from Python to the DB
session = Session(engine)
results = session.query(meters.street_name).all()
print(results)

# #################################################
# # Flask Setup
# #################################################
# app = Flask(__name__)

# @app.route("/")
# def welcome():
#     return (
#         f"HELLOOOOOOO"
      
#     )

# @app.route("/api/v1.0/street_name")
# def objectids():
#     """Return a list of stations."""
#     results = session.query(meters.street_name).all()
#     print(results)
#     street_name = list(np.ravel(results))
#     return jsonify(street_name)

# if __name__ == '__main__':
#     app.run()
