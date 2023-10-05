import os
import sys
import time
import json
from web3 import Web3
import IPython


def deploy_test(*args, endpoint="http://127.0.0.1:8545"):
    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = os.path.join(basedir, os.path.pardir)
    build_dir = os.path.join(basedir, 'artifacts', 'contracts')
    contracts = {}

    w3 = Web3(Web3.HTTPProvider(endpoint))
    assert w3.is_connected(), f"Cannot connect to endpoint at {endpoint}"
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.eth.default_account)
    print("Using above address as default account for deployment")

    for filename in args:
        build_path = os.path.join(
            build_dir,
            filename,
            f'{filename.rsplit(".", 1)[0]}.json'
        )
        if not os.path.isfile(build_path):
            print(f'Skipping over "{filename}", cannot locate file at path {os.path.dirname(build_path)}')
            continue 
        with open(build_path, 'r') as file:
            build = json.load(file)
        
        abi = build['abi']
        bytecode = build['bytecode']
        try:
            tx_hash = w3.eth.contract(abi=abi, bytecode=bytecode).constructor().transact()
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            address = tx_receipt.contractAddress
        except Exception as e:
            print(str(e))
            print("See above errors for deployment failure reasons ^^^")
            continue 
        contract = w3.eth.contract(address=address, abi=abi)
        
        contracts[filename] = contract
        print(f'Successfully deployed {filename} at: "{address}"')
    try:
        for idx, name in enumerate(list(contracts.keys())):
            line = f'[{idx}] {name}'
            print(line)
            print(f'{"-" * len(line)}')
        print("The above contracts have been deployed at your endpoint.")
        input("Enter to launch into IPython shell for contract interaction >>> ")
    except KeyboardInterrupt:
        raise SystemExit("Exiting..\nGoodbye!")
    
    print("The variable `contracts` will be a dictionary loaded into the namespace, it contains the names and objects representing your contracts.")
    print("Launching Shell in...")
    launch_in = 3
    while launch_in > 0:
        print(f'...{launch_in}')
        time.sleep(1)
        launch_in -= 1
    time.sleep(0.5)
    IPython.embed()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Missing Solidity Filename args!")
    args = sys.argv[1:]
    endpoint = False
    for a in args:
        if '=' in a:
            arg = a.split('=')
            assert arg[0].lower() == 'endpoint', f'Unrecognized argument: `{arg[0]}`'
            endpoint = arg[1].strip()
            args.remove(a)

    if endpoint:
        deploy_test(*args, endpoint=endpoint)

    else:
        deploy_test(*args)