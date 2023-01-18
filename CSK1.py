import streamlit as st
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import altair as alt
import numpy as np
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt
import base64

st.set_page_config(page_title="CSK aution data Dashboard", page_icon=":bar_chart:", layout="wide")
# ---- SIDEBAR ----
df = pd.read_csv('allyear.csv')
df = df[['Player_name','Team_name','Bid_amount','Is_awarded','Year']]
# df.columns= ['Player name','Team name','Bid amount','Is awarded', 'Year']
st.header("CSK aution data Dashboard")

top_level_menu = st.selectbox("Select a top-level option", ("player wise report", "Team wise report"))

if top_level_menu == "player wise report":
    st.write("You selected player wise report")
    sub_menu = st.selectbox("Select the option", ("Year wise report", "consolidated report"))
    if sub_menu == "Year wise report":

        st.write("You selected Year wise report.")
        Player = st.selectbox(
            "Select the Plyer Name:",
            options=df["Player_name"].unique(),
        )
        #
        a = df.query(
            "Player_name == @Player"
        )
        unique_values = a["Year"].unique()
        Year = st.selectbox(
            "Select the Year:",
            unique_values
        )

        a = a.query(
            "Year == @Year"
        )
        # ---- MAINPAGE ----
        st.title(":bar_chart: CSK auction Dashboard")
        st.markdown("##")
        if a.empty or a['Bid_amount'].isnull().any():
            st.write("No data available for the selected player and year.")
        else:
            x_scale = alt.Scale(domain=[a.Bid_amount.min() - 20, a.Bid_amount.max() + 20])
            b = alt.Chart(a).mark_line(point=True).encode(
                y='Team_name:O',
                x=alt.X('Bid_amount', scale=x_scale, axis=alt.Axis(labelAngle=0)),
                color='Team_name',
                strokeDash='Team_name').properties(width=1000, height=250)
            a = a.groupby('Team_name').agg({'Bid_amount': ['max', 'min', 'count']})
            st.dataframe(a.style.highlight_max(axis=0))
            st.altair_chart(b)

    else:
        st.write("You selected consolidated report.")
        Player = st.selectbox(
            "Select the Plyer Name:",
            options=df["Player_name"].unique(),
        )
        #
        a = df.query(
            "Player_name == @Player"
        )
        a = a.groupby('Year').agg({'Bid_amount': ['max','count']})
        st.dataframe(a.style.highlight_max(axis=0))
        # Reset the index
        a.reset_index(inplace=True)

        # Rename the columns
        a.columns = ['Year', 'max_bid', 'count_bid']
        # Create the line chart
        chart = alt.Chart(a).mark_bar().encode(
            x='Year:N',
            y='max_bid:Q',
        )
        st.altair_chart(chart, use_container_width=True)

else:
    st.write("You selected Team wise report")
    Player = st.selectbox(
        "Select the Team Name:",
        options=df["Team_name"].unique(),
    )
    #
    a = df.query(
        "Team_name == @Player"
    )
    unique_values = a["Year"].unique()
    Year = st.selectbox(
        "Select the Year:",
        unique_values
    )

    a = a.query(
        "Year == @Year"
    )
    if a.empty or a['Bid_amount'].isnull().any():
        st.write("No data available for the selected Team and year.")
    else:
        x_scale = alt.Scale(domain=[a.Bid_amount.min() - 20, a.Bid_amount.max() + 20])
        b = alt.Chart(a).mark_line(point=True).encode(
            y='Player_name:O',
            x=alt.X('Bid_amount', scale=x_scale, axis=alt.Axis(labelAngle=0)),
            color='Player_name',
            strokeDash='Player_name').properties(width=1000, height=250)
        a = a.groupby('Player_name').agg({'Bid_amount': ['max', 'min', 'count']})
        st.dataframe(a.style.highlight_max(axis=0))
        st.altair_chart(b)
