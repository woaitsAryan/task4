from flask import Flask, render_template,request
import requests
import json
from cs50 import SQL 
import pandas as pd
from importnb import imports
import datetime

db = SQL("sqlite:///covid19-india.sqlite")

app = Flask(__name__)


@app.route('/', methods = ["POST","GET"])
def index():
    states_options = ['West Bengal', 'Telangana', 'Maharashtra', 'Karnataka', 'Goa', 'Delhi']
    data_options = ['Daily Cases', 'Daily Deaths']
    return render_template('base.html', states_options=states_options, data_options=data_options)


@app.route('/graph', methods = ["POST"])
def graph():
    state = request.form['states']
    data = request.form['data']
    
    inputquery = {"state" :state, 
                 "data" : data}
   
    outputquerydict = requests.post("http://127.0.0.1:8080/process", json = inputquery).json()
    outputquery = outputquerydict['sqlquery']
    plottingdata = db.execute(outputquery)
    
    inputclean = {"dirtydata" :plottingdata, "datatype" : data}
    
    cleaneddatajson = requests.post("http://127.0.0.1:8080/clean", json = inputclean)

    cleaneddata = cleaneddatajson.json()['data']

    df = pd.read_json(json.dumps(cleaneddata))
    df.to_csv('data.csv', index = False)
    
    with imports("ipynb"): # type: ignore
        import properties  # type: ignore

    properties = properties.run()
    #save_file = open("static/data1.json", "w")
    #cleaneddata = eval(str(cleaneddata).replace("\"","'"))
    #json.dump(cleaneddata, save_file,indent = 6)
    #save_file.close()
    
    datatype = outputquerydict['datatype']
    
    return render_template('graph.html', data = cleaneddata, average = properties['average'], minvalue = properties['minvalue'], maxvalue = properties['maxvalue'],
                           mindate = properties['mindate'], maxdate = properties['maxdate'], datatype = datatype)
