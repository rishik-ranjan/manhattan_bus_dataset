from flask import Flask, render_template, request, redirect

import numpy as np
import requests
import pandas as pd

from datetime import datetime

app = Flask(__name__)

app.vars = {}

@app.route('/')
def blank():
    return render_template('graph.html')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug = True)
    app.run(debug=True,port=33507)
