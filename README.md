# dashboard

This on-chain analysis offers an overview of the volume and cost associated with Bitcoin Ordinal inscriptions. The fee estimator was created using multiple linear regression (R<sup>2</sup>=0.96) to predict the inscription cost based on the anticipated size and quantity of ordinals to be minted.

Methods:

**Data Collection.** On-chain data and historical BTCUSD prices were downloaded from Dune Analytics Platform in October 2023 after performing SQL queries to fetch the relevant features. 

**Data Processing.** Historical BTCUSD prices were used to convert daily ordinal inscription fees from BTC to USD units. 
