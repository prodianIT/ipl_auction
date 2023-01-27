import streamlit as st
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import altair as alt
import numpy as np
from datetime import date
from collections import Counter
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import base64

st.set_page_config(page_title="CSK aution data Dashboard", page_icon=":bar_chart:", layout="wide")
# ---- MAINPAGE ----
st.title(":bar_chart: CSK auction Dashboard")
st.markdown("##")
df = pd.read_csv('allyear.csv')
df = df[['Player_name','Team_name','Bid_amount','Is_awarded','Year']]
# ---- SIDEBAR ----
top_level_menu = st.selectbox("Select a top-level option", ("Team wise report", "player wise report" ))

if top_level_menu == "Team wise report":
    st.write("You selected Team wise report")
    sub_menu = st.selectbox("Select the option",
                            ("Fav player of a team by year",
                             "team wise speaciality and nationality count"))
    if sub_menu == "Fav player of a team by year":
        st.write("You selected data of Fav player of a team by year.")
        a = df[df['Is_awarded'] == 'Yes']
        Team = st.selectbox(
            "Select the Plyer Name:",
            options=df["Team_name"].unique(),
        )
        #
        a = a.query(
            "Team_name == @Team"
        )
        st.write("You selected the team:",Team)
        # Create sub-dataframes for each year
        df_2018 = a[a['Year'] == 2018]
        df_2019 = a[a['Year'] == 2019]
        df_2020 = a[a['Year'] == 2023]
        df_2021 = a[a['Year'] == 2021]

        # Sort and select top 10 players for each year
        df_2018_top10 = df_2018.sort_values(by='Bid_amount', ascending=False).head(10)
        df_2019_top10 = df_2019.sort_values(by='Bid_amount', ascending=False).head(10)
        df_2020_top10 = df_2020.sort_values(by='Bid_amount', ascending=False).head(10)
        df_2021_top10 = df_2021.sort_values(by='Bid_amount', ascending=False).head(10)

        # Create figure with 2x2 grid of subplots
        fig, axs = plt.subplots(2, 2, figsize=(10, 10))
        axs = axs.ravel()

        # Create pie chart for each sub-dataframe and add it to the grid
        axs[0].pie(df_2018_top10['Bid_amount'], labels=df_2018_top10['Player_name'], autopct='%1.1f%%')
        axs[0].set_title('Top 10 players - 2018')
        axs[1].pie(df_2019_top10['Bid_amount'], labels=df_2019_top10['Player_name'], autopct='%1.1f%%')
        axs[1].set_title('Top 10 players - 2019')
        axs[2].pie(df_2021_top10['Bid_amount'], labels=df_2021_top10['Player_name'], autopct='%1.1f%%')
        axs[2].set_title('Top 10 players - 2021')
        axs[3].pie(df_2020_top10['Bid_amount'], labels=df_2020_top10['Player_name'], autopct='%1.1f%%')
        axs[3].set_title('Top 10 players - 2023')

        st.pyplot(fig)
        df18 = df_2018_top10.Player_name.to_list()
        df19 = df_2019_top10.Player_name.to_list()
        df23 = df_2020_top10.Player_name.to_list()
        df21 = df_2021_top10.Player_name.to_list()
        all_players = df18 + df19 + df23 + df21
        player_counts = Counter(all_players)
        dfa = DataFrame.from_dict(player_counts, orient='index', columns=['count'])
        dfa.reset_index(inplace=True)
        dfa.rename(columns={'index': 'player'}, inplace=True)
        dfa = dfa.sort_values(by="count", ascending=False)
        st.write("Player name and The Number of years they played for",Team )
        st.dataframe(dfa)




    else:
        st.write("You selected team wise speaciality and nationality count")
        Team = st.selectbox(
            "Select the Plyer Name:",
            options=df["Team_name"].unique(),
        )
        #
        a = df.query(
            "Team_name == @Team"
        )
# End of main option 1

#The PLayer wise report section starts here

else:
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
            st.write("The max values are highlighted")
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
        a = a.groupby('Year').agg({'Bid_amount': ['max', 'count']})
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

