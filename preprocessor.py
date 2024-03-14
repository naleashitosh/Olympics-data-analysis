import pandas as pd
import numpy as np

def processor(data,reg):
    #global data, reg
    # merge dataframe on NOC values
    data = data.merge(reg,on='NOC',how = 'left' )
    # drop duplicates
    data.drop_duplicates(inplace=True)
    # create encoded columns for medal column
    data = pd.concat([data,pd.get_dummies(data.Medal)],axis=1)
    # Filter out the summer season data
    data = data[data.Season == 'Summer']
    return data