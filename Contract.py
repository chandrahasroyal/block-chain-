import json
from web3 import Web3, HTTPProvider
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import pickle
from hashlib import sha256

def get_contract():
    from web3 import Web3
    import json

    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(Web3.HTTPProvider(blockchain_address))

    json_path = r"C:\Users\seela\OneDrive\Desktop\MINI PROJECT\Blockchain-Based Secure Lost Data\SOURCE CODE\Lost_Data_Retrieval\Eth_Blockchain\build\contracts\SmartContract.json"

    with open(json_path) as f:
        contract_json = json.load(f)

    abi = contract_json['abi']
    network_id = list(contract_json['networks'].keys())[0]
    contract_address = contract_json['networks'][network_id]['address']

    contract = web3.eth.contract(
        address=Web3.to_checksum_address(contract_address),
        abi=abi
    )

    return web3, contract
