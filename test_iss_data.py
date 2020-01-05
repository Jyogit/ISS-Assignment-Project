#! /usr/bin/env python

"""
This program is a collection of pytest TestCases to test & validate
implementation of the API - calculate_iss_speed() which fetches the
ISS data from open-notify API & returns that data in a Pandas DataFrame.

Author: Jyoti C Dingle
"""

# -----------------------------------
# Import required modules.
# -----------------------------------
from extract_json import calculate_iss_speed, output_print_format
import pytest
from pandas.api.types import is_float_dtype, is_integer_dtype
import time

# -----------------------------------
# Define Global Objects
# -----------------------------------
# ISS DataFrame returned by the API.
api_dataframe = None
# List of invalid column entries to be printed in case of failures.
invalid_cols = ['Timestamp','Latitude','Longitude','Distance(km)','Speed(km/hr)']

@pytest.fixture
def exec_params():
    """
    Pass the values of time_duration and polling interval to the API.
    :return: A list with [time_duration, polling_interval] values in seconds.
        Examples:
            return[300,10]
            return[20,5]
    """
    return[60, 5]

@pytest.fixture
def iss_dataframe():
    """
    :return: Pandas DataFrame with ISS data returned by the API
    """
    global api_dataframe
    return api_dataframe

def test_validate_exec_params(exec_params):
    """
    Validate the exec_params (time_duration and polling_interval) before
    passing to the API.
    Populate api_dataframe after executing the API.
    :param exec_params: A list with [time_duration, polling_interval] values in seconds
    """
    global api_dataframe
    print("\n\nTIME_DURATION\t = ", exec_params[0])
    print("POLLING_INTERVAL = ", exec_params[1])
    print_test_message("Validate Execution Parameter values before passing to the API")
    if ((not isinstance(exec_params[0], int)) or (not isinstance(exec_params[1], int))):
        pytest.exit("ERROR: TIME_DURATION, POLLING INTERVAL must be integers.")
    if exec_params[0] <= 0 or exec_params[1] <= 0:
        pytest.exit("ERROR: TIME_DURATION, POLLING INTERVAL must be positive integers.")
    if exec_params[1] >= exec_params[0]:
        pytest.exit("ERROR: TIME_DURATION should not be less than or equal to POLLING_INTERVAL.")
    output_print_format("exec_params validated. Execute the API")
    api_dataframe = calculate_iss_speed(exec_params[0],exec_params[1])

def test_validate_latitude_datatype(iss_dataframe):
    """
    Verify if the datatype of Latitude values in the DataFrame is float &
    print PASS/FAIL messages accordingly.
    :param iss_dataframe: Pandas DataFrame with ISS data returned by the API.
    """
    print_test_message("Verify that datatype of Latitude values in the DataFrame is float.")
    if is_float_dtype(iss_dataframe["Latitude"]):
        print("PASS: Datatype of Latitude values in the DataFrame is float.")
    else:
        print("ERROR: Invalid datatype of one or more Latitude values in the DataFrame.")
        pytest.fail("ERROR: Invalid Latitude datatype.")

def test_validate_longitude_datatype(iss_dataframe):
    """
    Verify if the datatype of Longitute values in the DataFrame is float &
    print PASS/FAIL messages accordingly.
    :param iss_dataframe: Pandas DataFrame with ISS data returned by the API.
    """
    print_test_message("Verify that datatype of Longitude values in the DataFrame is float.")
    if is_float_dtype(iss_dataframe["Longitude"]):
        print("PASS: Datatype of Longitude values in the DataFrame is float.")
    else:
        print("ERROR: Invalid datatype of one or more Longitude values in the DataFrame.")
        pytest.fail("ERROR: Invalid Longitude datatype.")

def test_verify_latitude_range(iss_dataframe):
    """
    Verify if the Latitude values are within the range [-90.0 to 90.0] and
    print PASS/FAIL messages accordingly.
    :param iss_dataframe: Pandas DataFrame with ISS data returned by the API
    """
    global invalid_cols
    print_test_message("Verify that Latitude values in the DataFrame are within the valid range")
    lat_invalid_range = ((iss_dataframe['Latitude'] >= -90.0) & (iss_dataframe['Latitude'] <= 90.0)) == False
    invalid_lat_df = iss_dataframe.loc[lat_invalid_range, invalid_cols]
    if invalid_lat_df.empty:
        print("PASS: Latitude values are within the valid range [-90.0 to 90.0] for all timestamps.")
    else:
        print("ERROR: Latitude values are not within the valid range [-90.0 to 90.0] for following timestamps:")
        print(invalid_lat_df)
        pytest.fail("ERROR: Invalid/Out-of-range Latitude values")

def test_verify_longitude_range(iss_dataframe):
    """
    Verify if the Longitude values are within the range [-180.0 to 180.0] and
    print PASS/FAIL messages accordingly.
    :param iss_dataframe: Pandas DataFrame with ISS data returned by the API
    """
    global invalid_cols
    print_test_message("Verify that Longitude values in the DataFrame are within the valid range")
    lon_invalid_range = ((iss_dataframe['Longitude'] >= -180.0) & (iss_dataframe['Longitude'] <= 180.0)) == False
    invalid_lon_df = iss_dataframe.loc[lon_invalid_range, invalid_cols]
    if invalid_lon_df.empty:
        print("PASS: Longitude values are within the valid range [-180.0 to 180.0] for all timestamps.")
    else:
        print("ERROR: Longitude values are not within the valid range [-180.0 to 180.0] for following timestamps:")
        print(invalid_lon_df)
        pytest.fail("ERROR: Invalid/Out-of-range Longitude values.")

def test_validate_timestamp(iss_dataframe):
    """
    Verify if the datatype of Timestamp values in the DataFrame is integer &
    print PASS/FAIL messages accordingly.
    :param iss_dataframe: Pandas DataFrame with ISS data returned by the API.
    """
    print_test_message("Verify that Timestamps are in valid numeric format")
    if is_integer_dtype(iss_dataframe["Timestamp"]):
        print("PASS: Datatype of Timestamp values in the DataFrame is integer.")
    else:
        print("ERROR: Invalid datatype of one or more Timestamp values in the DataFrame.")
        pytest.fail("ERROR: Invalid Timestamp datatype.")

def test_verify_iss_speed_range(iss_dataframe):
    """
    Verify if the Speed values are within the valid [min .. max] range &
    print PASS/FAIL messages accordingly.
    :param iss_dataframe: Pandas DataFrame with ISS data returned by the API
    """
    global invalid_cols
    print_test_message("Verify that Speed values in the DataFrame are within the valid range.")
    # Drop first row having NaN values.
    iss_dataframe = iss_dataframe.dropna()
    speed_invalid_range = ((iss_dataframe['Speed(km/hr)'] > 0.0) & (iss_dataframe['Speed(km/hr)'] <= 32186.88 )) == False
    invalid_speed_df = iss_dataframe.loc[speed_invalid_range,invalid_cols]
    if invalid_speed_df.empty:
        print("PASS: Speed values are within the valid range [0.0 to 32186.88] km/hr for all timestamps.")
    else:
        print("ERROR: Speed values are not within the valid range [0.0 to 32186.88] km/hr for the following timestamps:")
        print(invalid_speed_df)
        pytest.fail("ERROR: Invalid Speed values.")

def print_test_message(msg):
    """
    Print the testcase summary / title as given in the msg.
    :param msg: Testcase summary / title
    """
    time.sleep(1)
    print("\n\n>>> TESTCASE: {} <<<\n".format(msg))
