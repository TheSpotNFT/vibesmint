import tweepy
from web3 import Web3
import time
import json

# Set up web3
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR-PROJECT-ID'))

# Set up Twitter API
auth = tweepy.OAuthHandler('CONSUMER_KEY', 'CONSUMER_SECRET')
auth.set_access_token('ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')
api = tweepy.API(auth)

# Load contract ABI from file
with open('abi.json', 'r') as f:
    abi = json.load(f)

# Define contract and event
contract_address = '0xCONTRACT_ADDRESS'
contract = web3.eth.contract(address=contract_address, abi=abi)
mint_event = contract.events.Mint()

# Define function to check for mint events
def check_for_mints():
    block_number = web3.eth.block_number
    past_events = mint_event.getLogs(fromBlock=block_number-10000, toBlock=block_number)
    for event in past_events:
        to_address = event['args']['to']
        tweet = f'{to_address} got sent some gudVibes!'
        api.update_status(tweet)

# Set up Twitter bot to run every 5 minutes
while True:
    check_for_mints()
    time.sleep(300)
