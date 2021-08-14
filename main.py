import os
from flask import Flask, render_template, url_for, flash, redirect, request
import numpy as np
import pandas as pd
import geocoder
from geopy import distance
import random 
from forms import PreferencesForm

# global df
# global undeleted
# df = pd.read_csv('med.csv') 
# undeleted = True 

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

# def filterAndClean():

#   global df
#   # global undeleted 

#   # Get rid of null longitudes and latitudes
#   df = df.dropna(subset=['longitude', 'latitude'])

#   # Fill out wait time, drive time, and total time 
#   df["wait_time"] = df.apply(wait_time, axis=1)
#   df["drive_time"] = df.apply(drive_time, axis=1)
#   df["total_time"] = df.apply(total_time, axis=1)

#   # Delete columns
#   # if "index" in list(df.columns.values):
#   # if undeleted:
#   del df["index"]
#   del df["source_facility_type"]
#   del df["provider"]
#   del df["unit"]
#   del df["street_no"]
#   del df["street_name"]
#   del df["postal_code"]
#   del df["city"]
#   del df["source_format_str_address"]
#   del df["CSDname"]
#   del df["CSDuid"]
#   del df["Pruid"]
#     # undeleted = False

#   # Normalize text 
#   df["facility_name"] = df.apply(facility_normalize, axis=1)
#   df["province"] = df.apply(province_normalize, axis=1)

#   # return df

@app.route('/') 
@app.route('/main')
def main():
  return render_template('home.html')

@app.route('/application', methods=['GET', 'POST'])
def application(): 

  # global df

  form = PreferencesForm()

  # button press
  if form.validate_on_submit():

    # Get the variables from the form
    result = request.form
    province = result["province"]
    facility = result["facility"]
    waitTime = int(result["wait_time"]) * 60

    # Get CSV
    df = pd.read_csv('med.csv') 

    # Clean and Filter 
    # filterAndClean()
    print("here koals 1", df)

    # Filter for hospitals from the requested province and facility type
    df = df[df['province'].str.match(province)] 

    print("here koals 2", df)

    df = df[df['odhf_facility_type'].str.match(facility)] 
    print("here koals 3", df)

    # Get rid of null longitudes and latitudes
    df = df.dropna(subset=['longitude', 'latitude'])
    # print("df printed", df)

    # Fill out wait time, drive time, and total time 
    df["wait_time"] = df.apply(wait_time, axis=1)
    df["drive_time"] = df.apply(drive_time, axis=1)
    df["total_time"] = df.apply(total_time, axis=1)

    print("crash here 0", df)
    # Filter and sort total time 
    df = df[df['total_time'] <= waitTime] 
    
    print("crash here 1", df)
    df=df.sort_values(by=["total_time"]) 

    print("crash here 2", df)

    # Check if the dataframe is empty 
    if len(df) == 0:    

      # Return the template 
      return render_template("application.html", hasNoData=True, form=form, column_names=["Facility Type", "Facility Name", "Province", "Wait Time", "Drive Time", "Total Time"], row_data=list())
    
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
      return render_template("application.html", hasNoData=False, form=form, column_names=["Facility Type", "Facility Name", "Province", "Wait Time", "Drive Time", "Total Time"], row_data=list(df.values.tolist()))
  
  # Get CSV
  df = pd.read_csv('med.csv') 

  # Clean and Filter 
  # filterAndClean()

  # Drop rows if they're null in longitude or latitude 
  df = df.dropna(subset=['longitude', 'latitude'])

  # Fill out wait time and total time 
  df["wait_time"] = df.apply(wait_time, axis=1)
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
  return render_template('application.html', hasNoData=False, form=form, column_names=["Facility Type", "Facility Name", "Province", "Wait Time", "Drive Time", "Total Time"], row_data=list(df.values.tolist()))