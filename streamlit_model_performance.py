# !pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt

# Create some data
df = pd.DataFrame({'state_CA':np.random.randint(low = 40, high=60, size=15),
                   'state_TX':np.random.randint(low = 20, high=30, size=15),
                   'state_NY':np.random.randint(low = 10, high=15, size=15),
                   'volume':np.random.randint(low = 300, high=350, size=15),
                   'pred':np.random.randint(low = 60, high=99, size=15),
                   'TP':np.random.randint(low = 68, high=75, size=15),
                   'TN':np.random.randint(low = 15, high=20, size=15),
                   'FP':np.random.randint(low = 3, high=5, size=15)
                 },
                 index=pd.date_range(start="2019-01-01",end="2020-03-31", freq='M'))
df['FN'] = 100 - df['TP'] - df['TN'] - df['FP']
df.index = df.index.strftime('%Y-%m-%d')

##################
# Plots          #
##################
# Plot 1 #
fig1, ax1 = plt.subplots(figsize=(6,4))
s1 = sns.barplot(x = df.index, y = 'state_CA', data = df, color = 'red',label='state_CA',ax=ax1)
s2 = sns.barplot(x = df.index, y = 'state_TX', data = df, color = 'blue',label='state_TX',ax=ax1)
s3 = sns.barplot(x = df.index, y = 'state_NY', data = df, color = 'green',label='state_NY',ax=ax1)
plt.ylim(0,70)
z, _ = plt.xticks(rotation=90)
plt.legend(ncol=3, loc='best', frameon=True)

# plot 2
fig2, ax2 = plt.subplots(figsize=(6,4))
sns.set(style="whitegrid")
sns.barplot(x=df.index, y="volume", color="b",  data=df, ax=ax2)
z, _ = plt.xticks(rotation=90)


# Plot 3
fig3, ax3 = plt.subplots(figsize=(6,4))
sns.set(style="whitegrid")
sns.lineplot(x=df.index, y="pred", color="b",  data=df, ax=ax3)
plt.ylim(0,100)
z, _ = plt.xticks(rotation=90)

# Plot 4
fig4, ax4 = plt.subplots(figsize=(6,4))
t1 = sns.lineplot(x = df.index, y = 'TP', data = df, color = 'red',label='True Positive',ax=ax4)
t2 = sns.lineplot(x = df.index, y = 'TN', data = df, color = 'blue',label='True Negative',ax=ax4)
t3 = sns.lineplot(x = df.index, y = 'FP', data = df, color = 'green',label='False Positive',ax=ax4)
t4 = sns.lineplot(x = df.index, y = 'FN', data = df, color = 'black',label='False Negative',ax=ax4)
plt.ylim(0,100)
z, _ = plt.xticks(rotation=90)
plt.legend(ncol=2, loc='best', frameon=True)

##################
# Set up sidebar #
##################

option = st.sidebar.write('More functions')

###################
# Set up main app #
###################

col1, col2 = st.beta_columns(2)
col1.header("State")
col1.write(fig1)
col2.header("Volume")
col2.write(fig2)

col3, col4 = st.beta_columns(2)
col3.header("Prediction")
col3.write(fig3)
col4.header("Confusion Matrix")
col4.write(fig4)
