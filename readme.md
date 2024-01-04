# Automation Project: Retreiving GridScape Data from API and Converting it to .CSV

Author: Brandon Pyle and Deipey Panchal

## Purpose
This program was written in order to automate the process of retreiving GridScape data from the API and converting it to .CSV file format. This will allow the data to be collected in a .CSV database and used for PowerBI reports, etc.

## Setting up the Environment: Prerequisites
1. First of all, make sure you have python and IDE installed on your device. Here are the links:
   1. [Python](https://www.python.org/downloads/)
   2. [VSCode](https://code.visualstudio.com/Download) (or any IDE of your choice)

2. Let's also intall a python extension on VSCode for a better experience:
    1. Open VSCode and click on Extensions from the left pane.
    2. Search Python and download the one by Microsoft.

3. Verify python and install required libraries:
   1. Open terminal/command line using an icon in top-right of VSCode *OR* Open Command Prompt (as admin).
   2. Type `python --version`. If this displays the version, it means that we have python installed on our device. Now we can proceed to install required libraries.
   3. Type `pip install requests json csv datetime glob time schedule os` to install all the required libraries for our python program. *OR* We can also install them step by step in this format: `pip install <library name>`.

4. Download the Python script. You can do this from the GitHub repository [here](about:blank).

## Running the Script
1. Run the program by either using the Run button on top-right or with the command `python get_gs_availability_data_grouped.py` in the terminal.
2. You should see some text appear in the terminal describing what the program is currently doing. If the program prints out 'Success!' at the end without encountering any error messages, you will know the script executed properly.
3. You should then see a new .JSON and .CSV file in the same directory as your program. In the future, a new .CSV file will be created only on the first of every month. Each day the program runs the new data will be appended to the end of the current .CSV file.

# Code Explanation
This Python script allows you to extract table data from emails, find "not working" entries, and update an Excel workbook with the extracted data. It opens outlook using pywin32 lib, searches for specific emails from a particular sender, extracts table data from the email content (assumed to be in HTML format), and updates the Excel workbook with the new data. The script also finds rows with "not working" entries in the "Message" column and copies them to a separate sheet in the workbook.

## Dependencies
 - `requests`: This library is used for making HTTP requests to a web API.
 - `csv`: This library is used for creation and modification of .CSV files.
 - `json`: This library is used for creation and modification of .JSON files and data.
 - `datetime`: This library is used for accessing the current time and converting the time to different formats.
 - `glob`: This library is used for getting a list of files in a directory.
 - `schedule`: This library is used to run this script on a schedule once every day
 - `time`: This library is used for the timedelta function that allows subtracting days from dates
 - `os`: This library is used to be able to get the name of the .csv files without the full file path

Please make sure you have these libraries installed before running the script.

## Functions
### `get_json()`
This function fetches the JSON data from the GridScape API using an HTTP GET request and saves it to a .JSON file. If you would like to get different data you can change the url variable to one listed in the [GridScape Documentation](https://exeloncorp-my.sharepoint.com/:b:/r/personal/e187009_exelonds_com/Documents/Documents/Brandon%27s%20Documents/GridScape_Network_Manager_2.4_User_Guide.pdf?csf=1&web=1&e=PUPEib). Note that in the `'Authorization'` section of the `headers` variable, the random string of characters is a Base64 encoded string containing the username and password in the format `EXXXXXX:PASSWORD` where the 'X' characters are the digits of the username and 'PASSWORD' is the user's password. You can use [a base 64 encoder like this](https://www.base64encoder.org) to generate to proper encoded string.

### `read_json()`
This function reads the newly created .JSON file and converts it to JSON string object that is then returned for use in the following function.

### `normalize_json(data: dict)`
This function converts the JSON string to a Python dictionary object and normalizes the data so that it can be easily converted to .CSV format.

### `generate_csv_data(new_data: dict, filename: str)`
This function creates a new .CSV file, writes the table headers to it by reading the JSON dictionary that was created, and then writes the actual JSON data to the file.

### `append_csv_data(new_data: dict)`
This function first checks to see if there are any .CSV files in the same directory as the Python file. If there are none, it simply calls the `generate_csv_data()` function which creates a .CSV file. If there are .CSV files in the current directory, it opens the newest one by sorting the files by the date listed in the name of the file. It then appends the data from the JSON string to the end of the file.

### `job()`
This function creates a variable called `new_data` to hold the JSON data, calls the `get_json()` function to create the .JSON file, and then reads the json data into a new dictionary object by calling the `read_json()` function. After these steps are completed, the program loops through each row in the dictionary, calling the `normalize_json()` function on each one to prepare it for writing to a .CSV file. Once this is complete, the program will eather create a new .CSV file and add the JSON data to it if it is the first of the month, or append the JSON data to the most recent .CSV file. Finally, a success message is printed to confirm that the program has finished executing successfully.

### `main()`
This function handles the scheduling aspect of the program. It creates a schedule to run the `job()` function every day at 11:55pm and checks once every second to see if the current time is 11:55pm.