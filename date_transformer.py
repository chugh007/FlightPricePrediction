import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
import time

class DateTransformer(BaseEstimator,TransformerMixin):
    def __init__(self):
        pass
    def fit(self,X,y=None):
        return self
    def transform(self,X,y=None):
        newx = X.copy()
        date_attribs = ['Date_of_Journey','Dep_Time','Arrival_Time','Duration']
        newx['Date_of_Journey'] = pd.to_datetime(newx['Date_of_Journey'])
        newx['Date_of_Journey'+'_year'] = time.localtime().tm_year - newx['Date_of_Journey'].dt.year
        newx['Date_of_Journey'+'_month'] = newx['Date_of_Journey'].dt.month
        newx['Date_of_Journey'+'_day'] = newx['Date_of_Journey'].dt.day
        
        newx['Dep_Time'] = pd.to_datetime(newx['Dep_Time'])
        newx['Dep_Time'+'_hour'] = newx['Dep_Time'].dt.hour
        newx['Dep_Time'+'_minute'] = newx['Dep_Time'].dt.minute
        
        newx['Arrival_Time'] = pd.to_datetime(newx['Arrival_Time'])
        newx['Arrival_Time'+'_hour'] = newx['Arrival_Time'].dt.hour
        newx['Arrival_Time'+'_minute'] = newx['Arrival_Time'].dt.minute
        
        newx['Duration_hour'] = newx['Duration'].str.extract(r'(\d+)h').fillna(0)
        newx['Duration_min'] = newx['Duration'].str.extract(r'(\d+)m').fillna(0)
        
        return newx.drop(date_attribs,axis=1)
        