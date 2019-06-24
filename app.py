import os

import pandas as pd
import numpy as np
import sqlite3
import pandas 

import requests

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template,request
from flask_sqlalchemy import SQLAlchemy

import seaborn as sns

# Import SQLAlchemy `automap` and other dependencies here
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, Column, Integer, String, update

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

# Add total likes Column
# def add_column(engine, table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(engine.dialect)
#     engine.execute('ALTER TABLE %s ADD %s %s DEFAULT(0)' %(table_name, column_name, column_type))

# column = Column('likes', Integer)
# add_column(engine, 'restaurant_yelp', column)
# restaurant_yelp.update().values({"total_likes": 0})
inspector_obj = inspect(engine)
inspector_obj.get_table_names()
columns = inspector_obj.get_columns('restaurant_yelp')
for column in columns:
    print(column["name"], column["type"])

def meter_loc_resturant():
  
    sel = [meters.objectid, 
           meters.street_num,
           meters.street_name,
           meters.longitude,
           meters.latitude, 
           meters.meter_type]
    meters_json = {}
    results = db.session.query(*sel).all()
    for result in results:
            meter = {}
            meter["coordinates"] = (result[4],result[3])
            meter["meter_id"] = str(result[0])
            meter["steet_num"] = str(result[1])
            meter["steet_name"] = str(result[2])
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
           meter_restaurant.meter10
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
            street_num = meters_json[i["meter1"]]["steet_num"]
            street_name = meters_json[i["meter1"]]["steet_name"]
            i["meter1"]=[i["meter1"],coordinates[0],coordinates[1],street_num + " " + street_name]
            
            coordinates = meters_json[i["meter2"]]["coordinates"]
            street_num = meters_json[i["meter2"]]["steet_num"]
            street_name = meters_json[i["meter2"]]["steet_name"]
            i["meter2"]=[i["meter2"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter3"]]["coordinates"]
            street_num = meters_json[i["meter3"]]["steet_num"]
            street_name = meters_json[i["meter3"]]["steet_name"]
            i["meter3"]=[i["meter3"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter4"]]["coordinates"]
            street_num = meters_json[i["meter4"]]["steet_num"]
            street_name = meters_json[i["meter4"]]["steet_name"]
            i["meter4"]=[i["meter4"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter5"]]["coordinates"]
            street_num = meters_json[i["meter5"]]["steet_num"]
            street_name = meters_json[i["meter5"]]["steet_name"]
            i["meter5"]=[i["meter5"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter6"]]["coordinates"]
            street_num = meters_json[i["meter6"]]["steet_num"]
            street_name = meters_json[i["meter6"]]["steet_name"]
            i["meter6"]=[i["meter6"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter7"]]["coordinates"]
            street_num = meters_json[i["meter7"]]["steet_num"]
            street_name = meters_json[i["meter7"]]["steet_name"]
            i["meter7"]=[i["meter7"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter8"]]["coordinates"]
            street_num = meters_json[i["meter8"]]["steet_num"]
            street_name = meters_json[i["meter8"]]["steet_name"]
            i["meter8"]=[i["meter8"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter9"]]["coordinates"]
            street_num = meters_json[i["meter9"]]["steet_num"]
            street_name = meters_json[i["meter9"]]["steet_name"]
            i["meter9"]=[i["meter9"],coordinates[0],coordinates[1],street_num + " " + street_name]
    
            coordinates = meters_json[i["meter10"]]["coordinates"]
            street_num = meters_json[i["meter10"]]["steet_num"]
            street_name = meters_json[i["meter10"]]["steet_name"]
            i["meter10"]=[i["meter10"],coordinates[0],coordinates[1],street_num + " " + street_name]

    return meter_to_restaurants_json

class Favoritelist(db.Model):
    __tablename__ = 'favoritelist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    foodtype = db.Column(db.String(64))
    price = db.Column(db.String(64))
    rating = db.Column(db.String(64))
    likecount = db.Column(db.Integer)

    def __repr__(self):
        return '<Favorite %r>' % (self.name)
#################################################
# Flask Setup
#################################################

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/map/")
def map():
    return render_template("map.html")
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
           restaurant_yelp.yelp_id,
           restaurant_yelp.address,
           restaurant_yelp.city,
           restaurant_yelp.likes]
    
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
        restaurant["display_phone"] = str(result[7])
        restaurant["zip"] = result[8]
        restaurant["image_url"] = result[9]
        restaurant["yelp_id"] = result[10]
        restaurant['address']=result[11]
        restaurant['city']=result[12]
        restaurant["likes"]=result[13]
        

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

@app.route("/favlist/<yelp_id>", methods=['GET','POST'])
def favoritelist(yelp_id):
    # print("yelp_id: " + yelp_id)
    if request.method == "POST":
        data = request.get_json()
        result = db.session.query(restaurant_yelp).filter(restaurant_yelp.yelp_id==yelp_id).first()
        # result = db.session.query(restaurant_yelp).get(yelp_id)
        result.likes = data["likes"]
        # print(result.likes);
        # db.session.dirty
        db.session.commit()
        # restaurant = {"":"", }
        # db.session.add(pet)
        # db.session.commit()
    return jsonify(status="success", data=data)

        

# @app.route("/meterstatus", methods=['GET','POST'])
# def meterstatus():
#     if request.method == "POST":   
#         metersdata = request.get_json()
#         print(metersdata["meter1"][0], metersdata["meter1"][1], metersdata["meter1"][2])
#         url = 'http://api.sfpark.org/sfpark/rest/availabilityservice?lat=37.7622866993&long=-122.4217428991&radius=0.25&uom=mile&response=json'
#         r = requests.get(url).json()
#         print(r)
       
    
#     return jsonify(status="success", data=metersdata)

if __name__ == '__main__':
    app.run(port=8100)
