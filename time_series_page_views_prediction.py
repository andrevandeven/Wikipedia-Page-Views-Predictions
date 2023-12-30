# -*- coding: utf-8 -*-
"""Time Series Page Views Prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/147GS7XLrz8bIThZ632DqqLXejHDP_sKM

# Using Prophet Model to Predict Time Series Data: Wikipedia Page Views

We will be forecasting the number of page views for the "Thanksgiving" Wikipedia article in November, with the assistance of a time series model called Prophet.

## Setup
"""

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

"""## Part 1: Preparing Data"""

! wget -nc https://storage.googleapis.com/penn-cis5450/thanksgiving.csv

thanksgiving_df = pd.read_csv("thanksgiving.csv")
thanksgiving_df["Date"] = pd.to_datetime(thanksgiving_df["Date"])

thanksgiving_df = thanksgiving_df.rename(columns={'Date': 'ds', 'Views': 'y'})

start_date = pd.to_datetime('2022-11-01')
df = thanksgiving_df[thanksgiving_df['ds'] < start_date]
thanksgiving_train = thanksgiving_df[thanksgiving_df['ds'] < start_date].reset_index(drop=True)
thanksgiving_test = thanksgiving_df[thanksgiving_df['ds'] >= start_date].reset_index(drop=True)

"""##Part 2: Prophet Model

We will be exploring the Prophet model and comparing **two types of models**; one where we do not account for holidays (Thanksgiving is a U.S. holiday), and one where we do account for holidays.

### 2.1 Prophet Model (Base)
"""

m = Prophet()
m.fit(thanksgiving_train)

future_df = m.make_future_dataframe(periods = 30)
future_df = m.predict(future_df)
future_df = future_df[['ds', 'yhat']]
future_df = future_df[future_df['ds'] >= start_date].reset_index(drop=True)

plt.figure(figsize=(10, 6))
merged_df = future_df.merge(thanksgiving_test, on='ds').sort_values(by='ds')
merged_df['ds'] = merged_df['ds'].dt.strftime('%d')
plt.plot(merged_df['ds'], merged_df['y'], label='Actual')
plt.plot(merged_df['ds'], merged_df['yhat'], label='Predicted')
plt.xlabel('Date')
plt.ylabel('Views')
plt.title("Page Views for Thanksgiving Article (November 2022)")
plt.legend()
plt.show()

"""### 2.2 Prophet Model (Holiday)"""

m = Prophet()
m.add_country_holidays(country_name='US')
m.fit(thanksgiving_train)

future_holiday_df = m.make_future_dataframe(periods = 30)
future_holiday_df = m.predict(future_holiday_df)
future_holiday_df = future_holiday_df[['ds', 'yhat']]
future_holiday_df = future_holiday_df[future_holiday_df['ds'] >= start_date].reset_index(drop=True)

plt.figure(figsize=(10, 6))
merged_df = future_holiday_df.merge(thanksgiving_test, on='ds').sort_values(by='ds')
merged_df['ds'] = merged_df['ds'].dt.strftime('%d')
plt.plot(merged_df['ds'], merged_df['y'], label='Actual')
plt.plot(merged_df['ds'], merged_df['yhat'], label='Predicted')
plt.xlabel('Date')
plt.ylabel('Views')
plt.title("Page Views for Thanksgiving Article (November 2022)")
plt.legend()
plt.show()

"""**Much better!**"""