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

def drive_time(row):
  # me = geocoder.ip('me')
  # my_coords = (me.latlng[0], me.latlng[1])
  my_coords = (45, -75)
  destination_coords = (row["latitude"], row["longitude"]) 
  distances = distance.distance(my_coords, destination_coords).km
  driveTime = distances / 60 
  return int(driveTime)

def total_time(row):
  return int(row["wait_time"] + row["drive_time"])

def wait_time(row):
  return int(random.randint(10,300))

@app.route('/') 
@app.route('/main')
def main():
  return render_template('home.html')

@app.route('/application', methods=['GET', 'POST'])
def application(): 
  form = PreferencesForm()
  # button press
  if form.validate_on_submit():

    # Get the variables from the form
    result = request.form
    province = result["province"]
    facility = result["facility"]
    waitTime = int(result["wait_time"]) * 60

    # Get CSV
    df = pd.read_csv('blah.csv') 

    # Filter for hospitals from the requested province and facility type
    df = df[df['province'].str.match(province)] 
    df = df[df['facility_type'].str.match(facility)] 

    # Get rid of null longitudes and latitudes
    df = df[(df['longitude'] != "null")]
    df = df[(df['latitude'] != "null")]

    # Fill out and filter wait time 
    df["wait_time"] = df.apply(wait_time, axis=1)

    # Filter wait time 
    df = df[df['wait_time'] <= waitTime] 

    # Check if the dataframe is empty 
    if len(df) == 0:    
      # Return the template 
      return render_template("application.html", hasNoData=True, form=form, column_names=["Facility Type", "Facility Name", "Province", "Wait Time", "Drive Time", "Total Time"], row_data=list())
    else: 
      # Filling in total time 
      df["drive_time"] = df.apply(drive_time, axis=1)
      df["total_time"] = df.apply(total_time, axis=1)
      del df["index"]
      df=df.sort_values(by=["total_time"]) 
      return render_template("application.html", hasNoData=False, form=form, column_names=["Facility Type", "Facility Name", "Province", "Wait Time", "Drive Time", "Total Time"], row_data=list(df.values.tolist()))
  
  # Get CSV
  df = pd.read_csv('blah.csv') 
  # Fill out wait time and total time 
  df["wait_time"] = df.apply(wait_time, axis=1)
  df["drive_time"] = df.apply(drive_time, axis=1)
  df["total_time"] = df.apply(total_time, axis=1)
  # Delete the index column
  del df["index"]
  # Sort by total time 
  df=df.sort_values(by=["total_time"]) 
  # Return the template 
  return render_template('application.html', hasNoData=False, form=form, column_names=["Facility Type", "Facility Name", "Province", "Wait Time", "Drive Time", "Total Time"], row_data=list(df.values.tolist()))
