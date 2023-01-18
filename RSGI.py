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

st.set_page_config(page_title="IPL auction Dashboard", page_icon=":bar_chart:", layout="wide")
# ---- SIDEBAR ----

df = pd.read_csv('csk aution data - IPL 2023 AUCTION BID BY BID DET.csv')
df.columns =['Serialno', 'Player_name', 'Team', 'Bid_amount', 'Is_awarded']

st.sidebar.header("Please Filter Here:")

Player = st.sidebar.selectbox(
    "Select the Plyer Name:",
    options=df["Player_name"].unique(),
)

#
a = df.query(
    "Player_name == @Player"
)
df4 = a.groupby(['Team'])['Bid_amount'].agg(['mean', 'std', 'min', 'max'])
df5 = a[a['Is_awarded']== 'Yes']
df5 = df5[['Team','Is_awarded']]
df6 = pd.merge(df4, df5, on=['Team'], how='left')
df6=df6[['Team','min', 'max', 'Is_awarded']]
#
# # a['age'] = this_year - a['year_of_manufacture']
# ---- MAINPAGE ----
st.title(":bar_chart: IPL auction Data")
st.markdown("##")
# Create the box plot
# fig = sns.boxplot(x='Team', y='Bid_amount', data=a, hue='Team')

# y_max = a['Bid_amount'].max()
# # Add a horizontal line at the maximum value
# plt.axhline(y_max, color='r', linestyle='--')
# # Place the legend outside the plot area
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.xticks(rotation=30)
# plt.show()
# st.pyplot(fig)
# b = alt.Chart(a).mark_boxplot(size=50, extent=0.5, outliers={'size': 5}).encode(
#     x='Team:O',
#     y=alt.Y('Bid_amount:Q',scale=alt.Scale(zero=False)),
#     color=alt.Color('Team')
#
# ).properties(width=600,height=450)
# st.altair_chart(b)
#


max_bid = a['Bid_amount'].max()

text = alt.Chart(a).mark_text(
    align='left',
    baseline='middle',
    dx=5,
    dy=-5,
    fontSize=12
).encode(
    x='Team:O',
    y=alt.Y('Bid_amount:Q', scale=alt.Scale(zero=False)),
    text=alt.Text('Bid_amount:Q', format='.2f'),
    color=alt.Color('Team')
).transform_filter(
    alt.datum.Bid_amount == max_bid
)

chart = alt.Chart(a).mark_boxplot(size=50, extent=0.5, outliers={'size': 5}).encode(
    x='Team:O',
    y=alt.Y('Bid_amount:Q',scale=alt.Scale(zero=False)),
    color=alt.Color('Team')
).properties(width=600,height=450)

a= chart + text
st.altair_chart(a)
