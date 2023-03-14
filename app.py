#CREATE TABLE `Metadata_Tables_Overview` (`table_name` STRING NOT NULL PRIMARY KEY, `state` STRING, `description` STRING);
from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    dropdown1_options = ['Option 1A', 'Option 1B', 'Option 1C']
    dropdown2_options = ['Option 2A', 'Option 2B', 'Option 2C']
    return render_template('base.html', dropdown1_options=dropdown1_options, dropdown2_options=dropdown2_options)