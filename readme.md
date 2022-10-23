# Limit Order Books Simulation Framework

Orders in CLOB have a dynamic distribution that depends on critical level, current market conditions and current price trend [1],[2].

This repo implements a simple framework for generating, visualizing and simulating order fills of a CLOB.

## Features

- The Order Book is implemented by sampling from two distributions:
  - Uniform distributions, representing liquidity which target the whole price range
  - Clustered distributions, representing liquidity concentrated in critical levels. An improvement is estimating realistic position of these clusters following the examples provided in [2].

  Implementing additional distributions (or adding complexity to the current ones) is straightforward as long as there is a mathematical model to follow.

- Order fills are simulated assuming that the price timeseries is an oracle not impacted by the CLOB.

- An initial total liquidity is provided at the beginning of the simulation, additional liquidity is added at each timestep. Liquidity is removed through price fills. 

- The visualization is done through a heatmap of the liquidity evolving over time.

Further improvement to the model and the simulation can be implemented following insights from [3], [4], [5]. 



# Bibliography

- [1] Price clustering on the limit-order book: Evidence from the Stock Exchange of Hong Kong
- [2] https://medium.com/coinmonks/liquidity-and-order-book-distribution-908e4ebd9173
- [3] Simulating Limit Order Book Models - Samuel Watts
- [4] Order book dynamics in liquid markets: limit theorems and diffusion approximations
- [5] Market making behaviour in an order book model and its impact on the bid-ask spread