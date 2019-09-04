from flask import Flask, escape, request, render_template
from functools import reduce
from model import Event
import json

app = Flask(__name__)

# Website
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    # return str(updater.blockNumber())
    return f'Hello, {escape(name)}!'

@app.route('/<search>')
def index(search):
    res = Event.find_by_eth_address(search)
    sum = 0
    for evt in res:
        sum += int(evt.amt)
    sum /= 1e8
    blueTotal = sum
    byzTotal = 5 * sum
    def fRes(r):
        return {
                'blockNum': r.blockNum,
                'blueAmt': int(r.amt) / 1e8,
                'byzAmt': int(r.amt) * 5 / 1e8
            }
    res = map(fRes, res)
    return render_template('balance.html', events = res, blueTotal = blueTotal, byzTotal = byzTotal)

# API
@app.route('/api/allEventData')
def all_event_data():
    print(f"{len(Event.all())}")
    r = []
    for evt in Event.all().dicts():
        r.append(evt)
    return json.dumps(r)