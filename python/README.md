# Pushbuild data API clients

One key, 350+ official and public data sources: SEC EDGAR filings, Federal Reserve, BLS, BEA, Census, USDA, NOAA, FDA, central banks worldwide, crypto exchanges and more. Every API takes JSON inputs and returns JSON rows.

- Catalogue and docs: https://pushbuild.com/apis
- Free key, with free monthly usage and no card needed: https://pushbuild.com/apis/app/signup
- Each API's inputs: `https://api.pushbuild.com/openapi/<slug>.json`

## Python

```
pip install "git+https://github.com/pushbuild/pushbuild-clients#subdirectory=python"
```

```python
from pushbuild import Pushbuild

pb = Pushbuild("YOUR_KEY")  # or set PUSHBUILD_API_KEY
rows = pb.run("us-treasury-yield-curve", maxItems=5)
print(pb.apis()[:10])        # every API slug
```

## JavaScript (Node 18+)

```
npm install pushbuild
```

```js
const { Pushbuild } = require("pushbuild");
const pb = new Pushbuild(process.env.PUSHBUILD_API_KEY);
const rows = await pb.run("crypto-perp-funding-rates", { symbols: "BTC,ETH" });
```

## HTTP

```
curl -X POST https://api.pushbuild.com/usgs-earthquakes/run \
  -H "X-API-Key: $PUSHBUILD_API_KEY" -H "Content-Type: application/json" \
  -d '{"minMagnitude": 5, "maxItems": 10}'
```

The response is `{"count": n, "truncated": bool, "seconds": s, "items": [...]}`. Errors return a JSON `detail`: 401 means no key or a bad key, and 402 means you are out of credit.

See [examples/](examples) for more. Both clients have no dependencies. MIT licence.
