# Investment Analysis

## Description

This repository contains a simulation tool for investment portfolios. The portfolios can be build with various assets and assigned target ratios. These target ratios can be kept by rebalancing and targeted deposits. Taxes and fees can be set individually for the assets. Predefined analysis plots are available.

## TODOs

- Implement more deposit options

  - DynamicShareSavingPlans
- Wrap Propagation in a Tester class

  - Clear propagation simulation before run
  - Automatically set differnt possible start dates to reduce statistical fluctuation
  - Add function to view results for range of 1(, 2) parameter
- Include more asset classes

  - Commodities
  - Krypto / Currencies
  - P2P-loans
- Bugs/Small things

  - cash_position not 0 at end of simulation
  - auto normalisation
  - redo deposit options
