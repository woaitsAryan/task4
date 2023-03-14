#CREATE TABLE `Metadata_Tables_Overview` (`table_name` STRING NOT NULL PRIMARY KEY, `state` STRING, `description` STRING);
from flask import Flask, render_template,request
import requests
import json
from cs50 import SQL 

db = SQL("sqlite:///covid19-india.sqlite")

app = Flask(__name__)

@app.route('/', methods = ["POST","GET"])
def index():
    dropdown1_options = ['Option 1A', 'Option 1B', 'Option 1C']
    dropdown2_options = ['Option 2A', 'Option 2B', 'Option 2C']
    return render_template('base.html', dropdown1_options=dropdown1_options, dropdown2_options=dropdown2_options)

@app.route('/graph', methods = ["POST"])
def graph():
    dropdown1_value = request.form['dropdown1']
    dropdown2_value = request.form['dropdown2']
    x = f"You selected {dropdown1_value} from dropdown1 and {dropdown2_value} from dropdown2."
    y = db.execute("SELECT date,cases_new FROM WB_case_info")
    print(y)
    print(x)
    
    
    return render_template('graph.html')
    