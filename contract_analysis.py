import time

import requests as requests
from web3 import Web3
import config
import pandas as pd
import requests

contract_df = pd.read_csv("contracts_created_from_EOAs_2022.csv")

contract_df = contract_df[pd.to_datetime(contract_df["block_timestamp"]) > pd.to_datetime("2022-04-01 00:00:00 UTC")]

df_counts = contract_df["from_address"].value_counts()

df_counts = df_counts[df_counts <= 10]

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{config.INFURA_PROJECT_ID}'))

etherscan_baseurl = "https://api.etherscan.io/api"

# method_signatures = [
#     "23b872dd",  # transferFrom(address,address,uint256), contained both in ERC20 and ERC721
# ]

filtered_contracts = []

for from_address, counts in df_counts.items():
    tx_hashes = contract_df[contract_df["from_address"] == from_address]["transaction_hash"]

    for tx_hash in tx_hashes:

        try:

            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
            contract_address = tx_receipt["contractAddress"]

            response = requests.get(f"{etherscan_baseurl}?module=contract&action=getsourcecode"
                                    f"&address={contract_address}"
                                    f"&apikey={config.ETHERSCAN_API_KEY}").json()

            if response["result"][0]["SourceCode"] == "" or "transferFrom" in response["result"][0]["ABI"]:
                continue

            contract_name = response["result"][0]["ContractName"]

            filtered_contracts.append((contract_name, contract_address))

            time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(1)

    time.sleep(1)

pd.DataFrame(filtered_contracts).to_csv("filtered_contracts.csv")