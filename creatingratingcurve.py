
# coding: utf-8

# In[1]:


# import pandas, os library and get path
import pandas as pd
import os 
os.getcwd()


# In[2]:

# suggesting user to input account username
# read csv file into dataframe 'data'
data = pd.read_csv('/home/mygeohub/inputusernamehere/class1/eaglecreek.csv')
data.head()  # checking data vs csv file for consistency


# In[3]:


timestamp = pd.to_datetime(data.datetime) # convert datetime from format store in csv file to a format for faster processing
discharge_mask = data.discharge.notna()  # when plotting imported data, there appears to be some infs and/or NaN value, this is to make a mask
# to find any cell in discharge that has appropriate value

discharge = data.discharge  # import discharge value for faster processing/plotting
discharge_clean = discharge[discharge_mask]    # eliminate NaN values in discharge
stage_clean = data.stage[discharge_mask]    # import stage value and eliminate existing or non-existing(NaN) value in the same row where we elimiated the discharge value
# since the x and y in later plotting/fitting need to be consistent
timestamp_clean = timestamp[discharge_mask]   # timestamp clean up

# len(stage_clean) == len(discharge_clean)  # a quick double check if needed

# same procedure below to elimiate any leftover NaN value in stage and corresponding rows in the other two column
stage_mask = stage_clean.notna()
stage_final = stage_clean[stage_mask]
discharge_final = discharge_clean[stage_mask]
timestamp_final = timestamp_clean[stage_mask]


# In[4]:


#  cleaned data was sorted since the original values resulted in a zag bag fit (at one point, the)
data_final = pd.concat([stage_final, discharge_final], axis=1)  
data_final = data_final.sort_values(by='stage')   # you can see the effect by commenting this line
data_final.head()


# In[5]:


import matplotlib.pyplot as plt  # import matplotlib library
plt.plot(timestamp_final, discharge_final)   # hydrography/daily series plot and labeling/titling
plt.xlabel('Time (days)')
plt.ylabel('Discharge (cfs)')
plt.title('Discharge Hyrdrography')
plt.savefig('Hyrdrography.png')


# In[6]:


from scipy import optimize    #  import scipy for curve fitting
def test_func(x, a, b):   # function required for fitting
    return a*x**b
params, params_covariance = optimize.curve_fit(test_func, data_final.stage, data_final.discharge, p0=[23, 2.5])  #  optimizing curve fitting, initial values 
# were [2, 2], changed to the current values in hope of a better fitting, other initial values experimented but dropped
print(params)


# In[7]:


plt.scatter(data_final.stage, data_final.discharge, label='Data')    # scatter plot of stage with labels and tittle
plt.xlabel('Stage (ft)')
plt.ylabel('Discharge (cfs)')
plt.title('Stage Discharge Curve for Eagle Creek')

plt.plot(data_final.stage, test_func(data_final.stage, params[0], params[1]), label='Fitted Curve', color='red')    #  curve plotted on top of discrete 
#  value with obtain optimization
plt.legend(loc='best')
plt.savefig('RatingCurve.png')

