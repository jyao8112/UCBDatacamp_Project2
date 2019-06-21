import os

import pandas as pd
import numpy as np
import sqlite3
import pandas 

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import seaborn as sns

# Import SQLAlchemy `automap` and other dependencies here
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

app = Flask(__name__)


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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meter_restaurant.sqlite"
db = SQLAlchemy(app)
def meter_loc_resturant():
    sel = [meters.objectid, 
           meters.street_num,
           meters.street_name,
           meters.longitude,
           meters.latitude, 
           meters.meter_type]
    meters_json ={}
    results = db.session.query(*sel).all()
    for result in results:
            meter = {}
            meter["coordinates"] = (result[4],result[3])
            meter["meter_id"] = str(result[0])
            meters_json[result[0]]=meter

    sel2 = [meter_restaurant.yelp_id, 
           meter_restaurant.meter1,
           meter_restaurant.meter2,
           meter_restaurant.meter3,
           meter_restaurant.meter4, 
           meter_restaurant.meter5,
           meter_restaurant.meter6,
           meter_restaurant.meter7,
           meter_restaurant.meter8,
           meter_restaurant.meter9,
           meter_restaurant.meter10,
           ]
    results2 = db.session.query(*sel2).all()
    meter_to_restaurants_json=[]
    for result in results2:
            meter_to_restaurants = {}

            meter_to_restaurants["yelp_id"] = result[0]
            meter_to_restaurants["meter1"] = result[1]
            meter_to_restaurants["meter2"] = result[2]
            meter_to_restaurants["meter3"] = result[3]
            meter_to_restaurants["meter4"] = result[4]
            meter_to_restaurants["meter5"] = result[5]
            meter_to_restaurants["meter6"] = result[6]
            meter_to_restaurants["meter7"] = result[7]
            meter_to_restaurants["meter8"] = result[8]
            meter_to_restaurants["meter9"] = result[9]
            meter_to_restaurants["meter10"] = result[10]
        
            meter_to_restaurants_json.append(meter_to_restaurants)
    for i in meter_to_restaurants_json:
            coordinates = meters_json[i["meter1"]]["coordinates"]
            i["meter1"]=[i["meter1"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter2"]]["coordinates"]
            i["meter2"]=[i["meter2"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter3"]]["coordinates"]
            i["meter3"]=[i["meter3"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter4"]]["coordinates"]
            i["meter4"]=[i["meter4"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter5"]]["coordinates"]
            i["meter5"]=[i["meter5"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter6"]]["coordinates"]
            i["meter6"]=[i["meter6"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter7"]]["coordinates"]
            i["meter7"]=[i["meter7"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter8"]]["coordinates"]
            i["meter8"]=[i["meter8"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter9"]]["coordinates"]
            i["meter9"]=[i["meter9"],coordinates[0],coordinates[1]]
    
            coordinates = meters_json[i["meter10"]]["coordinates"]
            i["meter10"]=[i["meter10"],coordinates[0],coordinates[1]]

    return meter_to_restaurants_json

meter_loc_resturant()

#################################################
# Flask Setup
#################################################

@app.route("/")
def welcome():
    return render_template("index.html")

# @app.route("/testmeters")
# def objectids():
#     """Return a list of stations."""
#     results = session.query(meters.street_name).all()
#     print(results)
#     street_name = list(np.ravel(results))
#     return jsonify(street_name)

@app.route("/foodtype")
def get_category():
    results = db.session.query(restaurant_yelp.category_title).group_by(restaurant_yelp.category_title).all()
    print(results)
    category = list(np.ravel(results))
    return jsonify(category)

# @app.route('/testrtom')
# def rtom():
#     """Return a list of stations."""
#     results = db.session.query(meter_restaurant.resturant_name).all()
#     print(results)
#     r_name = list(np.ravel(results))
#     return jsonify(r_name)


@app.route("/resturant_stat1")

def stat_typrnum():
    """return restaurant types and count for stat charts"""
    # food_type = session.query(restaurant_yelp.category_title, func.count(restaurant_yelp.category_title)).\
    # group_by(restaurant_yelp.category_title).order_by(func.count(restaurant_yelp.category_title).desc()).all()
    food_type = session.query(restaurant_yelp.category_title, func.count(restaurant_yelp.review_count)).\
    group_by(restaurant_yelp.category_title).order_by(func.count(restaurant_yelp.review_count).desc()).all()
    return jsonify(food_type)

@app.route("/resturant_stat2")
def stat_review():
    "return restaurant types and total review counts for each type"
    sel = [restaurant_yelp.category_title, 
            func.sum(restaurant_yelp.review_count),
            func.avg(restaurant_yelp.review_count)]

    results = session.query(*sel).group_by(restaurant_yelp.category_title).order_by(restaurant_yelp.category_title).all()


    return jsonify(results)


@app.route("/yelpdata")
def restaurant():
    restaurants =[]

    """Return all columns of each restaurant"""
    sel = [restaurant_yelp.name, 
           restaurant_yelp.category_title,
           restaurant_yelp.latitude,
           restaurant_yelp.longitude,
           restaurant_yelp.price, 
           restaurant_yelp.rating,
           restaurant_yelp.review_count,
           restaurant_yelp.display_phone,
           restaurant_yelp.zip_code,
           restaurant_yelp.image_url,
           restaurant_yelp.yelp_id]
    
    results = db.session.query(*sel).all()
    # restaurant = {}
    # Create a dictionary entry for each row of restaurant information
    for result in results:
        restaurant = {}
        restaurant["name"] = result[0]
        restaurant["category_title"] = result[1]
        restaurant["latitude"] = result[2]
        restaurant["longitude"] = result[3]
        restaurant["coordinates"] = (result[2],result[3])
        restaurant["price"] = result[4]
        restaurant["rating"] = result[5]
        restaurant["review_count"] = result[6]
        restaurant["display_phone"] = result[7]
        restaurant["zip"] = result[8]
        restaurant["image_url"] = result[9]
        restaurant["yelp_id"] = result[10]

        restaurants.append(restaurant)
       
    # print(restaurants)
    
    # return jsonify(results)
    return jsonify(restaurants)   

@app.route("/meterdata")
def meter():
    meters_json =[]

    """Return all columns of meter"""
    sel = [meters.objectid, 
           meters.street_num,  
           meters.street_name,
           meters.longitude,
           meters.latitude, 
           meters.meter_type]

    results = db.session.query(*sel).all()

    # Create a dictionary entry for each row of restaurant information
    for result in results:
        meter = {}
        meter["meter_id"] = result[0]
        meter["stree_number"] = result[1]
        meter["street_name"] = result[2]
        meter["address"] = result[1], result[2]
        meter["latitude"] = result[4]
        meter["coordinates"] = (result[4],result[3])
        meter["longitude"] = result[3]
        meter["meter_type"] = result[5]
        

        meters_json.append(meter)
       
    # print(restaurants)
    
    return jsonify(meters_json)   

# @app.route("/mtor")
# def meter_to_restaurants():
#     meter_to_restaurants_json =[]

#     """Return all columns of meter"""
#     sel = [meter_restaurant.yelp_id, 
#            meter_restaurant.resturant_name,
#            meter_restaurant.meter1,
#            meter_restaurant.meter2,
#            meter_restaurant.meter3,
#            meter_restaurant.meter4, 
#            meter_restaurant.meter5,
#            meter_restaurant.meter6,
#            meter_restaurant.meter7,
#            meter_restaurant.meter8,
#            meter_restaurant.meter9,
#            meter_restaurant.meter10,
#            ]

#     results = session.query(*sel).all()

#     # Create a dictionary entry for each row of restaurant information
#     for result in results:
#         meter_to_restaurants = {}

#         meter_to_restaurants["yelp_id"] = result[0]
#         meter_to_restaurants["meter1"] = result[1]
#         meter_to_restaurants["meter2"] = result[2]
#         meter_to_restaurants["meter3"] = result[3]
#         meter_to_restaurants["meter4"] = result[4]
#         meter_to_restaurants["meter5"] = result[5]
#         meter_to_restaurants["meter6"] = result[6]
#         meter_to_restaurants["meter7"] = result[7]
#         meter_to_restaurants["meter8"] = result[8]
#         meter_to_restaurants["meter9"] = result[9]
#         meter_to_restaurants["meter10"] = result[10]
#         meter_to_restaurants["resturant_name"] = result[11]
        
#         meter_to_restaurants_json.append(meter_to_restaurants)
       
#     # print(restaurants)
    
#     return jsonify(meter_to_restaurants_json)  

@app.route("/meterloc")
def meterlocation():
    meterloc=meter_loc_resturant()
    

    return jsonify(meterloc)
    

if __name__ == '__main__':
    app.run(port=8100)
