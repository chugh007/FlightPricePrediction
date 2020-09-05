from flask import Flask,render_template,request
import json
import joblib
import pandas as pd
import os
import numpy as np
from date_transformer import DateTransformer

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