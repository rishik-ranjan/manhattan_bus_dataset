from flask import Flask, render_template, request, redirect

import numpy as np
import requests
import pandas as pd
import os
import json
import time

from datetime import datetime

path = os.path.realpath(".")

df = pd.DataFrame()
df = pd.read_csv(path+"/manhattan.csv")
df.timestamp = df.timestamp.apply(lambda x: time.mktime(pd.datetime.strptime(x,"%Y-%m-%d %H:%M:%S").timetuple()))
starttime = time.mktime(pd.datetime.strptime("2015-09-13 09:00:00","%Y-%m-%d %H:%M:%S").timetuple())
endtime = time.mktime(pd.datetime.strptime("2015-09-13 12:00:00","%Y-%m-%d %H:%M:%S").timetuple())

ans1 = pd.pivot_table(df.loc[(df.timestamp>=starttime)&(df.timestamp<=endtime),:],\
        values = ["vehicle_id"],index = ["timestamp"], aggfunc=np.count_nonzero)

ans1["timestamp"] = ans1.index
import math

ans1["timesince"] = ans1.index.map(lambda x: math.floor((x-starttime)/60))
ans1 = pd.pivot_table(ans1,values=["vehicle_id"],index=["timesince"],aggfunc=np.sum)
ans1["minutes"]=ans1.index
ans1 = ans1.reset_index(drop=True)

def tojson(df):
    d = [dict([(colname, row[i]) for i,colname in enumerate(df.columns) \
         ]) for row in df.values ]
    return json.dumps(d)

ans1 = tojson(ans1)
app = Flask(__name__)
app.vars = {}

@app.route("/")
def blank():
    return render_template("graph.html",ans1=ans1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
    #app.run(debug=True,port=33507)
