from web3 import Web3
from app import model

abi = '''[{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"jetTokens","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSwapped","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"tokens","type":"uint256"},{"internalType":"string","name":"btcAddress","type":"string"}],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalSwapped","type":"uint256"},{"indexed":false,"internalType":"string","name":"btcAddress","type":"string"}],"name":"DidSwap","type":"event"}]'''

rewardDropBlock1 = 8493120

class Updater:
    def __init__(self):
        provider = Web3.HTTPProvider("https://mainnet.infura.io:443")
        self.w3 = Web3(provider)
        self.contract = self.w3.eth.contract(address="0x3ADcec93a8bfaCD93C0d6E32d6FEdc2F7E571AB2", abi=abi)
    def blockNumber(self):
        return self.w3.eth.blockNumber
    def eventsFromBlock(self, last_known_event_block):
        events = self.contract.events.DidSwap.getLogs(fromBlock=last_known_event_block, toBlock='latest')
        return events
    def allEvents(self):
        return self.contract.events.DidSwap.getLogs(fromBlock=0, toBlock='latest')

if __name__ == "__main__":
    model.db.connect()
    model.db.create_tables([model.Event, model.Wallet])
    '''wallet_query = model.Wallet.select().where(model.Wallet.byzAddress == 'BYZ3AwzghzPjTwgztn5AHiWNRFokA19rkmWav')
    print(len(wallet_query))
    print(wallet_query.first().totalByz)
    wallet_update = model.Wallet.update(totalByz = wallet_query.first().totalByz+1).execute()
    wallet_query = model.Wallet.select().where(model.Wallet.byzAddress == 'BYZ3AwzghzPjTwgztn5AHiWNRFokA19rkmWav')
    print(wallet_query.first().totalByz)
    print(wallet_update)
    exit(0)'''

    u = Updater()
    events = model.Event.all()
    if len(events) > 0:
        last_known_event_block = events[len(events)-1].blockNum
        print(f'Last block with events: {events[len(events)-1].blockNum}')
        events = u.eventsFromBlock(last_known_event_block + 1)
    else:
        events = u.allEvents()
    for e in events:
        amt = e.args.amount
        try:
            byzAddress = e.args.btcAddress
            ethAddress = e.args['from']
            model.Event.create(
            byzAddress=byzAddress,
            blockNum=e.blockNumber,
            amt=amt,
            ethAddress=ethAddress,
            totalSwapped=e.args.totalSwapped
            )
        except Exception as e:
            print('Event exception')
            print(e)
            pass
        try:
            # Create or get wallet owned by this user
            wallet_query = model.Wallet.select().where(model.Wallet.byzAddress == byzAddress)
            reward = model.SwapCfg.reward_at_height(e.blockNumber) * amt / 1e8
            if(len(wallet_query) < 1):
                # Create new wallet
                model.Wallet.create(
                    byzAddress=byzAddress,
                    ethAddress=ethAddress,
                    balance=reward
                )
            else:
                # Adding to existing amount
                if(byzAddress == "BYZ3AwzghzPjTwgztn5AHiWNRFokA19rkmWav"):
                    print("Found this wallet 3AwzghzPjTwgztn5AHiWNRFokA19rkmWav")
                    print(f"Current balance: {wallet_query.first().balance}")

                    print(f"Adding {reward}")
                model.Wallet.update(
                    balance = wallet_query.first().balance + reward
                ).where(model.Wallet.byzAddress == byzAddress).execute()
        except Exception as e:
            print('Wallet exception')
            print(e)
            pass