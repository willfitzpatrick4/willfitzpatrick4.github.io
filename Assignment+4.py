
# coding: utf-8

# ---
#
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
#
# ---

# In[1]:



import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
#
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
#
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
#
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
#
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

#Question 1

# In[4]:


with open('university_towns.txt') as f:
    dfu = f.readlines()
dfu


# In[5]:


pd.set_option('display.max_columns', None)

def get_list_of_university_towns():

    with open('university_towns.txt') as f:
        dfu = f.readlines()

    dfu = [line.rstrip('\n') for line in open('university_towns.txt')]

    df = pd.DataFrame(dfu)

    df['RegionName'] = df[0].apply(lambda x: x.split('(')[0].strip() if x.count('[ed')==0 else np.NaN)
    df['State'] = df[0].apply(lambda x: x.split('[ed')[0].strip() if x.count('[ed') > 0 else np.NaN).fillna(method="ffill")
    df = df.dropna().drop(0, axis=1).reindex(columns=['State', 'RegionName']).reset_index(drop=True)
    df = df.set_index('State')

    return df

get_list_of_university_towns()


# In[ ]:

# A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# A recession bottom is the quarter within a recession which had the lowest GDP.
# A university town is a city which has a high percentage of university students compared to the total population of the city.


# In[67]:


'''Returns the year and quarter of the recession start time as a
string value in a format such as 2005q3'''


# In[9]:



df = pd.read_excel('gdplev.xls', skiprows=5)
df = df.drop(df.columns[[0, 1, 2, 3, 5, 7]], axis=1)
df = df.rename(index=str, columns={"Unnamed: 4": "Year & Quarter", "GDP in billions of chained 2009 dollars.1": "GDP"})
df = df.set_index(['Year & Quarter'])
df = df.drop(df.index[:214])


diffs = df.GDP.diff()
df.assign(Change=np.where(diffs > 0, 'increase', np.where( diffs < 0, 'decline', '------')))



# In[65]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''

    return "ANSWER"


# In[ ]:





# In[66]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''

    return "ANSWER"


# In[ ]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''

    return "ANSWER"


# In[ ]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    return "ANSWER"
