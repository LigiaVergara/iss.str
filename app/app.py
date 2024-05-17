import streamlit as st
import requests
import pandas as pd

# --- App Title and Description ---
st.title("Who's in Space Right Now?")
st.markdown("""
This app displays the total number of people currently in space 
and their names, as well as a live map showing the location of the International Space Station.
""")

# --- People in Space Data ---
PEOPLE_IN_SPACE_API = "http://api.open-notify.org/astros.json"

def get_people_in_space():
    response = requests.get(PEOPLE_IN_SPACE_API)
    data = response.json()
    return data["people"]

people = get_people_in_space()

st.subheader(f"Total People in Space: {len(people)}")


people_df = pd.DataFrame(people)
st.write("Names:")
for person in people_df["name"]:
    st.markdown(f"- {person}")

# --- ISS Location Data and Map ---
ISS_LOCATION_API = "http://api.open-notify.org/iss-now.json"

def get_iss_location():
    response = requests.get(ISS_LOCATION_API)
    data = response.json()
    return data["iss_position"]

iss_location = get_iss_location()

st.subheader("International Space Station Location")
st.markdown("The map below shows the current location of the ISS.")

if iss_location:
    df = pd.DataFrame.from_dict(iss_location, orient="index").T
    df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)
    st.map(df, zoom=2)
