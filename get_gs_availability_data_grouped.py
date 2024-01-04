import requests
import json
import csv
from datetime import date, datetime, timedelta
import glob
import schedule
import time
import os

def get_json():
    print("Fetching JSON data...")
    
    todate = datetime.now().isoformat()
    fromdate = (datetime.now() + timedelta(days = -1)).isoformat()
    
    url = "https://dem.prod01.bge.ssnsgs.net:8043/da/api/report/availability/fromdate/" + fromdate + "/todate/" + todate + "/limit/5000000/offset/0/states/ACTIVE,MAINTENANCE/usecurrentstate/false/failedonly/false/groupresults/true"
    print(url)
    payload = {}

    headers = {
      'Authorization': 'Basic ZTE4NzAwOTpEYXZpZDQyNDEyMDAyJCNAIQ==',
      'Cookie': 'JSESSIONID=17B96EEB9418E453F1617335C72317D0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = json.loads(response.text)
        with open(str(date.today()) + '_gs_availability_data_grouped.json', 'w') as f:
            json.dump(data, f)
        print("JSON data fetched successfully.")
    else:
        print(f"There was an error. Code {response.status_code}")

def read_json() -> dict:
    print("Reading JSON data...")
    
    try: 
        with open(str(date.today()) + '_gs_availability_data_grouped.json', "r") as f: 
            data = json.loads(f.read()) 
    except: 
        raise Exception("Reading" + str(date.today()) + "_gs_availability_data_grouped.json file encountered an error") 
  
    return data['results']

def normalize_json(data: dict) -> dict: 
    new_data = dict() 
    for key, value in data.items(): 
        if not isinstance(value, dict): 
            new_data[key] = value 
        else: 
            for k, v in value.items(): 
                new_data[key + "_" + k] = v 
  
    return new_data

def generate_csv_data(new_data: dict, filename: str):
    print("Converting JSON data to CSV...")
    
    csv_file = open('./gs_availability_data_grouped/' + filename, 'w', newline = '')
    csv_writer = csv.writer(csv_file)

    count = 0

    for data in new_data:
        data['date'] = str(datetime.now())
        
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1

        csv_writer.writerow(data.values())

    csv_file.close()

def append_csv_data(new_data: dict):
    files = list(map(os.path.basename, glob.glob("C:/Users/E187009/OneDrive - Exelon/Documents/Python/gs_availability_data_grouped/**/*.csv", recursive = True)))

    print(len(files))

    if len(files) == 0:
        print("No CSV files exist to append to, creating a new one...")
        csv_data = generate_csv_data(new_data, str(date.today().year) + "-" + str(date.today().month) + "_gs_availability_data_grouped.csv")
    else:
        print("Converting JSON data to CSV...")
        files = [files_short[:7] for files_short in files]
        max(files, key= lambda d: datetime.strptime(d, '%Y-%m'))

        csv_file = open('./gs_availability_data_grouped/' + files[len(files) - 1] + '_gs_availability_data_grouped.csv', 'a')
        csv_writer = csv.writer(csv_file)

        count = 0

        for data in new_data:
            data['date'] = str(datetime.now())
            csv_writer.writerow(data.values())

        csv_file.close()

def job():
    print("**************************************************************")
    print(f"* {str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))} - Getting GridScape Availability Data (Grouped) *")
    print("**************************************************************")
    
    new_data = []

    get_json()

    data = read_json()

    for i in range(len(data)):
        new_data.append(normalize_json(data[i]))

    if date.today().day is 1:
        csv_data = generate_csv_data(new_data, str(date.today().year) + "-" + str(date.today().month) + "_gs_availability_data_grouped.csv")
    else:
        csv_data = append_csv_data(new_data = new_data)

    print("Success!")


def main():
    schedule.every().day.at("23:55").do(job)

    while True: 
        schedule.run_pending()
        time.sleep(1)
#    job()

if __name__ == "__main__":
    main()
