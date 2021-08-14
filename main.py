from flask import Flask, render_template, url_for
import numpy as np
import pandas as pd
import geocoder
from geopy import distance
import random 

app = Flask(__name__)

def total_time(row):
  me = geocoder.ip('me')
  # print(me.latlng)  
  my_coords = (me.latlng[0], me.latlng[1])
  destination_coords = (row["latitude"], row["longitude"]) 
  distances = distance.distance(my_coords, destination_coords).km
  # print(distance.distance(my_coords, destination_coords).km)
  # print("type row['wait_time']", type(row["wait_time"]))
  # print("type distance/60", type(distances/60))
  totalTime = distances/60 + row["wait_time"]
  return totalTime

def wait_time(row):
  return int(random.randint(10,300))

@app.route('/') 
@app.route('/main')
def main():
  path = ["stuff", "more", "ahfjs"]
  return render_template('home.html', path=path)

@app.route('/application')
def application(): 

  # location = request.form["location"]
  df = pd.read_csv('blah.csv') 
  print(df)
  # path.append(df)
  # path.append(list(df.columns))
  # path.append(list(df["province"]))
  # path.append(df.head(3))

  filtered = df[df['province'].str.match('')] 
  filtered = filtered[(filtered['longitude'] != "null")]
  filtered = filtered[(filtered['latitude'] != "null")]
  print("after cleaning", filtered) 

  filtered["wait_time"] = filtered.apply(wait_time, axis=1)
  print("wait time before", filtered) 
  filtered["total_time"] = filtered.apply(total_time, axis=1)
  print("wait time after", filtered)

  # Delete columns 
  # del filtered["index"]
  # del filtered["longitude"]
  # del filtered["latitude"]

  # filtered.filter(items=["facility_name", "odhf_facility_type", "postal_code", "wait_time", "total_time"])
  filtered.filter(items=["facility_type", "facility_name", "province", "longitude", "latitude", "wait_time", "total_time"])
  del filtered['index']
  print("filtered HERE\n", filtered) 

  print("filtered.values.toList()", filtered.values.tolist())   

  return render_template('application.html', column_names=["Facility Type", "Facility Name", "Postal Code", "Wait Time", "Total Time"], row_data=list(filtered.values.tolist()))