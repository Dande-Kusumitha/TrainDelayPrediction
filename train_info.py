import requests
import pandas as pd
url = "https://trains.p.rapidapi.com/"

payload = { "search": "17214" }
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "f4fea6f826msh5e9a447377e0015p138b15jsnf9caa24e1e6e",
	"X-RapidAPI-Host": "trains.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

data=response.json()
# Extracting necessary data
train_num = data[0]['train_num']
name = data[0]['name']
days = ', '.join([day for day, runs in data[0]['data']['days'].items() if runs == 1])
classes = ', '.join(data[0]['data']['classes'])

# Create DataFrame
df = pd.DataFrame({
    'Train Name': [name],
    'Days': [days],
    'Classes': [classes],
})

print(df)