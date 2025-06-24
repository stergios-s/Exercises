- Overview:
A single script was created to handle token retrival, order and list of eSIMs.
Debug logs were added and can be disabled by modifying lines 5-7 from airalo.py
On token retrival we check the status code while on order we check status code, order package and order quantity.
Finally in list request we filter the output by order code and package id and we check status code and number of eSIMs found

- How to run py files for task 1
1) Make sure python is installed in your environment. If you don't have a python installed go to this page https://www.python.org/downloads/
   Note: Scripts were developed with python 3.9 and they should work also with the latest version. In case you have any issues running the scripts please install python 3.9 (https://www.python.org/downloads/release/python-3913/)
2) Open a command line and install package 'request' by providing the following command "pip install requests"
3) From a command line navigate to the directory were scripts are located.
4) Use the following command to run the scripts: "python airalo.py"

