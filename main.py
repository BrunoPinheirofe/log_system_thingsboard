import psutil
import time
import pprint
import requests
import json
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# URL for Thingsboard API

URL = "http://thingsboard.cloud/api/v1/<ACESS_TOKEN>/telemetry"

ACESS_TOKEN = os.getenv("TOKEN_ACESS")
if not ACESS_TOKEN:
    print("Error: THINGSBOARD_TOKEN environment variable is not set in .env file")
    print("Please create a .env file with THINGSBOARD_TOKEN=your_access_token")
    exit(1)

def sysytem_log():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else None,
        "temperature": psutil.sensors_temperatures().get('coretemp')[0].current
    }

def main():
    while True:
        try:
            log = sysytem_log()
            print(log)
            time.sleep(1)
            
            # Send data to Thingsboard
            response = requests.post(
                URL.replace("<ACESS_TOKEN>", ACESS_TOKEN),
                data=json.dumps(log),
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code == 200:
                pprint.pprint("Data sent successfully")
            else:
                pprint.pprint(f"Failed to send data: {response.status_code}")
        except Exception as e:
            pprint.pprint(f"An error occurred: {e}")
            time.sleep(1)
            continue
        finally:
            # Sleep for 1 second before the next iteration
            time.sleep(1)

if "__main__" == __name__:
    main()