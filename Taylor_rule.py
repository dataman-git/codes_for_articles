import pandas as pd
import numpy as np

# Consumer Price Index for All Urban Consumers:
CPIAUCSL = pd.read_csv("/Datasets/CPIAUCSL.csv")
# Consumer Price Index for All Urban Consumers: All Items Less Food and Energy in U.S. City Average
CPILFESL = pd.read_csv("/CPILFESL.csv")
# Gross Domestic Product: Implicit Price Deflator 
GDPDEF = pd.read_csv("/GDPDEF.csv")
# Personal Consumption Expenditures: Chain-type Price Index 
PCEPI = pd.read_csv("/PCEPI.csv")
# Real Gross Domestic Product
GDPC1 = pd.read_csv("/GDPC1.csv")
# Potential GDP
GDPPOT = pd.read_csv("/GDPPOT.csv")
# Federal Funds Rate
FEDFUNDS = pd.read_csv("/FEDFUNDS.csv")


# GDP indexes are quarterly. Create monthly data by forward filling
month = CPIAUCSL['DATE']
GDPDEF = pd.merge(month, GDPDEF, left_on = 'DATE', right_on = 'DATE', how='left')
GDPPOT = pd.merge(month, GDPPOT, left_on = 'DATE', right_on = 'DATE', how='left') 
GDPC1 = pd.merge(month, GDPC1, left_on = 'DATE', right_on = 'DATE', how='left')

# Combine all the data
from functools import reduce
dfs = [CPIAUCSL, CPILFESL, GDPDEF, PCEPI, GDPC1, GDPPOT,FEDFUNDS] 
data = reduce(lambda  left,right: pd.merge(left,right,on=['DATE'],how='outer'), dfs)
data = data.fillna(method='ffill') # Forward filling
data = data.dropna( how='any') # drop the NAs of old time periods
data['GDP_gap'] = 100 * (data['GDPC1'] / data['GDPPOT'] -1)
data['DATE'] = pd.to_datetime(data['DATE'], format='%Y-%m-%d').dt.strftime('%Y-%m')
data.index = data['DATE']

# Calculate the rate of inflation from CPI
data['rCPIAUCSL'] = 100 * ( data['CPIAUCSL'] / data['CPIAUCSL'].shift(12) -1 )
data['rCPILFESL'] = 100 * ( data['CPILFESL'] /  data['CPILFESL'].shift(12) -1 )
data['rGDPDEF'] = 100 * ( data['GDPDEF'] /  data['GDPDEF'].shift(12) -1 )
data['rPCEPI'] = 100 * ( data['PCEPI'] /  data['PCEPI'].shift(12) -1 )


# Taylor rule formula
def taylor(inflation):
    data['ff'+inflation] = data[inflation] + 0.5 * data['GDP_gap'] + 0.5 * (data[inflation] - 2) + 2
    return data

inf_list = ['rCPIAUCSL','rCPILFESL','rGDPDEF','rPCEPI']
for inflation in  inf_list:
   taylor(inflation)



import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

data2 = data[['FEDFUNDS','ffrCPIAUCSL', 'ffrCPILFESL', 'ffrGDPDEF', 'ffrPCEPI']]
data2.columns = ['Effective Federal Funds Rate', 
                   'CPI All Urban Consumers',
                   'CPI All Urban Consumers - All Items Less Food and Energy', 
                   'GGP Implicit Price Deflator', 
                   'Personal Consumption Expenditures Price Index']


##################
# Set up sidebar #
##################
# !pip install streamlit
import streamlit as st
import matplotlib.pyplot as plt

st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)


option = st.sidebar.selectbox('Select one inflation index', ( 
                   'CPI All Urban Consumers',
                   'CPI All Urban Consumers - All Items Less Food and Energy', 
                   'GGP Implicit Price Deflator', 
                   'Personal Consumption Expenditures Price Index' ))

import datetime

today = datetime.date.today()
before = today - datetime.timedelta(days=7000)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')


###################
# Set up main app #
###################
# https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
#progress_bar = st.progress(0)

start_date =  pd.to_datetime(start_date, format='%Y-%m-%d').strftime('%Y-%m')
end_date =  pd.to_datetime(end_date, format='%Y-%m-%d').strftime('%Y-%m')

data3 = data2[ (data2.index >= start_date) & (data2.index <= end_date) ]
data4 = data3[ ['Effective Federal Funds Rate', option]]

st.title('The Taylor rule')



import matplotlib.pyplot as plt
f = plt.figure(figsize=(16,8))
ax = data3.plot(kind='line', ax=f.gca(),rot=45,fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(0, 1.2), fontsize = 16)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

st.write(f)



import matplotlib.pyplot as plt
f = plt.figure(figsize=(16,8))
ax = data4.plot(kind='line', ax=f.gca(),rot=45,fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(0, 1.1), fontsize = 16)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

st.write(f)