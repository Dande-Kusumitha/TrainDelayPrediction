import requests

url = "https://indian-railway-irctc.p.rapidapi.com/getTrainId"

querystring = {"trainno":"17231"}
def get_train_delay(data, src):
    for station in data['stations']:
        if station['source_name'] == src:
            scheduled_arrival_time_str = station['arrival_time']
            actual_arrival_time_str = station['actual_arrival_time']
            if actual_arrival_time_str and scheduled_arrival_time_str:
                scheduled_arrival_time = datetime.datetime.strptime(scheduled_arrival_time_str, '%H:%M:%S')
                actual_arrival_time = datetime.datetime.strptime(actual_arrival_time_str, '%H:%M:%S')
                delay = actual_arrival_time - scheduled_arrival_time
                return delay.total_seconds() // 60  # Convert delay to minutes
    return None

def get_running_status(data):
    current_time = datetime.datetime.now()
    last_updated_time_str = data['train']['date_updated_full']
    last_updated_time = datetime.datetime.strptime(last_updated_time_str, '%Y-%m-%d %H:%M:%S')
    time_difference = current_time - last_updated_time
    if time_difference.days == 0 and time_difference.seconds < 3600:  # Within the last hour
        return "Train is live"
    else:
        return "Train status is not available"
headers = {
	"x-rapid-api": "rapid-api-database",
	"X-RapidAPI-Key": "f06e160190msh8ded5a07d0faf6cp1345ccjsn39847ea7adb1",
	"X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data=response.json()
id=data[0]['id']
url = "https://indian-railway-irctc.p.rapidapi.com/getTrainLiveStatusById"

querystring = {"id":id,"date":"7th Apr"}

headers = {
	"x-rapid-api": "rapid-api-database",
	"X-RapidAPI-Key": "f06e160190msh8ded5a07d0faf6cp1345ccjsn39847ea7adb1",
	"X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data=response.json()
st.write(data)
import datetime

    
running_status = get_running_status(data)
print(running_status)

source_station = 'GUNTUR JN'
delay = get_train_delay(data, source_station)
if delay is not None:
    print(f"The train is delayed by {delay} minutes at station {source_station}.")
else:
    print(f"No delay information available for station {source_station}.")
