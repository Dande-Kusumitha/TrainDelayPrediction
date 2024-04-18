import requests
import pandas as pd
pnr=input("Enter your PNR number: ")
url = "https://pnr-status-indian-railway.p.rapidapi.com/pnr-check/"+pnr
headers = {
	"X-RapidAPI-Key": "f4fea6f826msh5e9a447377e0015p138b15jsnf9caa24e1e6e",
	"X-RapidAPI-Host": "pnr-status-indian-railway.p.rapidapi.com"
}
response = requests.get(url, headers=headers)

data =response.json()
# Extracting relevant data for route details
train_routes = data['data']['trainRoutes']
df_route_data = []
for route in train_routes:
    df_route_data.append([
        route['stationCode'],
        route['stationName'],
        route['arrivalTime'],
        route['departureTime'],
        route['haltTime'],
        route['travellingDay'],
        route['distance'],
        route['platform']
    ])

# Creating DataFrame for route details
route_columns = ['Station Code', 'Station Name', 'Arrival Time', 'Departure Time', 'Halt Time', 'Travelling Day', 'Distance', 'Platform']
df_route = pd.DataFrame(df_route_data, columns=route_columns)

# Extracting relevant data for passenger details
passenger_info = data['data']['passengerInfo']
df_passenger_data = []
for passenger in passenger_info:
    df_passenger_data.append([
        passenger['currentCoach'],
        passenger['currentBerthNo']
    ])

# Creating DataFrame for passenger details
passenger_columns = ['Current Coach', 'Current Berth']
df_passenger = pd.DataFrame(df_passenger_data, columns=passenger_columns)

print("Route Details DataFrame:")
print(df_route)
print("\nPassenger Details DataFrame:")
print(df_passenger)
