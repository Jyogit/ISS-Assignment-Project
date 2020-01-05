ISS Assignment Project:
=======================

Files:
------
	1. extract_json.py - Python module file with the main API calculate_iss_speed()
	2. test_iss_data.py - Pytest testcase file with the Testcases
	3. iss_testcase_execution.log – Testcase execution log
	4. 1578250871_iss_data.csv – ISS DataFrame saved in csv file after execution.
	5. Testcase_Document.xlsx – List & details of the Testcases

Execution Instructions:
----------------------
	- Download extract_json.py, test_iss_data.py in a directory.
	- Install required python modules as mentioned in import section of both the files as needed (Ex: json, pandas, numpy, pytest etc.)
	- Refer testcase document “Testcase_Document.xlsx” for details of each testcase.
	- In test_iss_data.py use pytest fixture exec_params() to pass [time_duration, polling_interval] to the API. The default values are [60, 5]
	- Open execution console and navigate to the directory containing the testcase file.

Execution Command:
------------------
	$ pytest test_iss_data.py –s

The execution traces on the STDOUT should be displayed similar to that in “iss_testcase_execution.log”

At the end of the execution a csv file will be created with ISS data, similar to “1578250871_iss_data.csv”

Notes:
------
	- IDE used for development: PyCharm
	- Test Framework: pytest
	- Execution Console: Windows PowerShell, PyCharm
