###############################
# This program lets you       #
# - enter values in Streamlit #
# - get prediction            #  
###############################
import pickle
import pandas as pd
import streamlit as st
 
# loading the model
path = ''
modelname = path + '/toymodel.pkl'
loaded_model = pickle.load(open(modelname, 'rb'))

 
      
#############  
# Main page #
#############                
st.write("The model prediction")     
  
LIVINGAPARTMENTS_AVG_MIN = 0.0
LIVINGAPARTMENTS_AVG_MAX = 1.0
APARTMENTS_AVG_MIN = 0.0
APARTMENTS_AVG_MAX = 0.11697126743049956

# Get input values - numeric variables
LIVINGAPARTMENTS_AVG = st.slider('Please enter the living apartments:',
                                 min_value = LIVINGAPARTMENTS_AVG_MIN,
                                 max_value = LIVINGAPARTMENTS_AVG_MAX
                                )
APARTMENTS_AVG = st.slider('Please enter the apartment average:',
                                 min_value = APARTMENTS_AVG_MIN,
                                 max_value = APARTMENTS_AVG_MAX
                                )

# Set dummy variables to zero    
cat_list = ['Accountants', 'Cleaning_staff', 'Cooking_staff',
       'Core_staff', 'Drivers', 'High_skill_tech_staff',
       'Laborers', 'Managers', 'Medicine_staff',
       'OTHER', 'Sales_staff', 'Security_staff']         
for i in cat_list:
       exec("%s = %d" % (i,0)) # The exec() command makes a value as the variable name
               

# Enter data for prediction 
Occupation = st.selectbox('Please choose Your Occupation',
                              ('Accountants',
                               'Cleaning_staff',
                               'Cooking_staff',
                               'Core_staff', 
                               'Drivers', 
                               'High_skill_tech_staff',
                               'Laborers', 
                               'Managers', 
                               'Medicine_staff',
                               'Sales_staff', 
                               'Security_staff',
                               'OTHER')
                             )
               
if Occupation=='Accountants':
        Accountants =1
elif Occupation=='Cleaning_staff':
        Cleaning_staff =1
elif Occupation=='Cooking_staff':
        Cooking_staff =1
elif Occupation=='Core_staff':
        Core_staff =1
elif Occupation=='Drivers':
        Drivers =1
elif Occupation=='High_skill_tech_staff':
        High_skill_tech_staff =1
elif Occupation=='Laborers':
        Laborers =1
elif Occupation=='Managers':
        Managers =1
elif Occupation=='Medicine_staff':
        Medicine_staff =1
elif Occupation=='Sales_staff':
        Sales_staff =1
elif Occupation=='Security_staff':
        Security_staff =1
else: 
        OTHER =1
               
# when 'Predict' is clicked, make the prediction and store it 
if st.button("Get Your Prediction"): 
    
    X = pd.DataFrame({'APARTMENTS_AVG':[APARTMENTS_AVG],
                      'LIVINGAPARTMENTS_AVG':[LIVINGAPARTMENTS_AVG], 
                      'Accountants':[Accountants], 
                      'Cleaning_staff':[Cleaning_staff], 
                      'Cooking_staff':[Cooking_staff],
                      'Core_staff':[Core_staff],
                      'Drivers':[Drivers], 
                      'High_skill_tech_staff':[High_skill_tech_staff],
                      'Laborers':[Laborers], 
                      'Managers':[Managers], 
                      'Medicine_staff':[Medicine_staff],
                      'Sales_staff':[Sales_staff], 
                      'Security_staff':[Security_staff],
                      'OTHER':[OTHER] 
                     })
               
    # Making predictions            
    prediction = loaded_model.predict_proba(X)[:,1] # The model produces (p0,p1), we want p1.

    st.success('Your Target is {}'.format(prediction))
