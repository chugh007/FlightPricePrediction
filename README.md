# FlightPricePrediction
Predicts price of the flight

* Application Demo : https://flight-price-prediction-appli.herokuapp.com
* Dataset : https://www.kaggle.com/nikhilmittal/flight-fare-prediction-mh/
* Metric Used : Mean squared error

## Implementation Notes

* Sklearn pipelines are used to automate preprocessing , feature selection and model building
* The final pipeline is saved on the disk and loaded again in the flask application for making predictions

## Demo

![alt text](https://github.com/chugh007/FlightPricePrediction/blob/master/images/demo1.png?raw=true)

![alt text](https://github.com/chugh007/FlightPricePrediction/blob/master/images/demo2.png?raw=true)


## Setup

Setting it up in local is very easy , just follow the steps listed below

* virtualenv venv 
* source venv/bin/activate
* pip install -r requirements.txt
* python app.py

