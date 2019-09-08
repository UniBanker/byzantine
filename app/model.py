from peewee import *

db = SqliteDatabase('eth.db')

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db

def to_array(result):
    arr = []
    for r in result:
        arr.append(r)
    return arr

rewardDropBlock1 = 8493120
class SwapCfg():
    @classmethod
    def reward_at_height(self, height):
        if(height < rewardDropBlock1):
            return 5 * 1e8
        return 4 * 1e8

class Wallet(BaseModel):
    ethAddress = CharField(unique=True)
    balance = IntegerField()
    byzAddress = CharField(unique=True)
    @classmethod
    def all(self):
        return self.select()
    @classmethod
    def find_by_byz_address(self, byzAddress):
        return to_array(self.select().where(Wallet.byzAddress % byzAddress))

class Event(BaseModel):
    blockNum = IntegerField()
    amt = CharField()
    ethAddress = CharField()
    byzAddress = CharField()
    totalSwapped = IntegerField(unique=True)
    def __str__(self):
        return f'''
        Block Number: {self.blockNum}
        Amount: {self.amt}
        ETH Address: {self.ethAddress}
        BYZ Address: {self.byzAddress}
        Total Swapped: {self.totalSwapped}
        '''
    @classmethod
    def all(self):
        return self.select().order_by(self.totalSwapped)
    @classmethod
    def find_by_eth_address(self, ethAddress):
        return to_array(self.select().where(Event.ethAddress % ethAddress))
    @classmethod
    def find_by_btc_address(self, btcAddress):
        return to_array(self.select().where(Event.byzAddress % f"BYZ{byzAddress}"))
    @classmethod
    def find_by_byz_address(self, byzAddress):
        return to_array(self.select().where(Event.byzAddress % byzAddress))