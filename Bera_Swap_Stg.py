from web3 import Web3, HTTPProvider, Account
import json
from datetime import datetime, timedelta
import random
from requests import Session
from config import ZERO_ADDRESS, W_BERA, STG_USDC, BEX_W_BERA_STG_USDC_POOL, BEX_ADDRESS, BEX_ABI, HONEY_ADDRESS, HONEY_ABI, ERC20_ABI
    
sess = Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                     'Accept': '*/*'})

class MyHTTPProvider(HTTPProvider):
    def __init__(self, endpoint_uri, session=None, request_kwargs=None):
        super().__init__(endpoint_uri, session, request_kwargs)
        self.session = session

    def set_proxy(self, proxy):
        self.session.proxies.update({'http': proxy, 'https': proxy})

    def make_request(self, method, params):
        self.logger.debug("Making request HTTP. URI: %s, Method: %s",
                          self.endpoint_uri, method)
        request_data = self.encode_rpc_request(method, params)

        response = self.session.post(
            self.endpoint_uri,
            headers=self.get_request_headers(),
            data=request_data,
        )
        response.raise_for_status()

        return self.decode_rpc_response(response.content)


def get_proxies():
    with open("proxies.txt", 'r') as f:
        return [line.strip() for line in f]

proxies = get_proxies()

w3 = Web3(MyHTTPProvider('https://artio.rpc.berachain.com', session=sess))
provider = w3.provider

contract = w3.eth.contract(BEX_ADDRESS, abi=BEX_ABI)

def swap(account):
    address = account.address
    nonce = w3.eth.get_transaction_count(address)
    amount = round(random.uniform(0.001, 0.002), 4) #рандомное значение от 0.0001 до 0.001
    amount_out = int(amount * 10 ** 18) 
    amount_out2= int(amount_out*0.9) 
    route = [(BEX_W_BERA_STG_USDC_POOL, ZERO_ADDRESS, amount_out, STG_USDC, amount_out2, b'')]
    deadline = 99999999
    transaction = contract.functions.batchSwap(0, route, deadline).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 600000,
        'from': address,
        'nonce': nonce,
        'value': amount_out

    })
    transaction.update({'maxFeePerGas': w3.eth.fee_history(w3.eth.get_block_number(), 'latest')['baseFeePerGas'][-1] + w3.eth.max_priority_fee})
    transaction.update({'maxPriorityFeePerGas': w3.eth.max_priority_fee})


    signed_swap_txn = w3.eth.account.sign_transaction(transaction, account.key)
    transaction_hash = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
    return transaction_hash

