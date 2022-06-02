-- executed on the publicly available crypto_ethereum dataset on Googles BigQuery
SELECT txs.from_address, transaction_hash, txs.block_timestamp
FROM `bigquery-public-data.crypto_ethereum.traces` as traces JOIN `bigquery-public-data.crypto_ethereum.transactions` as txs
  ON traces.transaction_hash = txs.hash
WHERE txs.to_address IS NULL
  AND traces.block_timestamp > TIMESTAMP('2022-01-01 00:00:00')
  AND traces.trace_type = 'create'