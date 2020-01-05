#! /usr/bin/env python

"""
This program polls the open-notify API repeatedly to calculate the current
speed of the international space station and prints it to standard output
in a DataFrame format

Author: Jyoti C Dingle
"""

# -----------------------------------
# Import required modules
# -----------------------------------
from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import time

# -----------------------------------
# Define Constants
# -----------------------------------
TIME_DURATION = 15 # seconds
POLLING_INTERVAL = 5 # seconds
RADIUS_OF_EARTH = 6371 # km
AVG_ISS_ALTITUDE = 400 # km

def get_coordinates():
    """ Called internally by calculate_iss_speed()
    This method opens the 'open-notify' url & reads the json response every
    POLLING_INTERVAL seconds for maximum TIME_DURATION specified.
    Populates dictionary with incoming parameter values for following keys,
        - Timestamp
        - Latitude
        - Longitude
    :return: Dictionary with the populated data.
    """
    resp_dict={'Timestamp':[],'Latitude':[],'Longitude':[]}
    start_time = time.time()
    while ((time.time() - start_time) < float(TIME_DURATION)):
        url = ("http://api.open-notify.org/iss-now.json")
        response = urlopen(url)
        obj = json.loads(response.read())
        print("Reading incoming response...", obj)
        if (obj["message"] == "success"):
            resp_dict['Timestamp'].append(obj['timestamp'])
            resp_dict['Latitude'].append(obj['iss_position']['latitude'])
            resp_dict['Longitude'].append(obj['iss_position']['longitude'])
            time.sleep(POLLING_INTERVAL)
    return resp_dict

def cal_distance(resp_df):
    """ Called internally by calculate_iss_speed()
    This method uses the Haversine Formula to calculate the distance
    between 2 consecutive points of ISS positions mentioned in resp_df.
    :param resp_df: Pandas DataFrame with 3 columns,
        - Timestamp
        - Latitude
        - Longitude
    :return: resp_df DataFrame with 5 additional columns,
        - Latitude(Radians)
        - Longitude(Radians)
        - Diff_Lat
        - Diff_Lon
        - Distance(Km)
    """
    # Converting position values from degrees to radians
    resp_df['Latitude'] = resp_df['Latitude'].astype(float)
    resp_df['Longitude'] = resp_df['Longitude'].astype(float)
    resp_df['Latitude(Radians)'] = np.deg2rad(resp_df['Latitude'])
    resp_df['Longitude(Radians)'] = np.deg2rad(resp_df['Longitude'])

    # Calculate diff between current & last point.
    resp_df['Diff_Lat'] = resp_df['Latitude(Radians)'].diff(+1)
    resp_df['Diff_Lon'] = resp_df['Longitude(Radians)'].diff(+1)

    # Haversine Formula
    # a is the square of half the chord length between the points.
    a = np.sin(resp_df['Diff_Lat'] / 2)**2 + np.cos((resp_df['Latitude(Radians)'].shift())) * np.cos(resp_df['Latitude(Radians)']) * np.sin(resp_df['Diff_Lon']/ 2)**2

    # c is the angular distance in radians.
    c = 2 * np.arcsin(np.sqrt(a))

    # Calculate the distance between successive points
    resp_df['Distance(km)'] = c * (RADIUS_OF_EARTH + AVG_ISS_ALTITUDE)
    return resp_df

def output_print_format(output_var):
    """
    Print the output_var text to STDOUT in a structured format
    :param output_var: text string to be printed
    """
    print("--------------------------------------------------------------------------------------")
    print("\n\t\t-------- {} --------\n".format(output_var))
    print("--------------------------------------------------------------------------------------")

# -----------------------------------
# MAIN
# -----------------------------------
def calculate_iss_speed(time_duration = None, polling_interval = None):
    """
    The main API that collects the ISS data and,
        - calculates the speed between two successive ISS positions
        - calculates average speed of ISS & prints it to STDOUT
    :param time_duration: Total time duration to fetch the data from open-notify API
    :param polling_interval: Time duration between two successive readings from open-notify API
    """
    global TIME_DURATION
    global POLLING_INTERVAL
    if time_duration: TIME_DURATION = time_duration
    if polling_interval: POLLING_INTERVAL = polling_interval
    coord_dict = get_coordinates()

    # Convert dictionary to DataFrame.
    resp_df = pd.DataFrame.from_dict(coord_dict)
    cal_distance(resp_df)

    # Calculate Speed of ISS between 2 consecutive positions
    resp_df['Speed(km/hr)']= resp_df['Distance(km)']/(POLLING_INTERVAL/3600)

    # Saving the DataFrame to csv file.
    file_ts = time.time()
    file_name = str(int(file_ts)) + "_iss_data.csv"
    resp_df.to_csv(file_name)
    Average_Speed = resp_df['Speed(km/hr)'].mean()

    output_print_format("Response DataFrame")
    print(resp_df)
    output_print_format("Average Speed of ISS is {} km/hr".format(round(Average_Speed, 6)))
    return resp_df
