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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"our project data"
      
    )
    
# @app.route("/api/v1.0/street_name")
# def objectids():
#     """Return a list of stations."""
#     results = session.query(meters.street_name).all()
#     print(results)
#     street_name = list(np.ravel(results))
#     return jsonify(street_name)

@app.route("/restaurant_yelp/location")
def restaurant():
    restaurants =[]

    """Return all columns of each restaurant"""
    sel = [restaurant_yelp.name, 
           restaurant_yelp.categary_title,
           restaurant_yelp.latitude,
           restaurant_yelp.longitude,
           restaurant_yelp.price, 
           restaurant_yelp.rating,
           restaurant_yelp.review_count,
           restaurant_yelp.display_phone,
           restaurant_yelp.zip_code,
           restaurant_yelp.image_url]
    
    results = session.query(*sel).all()

    # Create a dictionary entry for each row of restaurant information
    for result in results:
        restaurant = {}
        restaurant["name"] = result[0]
        restaurant["categary_title"] = result[1]
        restaurant["latitude"] = result[2]
        restaurant["longitude"] = result[3]
        restaurant["coordinates"] = (result[2],result[3])
        restaurant["price"] = result[4]
        restaurant["rating"] = result[5]
        restaurant["review_count"] = result[6]
        restaurant["display_phone"] = result[7]
        restaurant["zip"] = result[8]
        restaurant["image_url"] = result[9]

        restaurants.append(restaurant)
       
    # print(restaurants)
    
    return jsonify(restaurants)   

if __name__ == '__main__':
    app.run(port=8600)
