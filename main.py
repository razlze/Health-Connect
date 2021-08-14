from flask import Flask, render_template, url_for, flash, redirect, request
import numpy as np
import os
import pandas as pd
import geocoder
from geopy import distance
import random 
from forms import PreferencesForm

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

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
  return int(random.randint(60,600))

@app.route('/') 
@app.route('/main')
def main():
  return render_template('home.html')

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
  print("Check")
  return render_template("application.html", hasData=True, column_names=["Facility Type", "Facility Name", "Postal Code", "Wait Time", "Total Time"], row_data=list(filtered.values.tolist()))

@app.route("/preferences", methods=['GET', 'POST'])
def preferences():
  form = PreferencesForm()
  if form.validate_on_submit():
    result = request.form
    print("result", result)
    province = result["province"]
    facility = result["facility"]
    waitTime = int(result["wait_time"])*60
    print("Wait time", waitTime)
    print("Province", province)

    df = pd.read_csv('blah.csv') 

    # Get all hospitals from the requested province, facility type, wait time 
    filtered = df[df['province'].str.match(province)] 
    print("haha 1", filtered)

    filtered = filtered[filtered['facility_type'].str.match(facility)] 
    print("haha 2", filtered)
    # Get all hospitals from the requested wait time 
    filtered["wait_time"] = filtered.apply(wait_time, axis=1)

    print("haha 3", filtered)
    # Get rid of null longitudes and latitudes
    filtered = filtered[(filtered['longitude'] != "null")]
    filtered = filtered[(filtered['latitude'] != "null")]
    filtered = filtered[filtered['wait_time'] <= waitTime] 
    # Filling in wait time (not random we promise) 
    print("wait time before", filtered) 
    # Get all hostpitals with wait times lower than the requested one  
    
    
    print("wait time after", filtered)
    print("num", len(filtered))
    if len(filtered) == 0:
      print("no data")
      return render_template("application.html", hasData=False)
    else: 
      # Filling in total time 
      filtered["total_time"] = filtered.apply(total_time, axis=1)
      print("before deleteing index", filtered)
      del filtered["index"]
      print("after deleteing index", filtered)
      return render_template("application.html", hasData=True, column_names=["Facility Type", "Facility Name", "Postal Code", "Wait Time", "Total Time"], row_data=list(filtered.values.tolist()))
    
  return render_template('preferences.html', title='Preferences', form=form)