# -*- coding: utf-8 -*- 
from flask import Flask
import json
import pythoncli
app = Flask(__name__)

@app.route("/query/<sentence>")
def hello(sentence):
    output = {'retcode':0, 'errmsg':'', 'data':[]}
    ret = pythoncli.doQuery(sentence)
    output['data'] = ret
    return json.dumps(output)

if __name__ == "__main__":
    app.run()