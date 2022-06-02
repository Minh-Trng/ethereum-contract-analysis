import time

import requests
import config
import pandas as pd

MIN_AMOUNT_TXS = 50
etherscan_baseurl = "https://api.etherscan.io/api"

def has_enough_txs(address):
    txs_response = requests.get(f"{etherscan_baseurl}?module=account&action=txlist&address={address}&startblock=0"
                            f"&endblock=99999999&page=1&offset=100&apikey={config.ETHERSCAN_API_KEY}").json()

    if len(txs_response["result"]) >= MIN_AMOUNT_TXS:
        return True

    internal_txs_response = requests.get(f"{etherscan_baseurl}?module=account&action=txlistinternal&address={address}&startblock=0"
                            f"&endblock=99999999&page=1&offset=100&apikey={config.ETHERSCAN_API_KEY}").json()

    if len(internal_txs_response["result"]) >= MIN_AMOUNT_TXS:
        return True

    return False


if __name__ == "__main__":
    df = pd.read_csv("filtered_contracts.csv")

    result = []

    for index, row in df.iterrows():
        address = row[2]

        try:
            if has_enough_txs(address):
                result.append((row[1], row[2]))
        except:
            continue
        time.sleep(0.2)

    result_df = pd.DataFrame(result)
    result_df.to_csv(f"filtered_contracts_min_{MIN_AMOUNT_TXS}_txs.csv")
