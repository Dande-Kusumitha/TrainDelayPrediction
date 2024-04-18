import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import speech_recognition as sr
import datetime
from bs4 import BeautifulSoup  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
st.title('Railway Information System')
st.sidebar.title('Menu')
selected = st.sidebar.selectbox('Select an option', ['Home', 'Train ID Info', 'Live Status'])
if selected == 'Home':
    st.image('1.jpg')
if selected == 'Train ID Info':
    
    train_no = st.text_input('Enter the train number')
    if train_no:
        url = "https://indian-railway-irctc.p.rapidapi.com/getTrainId"

        querystring = {"trainno":train_no}

        headers = {
	"x-rapid-api": "rapid-api-database",
	"X-RapidAPI-Key": "d38580d0c7msh98807982e260f4ap115d80jsn4a4f7f74e608",
	"X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
}

        response = requests.get(url, headers=headers, params=querystring)

        data=response.json()
        id=data[0]['id']
        start_station=data[0]['source_name']
        end_station=data[0]['destination_name']
        st.write('Train ID: ', id)
        st.write('Start Station: ', start_station)
        st.write('End Station: ', end_station)
if selected == 'Live Status':
    train_id = st.text_input('Enter the train ID')
    date = st.text_input('Enter the date in the format Tue, 9th Apr')
    url = "https://indian-railway-irctc.p.rapidapi.com/getTrainLiveStatusById"

    querystring = {"id":train_id,"date":date}

    headers = {
	"x-rapid-api": "rapid-api-database",
	"X-RapidAPI-Key": "71923a9a28msh5c0aba50d6d9d6bp18a8cfjsn8486e5d287eb",
	"X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    station_data=data['stations']
    df = pd.DataFrame(station_data)
    text_data = df['source_name'] + ' ' + df['source_name_hi'] + ' ' + df['source_code']
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)
    cos_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    threshold = 0.9  # You can adjust this threshold based on your data
    # Check for delays based on cosine similarity
    for i in range(len(cos_sim)):
        for j in range(i+1, len(cos_sim)):
            if cos_sim[i][j] < threshold:
                st.write(f"Train from {df['source_name'][i]} to {df['source_name'][j]} is delayed.")
                break
            else:
                st.write(f"No delay detected for train from {df['source_name'][i]} to {df['source_name'][j]}.")


