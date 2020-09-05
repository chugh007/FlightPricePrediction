from flask import Flask,render_template,request
import json
import joblib
import pandas as pd
import os
import numpy as np
#from date_transformer import DateTransformer




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
        
app = Flask(__name__)
model_folder = "model"
model_name = "best_model.pkl"
model_path = os.path.join(model_folder,model_name)
@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    columns = ['Airline', 'Date_of_Journey', 'Source', 'Destination','Route',
       'Dep_Time', 'Arrival_Time', 'Duration', 'Total_Stops','Additional_Info']
    params = {}
    for c in columns:
        if c == 'Route':
            params[c]= 'blabla'
        elif c == 'Duration':
            hour_diff = abs(int(params['Arrival_Time'].split(':')[0]) - int(params['Dep_Time'].split(':')[0]))
            min_diff = abs(int(params['Arrival_Time'].split(':')[-1]) - int(params['Dep_Time'].split(':')[-1]))
            params[c] = "{}h {}m".format(hour_diff,min_diff)
        elif c== 'Additional_Info':
            params['Additional_Info'] = 'No info'
        else:
            params[c] = request.form.get(c)
    
    online_df = pd.DataFrame.from_dict([params])
    print(online_df.columns)
    model = joblib.load(model_path)
    pred_price = model.predict(online_df)
    print(pred_price)
    params['pred_price'] = pred_price[0]
    return render_template("index.html",prediction_text="Rs "+str(np.round(params['pred_price'],2)))


if __name__ == "__main__":
    app.run()