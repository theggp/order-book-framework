# Limit Order Books Simulation Framework

Orders in CLOB have a dynamic distribution that depends on historic price levels, market conditions and current price trend [1], [2].

This repository implements a simple framework for generating a CLOB, simulating order fills and visualizing the liquidy distribution.

![Sim2](https://user-images.githubusercontent.com/11960630/197416126-1771c42b-4782-4f7a-8606-7c711d3f558b.png)

## Features

- The Order Book is implemented by sampling from two distributions:
  - Uniform distributions, representing liquidity targeting the whole price range.
  - Clustered distributions, representing liquidity concentrated at critical levels. An improvement is estimating realistic position of these clusters through real historical data.

  Implementing additional distributions (or adding complexity to the current ones) should be straightforward.

- Order fills are simulated assuming that the price timeseries is an oracle not impacted by the CLOB.

- An initial total liquidity is provided at the beginning of the simulation, additional liquidity is added at each timestep. Liquidity is removed through price fills. 

- The visualization is done through a heatmap of the liquidity evolving over time.

Further improvements to the model and the simulation can be implemented following insights from [3], [4], [5]. 


# Bibliography

- [1] Price clustering on the limit-order book: Evidence from the Stock Exchange of Hong Kong
- [2] https://medium.com/coinmonks/liquidity-and-order-book-distribution-908e4ebd9173
- [3] Simulating Limit Order Book Models - Samuel Watts
- [4] Order book dynamics in liquid markets: limit theorems and diffusion approximations
- [5] Market making behaviour in an order book model and its impact on the bid-ask spread
