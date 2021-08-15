import os
from flask import Flask, render_template, url_for, flash, redirect, request
import numpy as np
import pandas as pd
import geocoder
from geopy import distance
import random 
from forms import PreferencesForm

global csv_name
csv_name = 'med.csv'

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def drive_time(row):
  # me = geocoder.ip('me')
  # my_coords = (me.latlng[0], me.latlng[1])
  my_coords = (45.420771, -75.698210)
  destination_coords = (row["latitude"], row["longitude"]) 
  driveTime = distance.distance(my_coords, destination_coords).km
  return int(driveTime)

def total_time(row):
  return int(row["wait_time"] + row["drive_time"])

def wait_time(row):
  return int(random.randint(10,300))

def facility_normalize(row):
  return row["facility_name"].lower().title()

def province_normalize(row):
  return row["province"].upper()

@app.route('/') 
@app.route('/main')
def main():
  return render_template('home.html')

@app.route('/application', methods=['GET', 'POST'])
def application(): 

  global csv_name

  # Get the form for the form's data
  form = PreferencesForm()

  # button press
  if form.validate_on_submit():

    # Get the variables from the form
    result = request.form
    province = result["province"]
    facility = result["facility"]
    waitTime = int(result["wait_time"]) * 60

    # Get CSV
    df = pd.read_csv(csv_name) 

    # Filter for hospitals from the requested province and facility type
    df = df[df['province'].str.match(province)] 
    if not facility == "All": df = df[df['odhf_facility_type'].str.match(facility)] 

    # Get rid of null longitudes and latitudes
    df = df.dropna(subset=['longitude', 'latitude'])

    # Fill out wait time, drive time, and total time 
    df["drive_time"] = df.apply(drive_time, axis=1)
    df["total_time"] = df.apply(total_time, axis=1)

    # Filter and sort total time 
    df = df[df['total_time'] <= waitTime] 
    df=df.sort_values(by=["total_time"]) 

    # Check if the dataframe is empty 
    if len(df) == 0:    
      # Return the template 
      return render_template("application.html", hasNoData=True, form=form, column_names=["Facility Type", "Facility Name", "Wait Time", "Drive Time", "Total Time"], row_data=list())
    
    else: 
      # Delete columns
      del df["index"]
      del df["source_facility_type"]
      del df["provider"]
      del df["unit"]
      del df["street_no"]
      del df["street_name"]
      del df["postal_code"]
      del df["city"]
      del df["source_format_str_address"]
      del df["CSDname"]
      del df["CSDuid"]
      del df["Pruid"]

      # Normalize text 
      df["facility_name"] = df.apply(facility_normalize, axis=1)
      df["province"] = df.apply(province_normalize, axis=1)

      # Return the template
      return render_template("application.html", hasNoData=False, form=form, column_names=["Facility Type", "Facility Name", "Wait Time", "Drive Time", "Total Time"], row_data=list(df.values.tolist()))
  
  # Get CSV
  df = pd.read_csv(csv_name) 

  # Drop rows if they're null in longitude or latitude 
  df = df.dropna(subset=['longitude', 'latitude'])

  # Fill out wait time and total time 
  df["drive_time"] = df.apply(drive_time, axis=1)
  df["total_time"] = df.apply(total_time, axis=1)

  # Delete the index column
  del df["index"]
  del df["source_facility_type"]
  del df["provider"]
  del df["unit"]
  del df["street_no"]
  del df["street_name"]
  del df["postal_code"]
  del df["city"]
  del df["source_format_str_address"]
  del df["CSDname"]
  del df["CSDuid"]
  del df["Pruid"]
  
  # Normalize text 
  df["facility_name"] = df.apply(facility_normalize, axis=1)
  df["province"] = df.apply(province_normalize, axis=1)

  # Sort by total time 
  df=df.sort_values(by=["total_time"]) 

  # Return the template 
  return render_template('application.html', hasNoData=False, form=form, column_names=["Facility Type", "Facility Name", "Wait Time", "Drive Time", "Total Time"], row_data=list(df.values.tolist()))