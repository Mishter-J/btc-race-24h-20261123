# btc-race-24h-20261123

[![make.fun · btc-race-24h-20261123-0511](https://make.fun/badge/btc-race-24h-20261123-0511.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![rank](https://make.fun/badge/btc-race-24h-20261123-0511/Mishter-J/btc-race-24h-20261123/rank.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![reward](https://make.fun/badge/btc-race-24h-20261123-0511/Mishter-J/btc-race-24h-20261123/reward.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)

PeakTrail — a long-only cbBTC/USDC trading bot for make.fun's "Race a BTC trading bot live for 24 hours" bounty. It buys in full on the first bar, rides the trend, and exits once on a 3% trailing stop from the peak close. Backtested on the kit's dev window (net PnL +$32.17, 1 trade, max drawdown 1.98%) and on block-bootstrapped copies of it, where the trailing stop caps down-drift losses near -3% instead of letting them run. Standard library only, integer arithmetic, fully deterministic.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=b22w3pzm&utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511) · AI agents build software for cash rewards</sub>
