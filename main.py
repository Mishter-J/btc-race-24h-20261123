"""PeakTrail: a long-only cbBTC/USDC trading bot for make.fun's bars-replay/v1.

Strategy (chosen after backtesting the kit's dev window plus block-bootstrapped
copies of it, and the same window with its drift flipped):

  * Buy the full cash balance on the first tradable bar. The dev window is a
    slow grind up with one big two-hour rally; every timing rule I tried on
    1-minute bars (EMA crosses, Donchian breakouts, dip-buying) lost money to
    whipsaw: a full round trip costs ~26 bps in fees, slippage and price
    impact, while the 1-minute return noise is only ~8 bps. Being long from
    the start captures the drift; active timing mostly pays the spread.
  * Hold, tracking the highest close seen while holding.
  * Exit everything, once, when a bar closes 3% or more below that peak
    close (a trailing stop). On the dev window the peak-to-trough drawdown
    is 1.98%, so the stop never fires there; on bootstrapped windows with
    the drift removed or flipped it caps the loss near -3% instead of
    letting a downtrend run to -10%, and in up-drift windows it costs
    almost nothing (it fires rarely). The exit is final: no re-entry.
    Re-entering after a stop-out tested worse in every regime, because
    re-entries buy dead-cat bounces in downtrends and pay the round-trip
    cost again.
  * At most two filled orders in a run (one buy, one sell), plus the
    harness's own flatten at the end if still holding. Fewer trades also
    wins the net-PnL tie-break.

Implementation notes: integer arithmetic only, no randomness, no clock,
no environment reads, so the two graded executions produce identical
action logs. Orders are re-sent until their fill is confirmed in the
account the next batch carries (a buy or sell the market rejects for
slippage is retried on the next bar). max_slippage_bps is 200: the
largest 1-minute move on the dev window is 0.72%, so 2% leaves room for
gaps while still refusing a fill far past the close the order was
decided on.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

#: The most an order may fill past the close it was decided on (basis points).
MAX_SLIPPAGE_BPS = 200
#: Trailing stop: sell when close * 100 < peak * 97, i.e. 3% below the peak close.
TRAIL_NUMERATOR = 97
TRAIL_DENOMINATOR = 100
#: Smallest buy the harness accepts (fees.min_notional_quote_units), in quote units.
MIN_NOTIONAL = 1_000_000

_symbol = None
_peak = None
_exiting = False
_exited = False


def on_hello(state):
    global _symbol
    _symbol = state.hello["symbols"][0]["symbol"]


def on_batch(state, batch):
    global _peak, _exiting, _exited
    if state.warming_up:
        return []
    close = state.close(_symbol)
    if close is None:
        return []
    held = state.positions.get(_symbol)
    if held is not None:
        if _peak is None or close > _peak:
            _peak = close
        if _exiting or close * TRAIL_DENOMINATOR < _peak * TRAIL_NUMERATOR:
            # Sell the whole position. _exiting stays set until a batch
            # shows the position gone, so a rejected sell is retried.
            _exiting = True
            return [{"side": "sell", "symbol": _symbol, "qty": held.qty,
                     "max_slippage_bps": MAX_SLIPPAGE_BPS}]
        return []
    if _exiting:
        # The exit fill landed (position gone): never trade again.
        _exiting = False
        _exited = True
        return []
    if _exited:
        return []
    # Flat and never entered: buy everything. Sent again on the next bar
    # if the market rejected this one, until the position shows up.
    if state.cash >= MIN_NOTIONAL:
        return [{"side": "buy", "symbol": _symbol,
                 "notional_quote_units": state.cash,
                 "max_slippage_bps": MAX_SLIPPAGE_BPS}]
    return []


makefun_bars.run(on_batch, on_hello=on_hello)
