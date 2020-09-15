#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

import pandas as pd
import glob
import os

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


# In[3]:


concatenated_df   = pd.read_csv('one.csv',encoding= 'unicode_escape')


# In[4]:


#Converting date object to year month and day
concatenated_df[['Date R']]
#concatenated_df['Date R'] = concatenated_df['Date R'].apply(pd.to_datetime)
concatenated_df['Date R'] = pd.to_datetime(concatenated_df['Date R'],dayfirst = True)
concatenated_df['year'] = concatenated_df['Date R'].dt.year
concatenated_df['month'] = concatenated_df['Date R'].dt.month
concatenated_df['day'] = concatenated_df['Date R'].dt.day
#Converting time object to hour and minutes
concatenated_df['Time R temp'] = concatenated_df['Time R'].apply(pd.to_datetime)
concatenated_df['hour']=concatenated_df['Time R temp'].dt.hour
concatenated_df['minute']=concatenated_df['Time R temp'].dt.minute
concatenated_df['seconds']=concatenated_df['Time R temp'].dt.second
#Adding quarters to dataframe
concatenated_df['Quarter']=4
concatenated_df.loc[concatenated_df['month'] < 4, 'Quarter'] = 1
concatenated_df.loc[(concatenated_df['month'] >= 4) & (concatenated_df['month'] < 7), 'Quarter'] = 2
concatenated_df.loc[(concatenated_df['month'] >= 7) & (concatenated_df['month'] < 10), 'Quarter'] = 3
concatenated_df=concatenated_df.fillna('')
#dropping few columns
concatenated_df.drop(columns=['Time R temp'])
concatenated_df["Time R"] = pd.to_timedelta(concatenated_df["Time R"])
concatenated_df["DateTime"] = concatenated_df["Date R"] + concatenated_df["Time R"]


# In[5]:


#1st subplot
start_date = '11/3/2019'
end_date = '11/5/2019'

df1=concatenated_df[(concatenated_df['Short Text Insp Char'] == 'TANK TEMPERATURE')]
mask = (df1['DateTime'] >= start_date) & (df1['DateTime'] <= end_date)
df1 = df1.loc[mask]

mask = df1['Original Value'].astype(int) >= 12

df_lower=df1[df1['Original Value'].astype(int) <= 12]
df_upper=df1[df1['Original Value'].astype(int) >= 12]
y = df1['QT Result']
x = df1['DateTime']

fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y,name='Original Value',fill='tozeroy'))


fig.add_trace(go.Scatter(x=df1['DateTime'], y=df1['Upp T Limi'], name='Threshold',
                         line = dict(color='firebrick', width=3, dash='dash')))

for index,row in df1.iterrows():
    if int(row['Original Value']) > 12:
        fig.add_annotation(
        x=row['DateTime'],
        y=row['Original Value'],
        xref="x",
        yref="y",
        text="Result:" + row['Result'],
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="red",
        opacity=0.8
        )

fig.update_xaxes(rangeslider_visible=True)

fig.update_layout(title='Temperature Anomaly Detection <br>Unit: °C',hovermode='x unified',
                   xaxis_title='Time',
                   yaxis_title='Original Value',template='plotly_white')

fig.show()


# In[6]:


app = dash.Dash()


app.layout = html.Div(children=[
    html.H1(children='Live dashboard'),
    html.Div(children='Anomaly detection'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': fig,
            'layout':
            go.Layout(title='Order Status by Customer', barmode='stack')
        })
    ])

if __name__ == '__main__':
    app.run_server(port='3000')


# In[ ]:




