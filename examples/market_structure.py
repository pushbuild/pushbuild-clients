"""Which large caps have the highest cancel-to-trade ratio and hidden-trade share (SEC MIDAS, latest quarter)."""
from pushbuild import Pushbuild

pb = Pushbuild()
rows = pb.run("sec-market-structure-metrics", tickers="AAPL,MSFT,NVDA,AMZN,TSLA,META,GOOGL", maxItems=7000)
latest = {}
for r in rows:  # newest first, so the first row per ticker is its latest day
    latest.setdefault(r["ticker"], r)
for t, r in sorted(latest.items(), key=lambda kv: -(kv[1]["cancelToTradeRatio"] or 0)):
    print(f'{t:6} {r["date"]}  cancel/trade {r["cancelToTradeRatio"]:6.1f}  hidden {r["hiddenTradeRate"]:.1%}  odd lot {r["oddLotRate"]:.1%}')
