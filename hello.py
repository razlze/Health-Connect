from flask import Flask, render_template, url_for
import numpy as np
import pandas as pd
import geocoder
from geopy import distance
import random 

app = Flask(__name__)

def total_time(row):
  
  me = geocoder.ip('me')
  print(me.latlng)  

  my_coords = (me.latlng[0], me.latlng[1])
  destination_coords = (row["latitude"], row["longitude"]) 
  distances = distance.distance(my_coords, destination_coords).km
  print(distance.distance(my_coords, destination_coords).km)
  print("type row['wait_time']", type(row["wait_time"]))
  print("type distance/60", type(distances/60))
  totalTime = distances/60 + row["wait_time"]
  return totalTime

def wait_time(row):
  return int(random.randint(10,300))

def convertMinToHour(mins):
  #if 
  return 10

@app.route('/') 
@app.route('/main')
def main():
  path = ["stuff", "more", "ahfjs"]
  return render_template('home.html', path=path)


@app.route('/application')
def application(): 

  # location = request.form["location"]
  path = []

  df = pd.read_csv('blah.csv') 
  print(df)
  # path.append(df)
  # path.append(list(df.columns))
  # path.append(list(df["province"]))
  # path.append(df.head(3))

  filtered = df[df['province'].str.match('Ontario')] 

  # for smthing in filtered:

  filtered["wait_time"] = filtered.apply(wait_time, axis=1)
  print("wait time before", filtered) 
  filtered["total_time"] = filtered.apply(total_time, axis=1)
  print("wait time after", filtered)

  # Delete columns 
  del filtered["index"]
  del filtered["longitude"]
  del filtered["latitude"]

  #index,facility_name,source_facility_type,odhf_facility_type,provider,unit,street_no,street_name,postal_code,city,province,source_format_str_address,CSDname,CSDuid,Pruid,latitude,longitude

  # filtered.filter(items=["facility_name", "odhf_facility_type", "postal_code", "wait_time", "total_time"])
  filtered.filter(items=["facility_name", "facility_type", "province", "wait_time", "total_time"])
  path.append(filtered)   

  print(filtered.values.tolist()) 

  return render_template('application.html', path=path, column_names=["Facility Name", "Facility Type", "Postal Code", "Wait Time", "Total Time"], row_data=list(filtered.values.tolist()))