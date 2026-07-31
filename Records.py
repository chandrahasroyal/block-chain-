from BlockchainFiles.Contract import get_contract

def saveRecords(data, _type):
    web3, contract = get_contract()

    if _type == 'signup':
        tx_hash = contract.functions.setRegister(data).transact({
            'from': web3.eth.accounts[0]
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    elif _type == 'file':
        tx_hash = contract.functions.setFile(data).transact({
            'from': web3.eth.accounts[0]
        })
        web3.eth.wait_for_transaction_receipt(tx_hash)
    elif _type == 'delete':
        tx_hash = contract.functions.addDeleteLog(data).transact({
            'from': web3.eth.accounts[0]
        })
        web3.eth.wait_for_transaction_receipt(tx_hash)
    elif _type == 'recovery':
        tx_hash = contract.functions.addRecoveryLog(data).transact({
            'from': web3.eth.accounts[0]
        })
        web3.eth.wait_for_transaction_receipt(tx_hash)

def updateOwner(id, data, _type):
    web3, contract = get_contract()
    if _type == 'update':
        tx_hash = contract.functions.updateRegister(int(id),data).transact({
            'from': web3.eth.accounts[0]
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)


def getRecords(contract_type):
    web3, contract = get_contract()

    if contract_type == 'signup':
        records = contract.functions.getRegister().call()

        result = []
        for r in records:
            result.append((r[0], r[1]))  # id, data

        return result
    if contract_type == 'file':
        records = contract.functions.getFile().call()

        result = []
        for r in records:
            result.append((r[0], r[1]))  # id, data

        return result
    if contract_type == 'delete':
        records = contract.functions.getDeleteLog().call()

        result = []
        for r in records:
            result.append((r[0], r[1]))  # id, data

        return result
    if contract_type == 'recovery':
        records = contract.functions.getRecoveryLog().call()

        result = []
        for r in records:
            result.append((r[0], r[1]))  # id, data

        return result
