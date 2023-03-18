from flask import Flask, render_template,request
import requests
import json
from cs50 import SQL 
import pandas as pd
from importnb import imports

db = SQL("sqlite:///covid19-india.sqlite") #connecting the database

app = Flask(__name__)


@app.route('/', methods = ["POST","GET"])
def index():
    states_options = ['West Bengal', 'Telangana', 'Maharashtra', 'Karnataka', 'Goa', 'Delhi']
    data_options = ['Daily Cases', 'Daily Deaths']
    return render_template('base.html', states_options=states_options, data_options=data_options) #displaying the state and data options


@app.route('/graph', methods = ["POST"])
def graph():
    state = request.form['states'] #Getting the selected state
    data = request.form['data'] #Getting the selected datatype
    
    inputquery = {"state" :state, 
                 "data" : data}
   
    outputquerydict = requests.post("http://127.0.0.1:8080/process", json = inputquery).json()  #Getting an appropriate SQL query from the input data
    outputquery = outputquerydict['sqlquery']
    plottingdata = db.execute(outputquery) #Using the SQL query to get the data
    
    inputclean = {"dirtydata" :plottingdata, "datatype" : data}
    
    cleaneddatajson = requests.post("http://127.0.0.1:8080/clean", json = inputclean) #Cleaning the data of null values and sorting them

    cleaneddata = cleaneddatajson.json()['data']

    df = pd.read_json(json.dumps(cleaneddata))
    df.to_csv('data.csv', index = False) #Printing the data to a .csv file
    
    with imports("ipynb"): # type: ignore
        import properties  # type: ignore 

    properties = properties.run() #Running the .ipynb file's run function to get the properties data
    
    datatype = outputquerydict['datatype'] 
    
    return render_template('graph.html', data = cleaneddata, average = properties['average'], minvalue = properties['minvalue'], maxvalue = properties['maxvalue'],
                           mindate = properties['mindate'], maxdate = properties['maxdate'], datatype = datatype) #Using all the data to render the graph
