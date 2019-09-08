from flask import Flask, escape, request, render_template
from functools import reduce
from model import Event, Wallet, SwapCfg
import json
from playhouse.shortcuts import model_to_dict

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
    byzTotal = 0
    blueTotal = 0
    for evt in res:
        blueTotal += int(evt.amt) / 1e8
        byzTotal += int(evt.amt) * SwapCfg.reward_at_height(evt.blockNum) / 1e8 / 1e8
    def fRes(r):
        return {
                'blockNum': r.blockNum,
                'blueAmt': int(r.amt) / 1e8,
                'byzAmt': int(r.amt) * SwapCfg.reward_at_height(r.blockNum) / 1e8 / 1e8
            }
    res = map(fRes, res)
    return render_template('balance.html', events = res, blueTotal = blueTotal, byzTotal = byzTotal)

# API
@app.route('/api/allEvents')
def all_events():
    return json.dumps(list(map(model_to_dict, Event.all())))

@app.route('/api/allWallets')
def all_wallets():
    return json.dumps(list(map(model_to_dict, Wallet.all())))

@app.route('/api/wallet/<address>')
def wallet_detail(address):
    wallets = Wallet.find_by_byz_address(address)
    events_raw = Event.find_by_byz_address(address)
    def addRewardRatio(evt):
        evt_dict = model_to_dict(evt)
        evt_dict['rewardRatio'] = int(SwapCfg.reward_at_height(evt_dict['blockNum']) / 1e8)
        return evt_dict
    events = map(addRewardRatio, events_raw)
    return json.dumps({
        'wallet': list(map(model_to_dict, wallets)),
        'history': list(events)
    })
