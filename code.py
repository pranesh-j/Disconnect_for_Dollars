#importing the libraries
import time
import json
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract TimeSpent {
    uint public timeSpent;
    uint public creditsEarned;
    uint public credits;
    uint public time;
    function TimeSpent() public {
        timeSpent = 0;
        creditsEarned = 0;
        credits = 0;
        time = 0;
    }
    function setTimeSpent(uint _timeSpent) public {
        timeSpent = _timeSpent;
        if(timeSpent < 60) {
            creditsEarned = 10;
            credits = credits + creditsEarned;
        }
        else {
            time = timeSpent - 60;
            creditsEarned = 0;
        }
    }
    function getTimeSpent() public constant returns (uint) {
        return timeSpent;
    }
    function getCreditsEarned() public constant returns (uint) {
        return creditsEarned;
    }
    function getCredits() public constant returns (uint) {
        return credits;
    }
    function getTime() public constant returns (uint) {
        return time;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:TimeSpent']

# web3.py instance
w3 = Web3(HTTPProvider('http://localhost:8545'))

# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.timeSpent()))
contract_instance.setTimeSpent(60, transact={'from': w3.eth.accounts[0]})
print('Setting value to: 60')
print('Contract value: {}'.format(contract_instance.timeSpent()))
print('Credits Earned: {}'.format(contract_instance.getCreditsEarned()))
print('Credits: {}'.format(contract_instance.getCredits()))
print('Time: {}'.format(contract_instance.getTime()))
