# import the solidity compiler
from itertools import chain
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

# read the .env file in search of environmental variables
load_dotenv()

# read the SimpleStorage contract
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# this installs the python's solidity compiler for 0.6.0's version of Solidity
install_solc("0.6.0")

# compile SimpleStorage contract with solcx
# specifify language, sources and low-code settings for the compiler to compile
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStrage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
)

# this function creates a json file with the compiled code specifications (abi, evm,...)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStrage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStrage.sol"]["SimpleStorage"]["abi"]

# # for connecting to ganache
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# chain_id = 1337
# my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = os.getenv("PRIVATE_KEY")

# for connecting to rinkeby (using Infura)
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/66e43ded87c747d8bccf191ea3662492")
)
chain_id = 4
my_address = "0x80aF4E8606988365cCd373C1DdF99cE1581E65dE"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the nonce (latest transaction made by address)
nonce = w3.eth.getTransactionCount(my_address)

print("Deploying contract...")

# create/build a transaction (to deploy the contract into the ganache's LOCAL blockchain)
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

# sign a transaction
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

# send a transaction (and deploy the smart contract)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(simple_storage.functions.retrieve().call())

print("Updating contract...")

store_transaction = simple_storage.functions.store(88).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key)
store_tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print("Updated!")

print(simple_storage.functions.retrieve().call())
