import streamlit as st
import pandas as pd

import joblib

### Load the trained model from the file
model = joblib.load('pest_model.joblib')

### app title
st.title("Pest Prediction App")

## Load the dataset
data = pd.read_csv('classification_data.csv')

### Build three KPI's for the app
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

### Average rainfall, average temperature, and average soil moisture
with col1:
    st.metric(label="Average Rainfall", value=f"{data['Rainfall_mm'].mean():.2f} mm")
with col2:  
    st.metric(label="Average Temperature", value=f"{data['Temperature_C'].mean():.2f} °C")  
with col3:
    st.metric(label="Average Soil Moisture", value=f"{data['Soil_Moisture'].mean():.2f} %")                                  
    
## User input for the features
## Create a sidebar for user input
st.sidebar.header("Input Features") 

### create a filter for regions
region = st.sidebar.selectbox("Select Region", data['Region'].unique())
### create a filter for crop types
crop_type = st.sidebar.selectbox("Select Crop Type", data['Crop_Type'].unique())

### create a filter for fertilizer use
fertilizer_use = st.sidebar.selectbox("Fertilizer_Use", data['Fertilizer_Used'].unique())

### create a filter for pest presence
pest_presence = st.sidebar.selectbox("Pest Presence", data['Pest_Presence'].unique())

### create a filter for day 
day = st.sidebar.slider("Day", 1, 31, 15)


### Sidebar sliders for numerical features
rainfall = st.sidebar.slider("Rainfall (mm)", float(data['Rainfall_mm'].min()), 
                             float(data['Rainfall_mm'].max()), float(data['Rainfall_mm'].mean()))

### sidebar sliders for temperature
temperature = st.sidebar.slider("Temperature (°C)", float(data['Temperature_C'].min()), 
                                float(data['Temperature_C'].max()), float(data['Temperature_C'].mean()))

### Sidebar sliders for soil moisture
soil_moisture = st.sidebar.slider("Soil Moisture (%)", float(data['Soil_Moisture'].min()), 
                                    float(data['Soil_Moisture'].max()), float(data['Soil_Moisture'].mean()))

### Create a DataFrame for the user input
user_input = pd.DataFrame({
    'Region': [region],
    'Crop_Type': [crop_type],
    'Fertilizer_Used': [fertilizer_use],
    'Pest_Presence': [pest_presence],
    'Day': [day],
    'Rainfall_mm': [rainfall],
    'Temperature_C': [temperature],
    'Soil_Moisture': [soil_moisture]
})

### predict the pest presence using the loaded model
### create a button to trigger the prediction
if st.button("Predict Disease Presence"):
    prediction = model.predict(user_input)
    if prediction[0] == 1:
        st.error("Disease detected! Take necessary actions.")
    else:
        st.success("No disease detected. Keep monitoring your crops!")
        
 