# ethereum-contract-analysis
Bunch of loose scripts to find new contracts on ethereum created by EOAs with a minimum tx count

1. Use *contracts_created_from_EOAs.sql* in Googles [BigQuery](https://cloud.google.com/bigquery) to find addresses created from EOAs after the specified date.
2. *contract_analysis.py* filters out EOAs that created more than 10 contracts within in the data found in Step 1. It also filters out contracts without verified source
code on Etherscan and contracts that contain a ("transferFrom") function, because I was not interested in token contracts.
3. *post_analysis.py* filters out contracts that have not had a minimum amount of (internal) txs.
