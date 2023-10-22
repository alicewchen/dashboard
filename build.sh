#!/bin/bash
pip install -r requirements.txt
wget -O data/raw_data/daily_btcusd.csv https://api.dune.com/api/v1/query/3120140/results/csv?api_key=$DUNE_API
wget -O data/raw_data/inscription_by_category.csv https://api.dune.com/api/v1/query/3119563/results/csv?api_key=$DUNE_API
wget -O data/raw_data/btc_fee_size.csv https://api.dune.com/api/v1/query/3119547/results/csv?api_key=$DUNE_API
wget -O data/raw_data/agg_inscription.csv https://api.dune.com/api/v1/query/3119564/results/csv?api_key=$DUNE_API