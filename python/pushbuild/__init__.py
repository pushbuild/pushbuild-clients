"""Client for the Pushbuild data APIs (https://pushbuild.com/apis): 350+ official and public data sources behind one key.

    from pushbuild import Pushbuild
    pb = Pushbuild("YOUR_KEY")            # or set PUSHBUILD_API_KEY
    rows = pb.run("us-treasury-yield-curve", maxItems=5)
"""
import json
import os
import urllib.error
import urllib.request

__version__ = "0.1.0"
BASE = "https://api.pushbuild.com"


class PushbuildError(Exception):
    def __init__(self, status, message):
        super().__init__(f"{status}: {message}")
        self.status = status


class Pushbuild:
    def __init__(self, api_key=None, base_url=BASE, timeout=300):
        self.api_key = api_key or os.environ.get("PUSHBUILD_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.last = {}  # count, truncated, seconds of the last run

    def _req(self, method, path, body=None):
        h = {"User-Agent": f"pushbuild-python/{__version__}", "Accept": "application/json"}
        if self.api_key:
            h["X-API-Key"] = self.api_key
        data = None
        if body is not None:
            data, h["Content-Type"] = json.dumps(body).encode(), "application/json"
        try:
            with urllib.request.urlopen(urllib.request.Request(self.base_url + path, data=data, headers=h, method=method), timeout=self.timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace")
            try:
                msg = json.loads(raw).get("detail") or raw
            except ValueError:
                msg = raw
            raise PushbuildError(e.code, msg) from None

    def apis(self):
        """Slugs of every API you can run."""
        return self._req("GET", "/health")["apis"]

    def openapi(self, slug):
        """The OpenAPI document of one API: its inputs, with descriptions and examples."""
        return self._req("GET", f"/openapi/{slug}.json")

    def run(self, slug, input=None, **kw):
        """Run one API and return its rows. Inputs go as keyword arguments or a dict, e.g. run("usgs-earthquakes", minMagnitude=5)."""
        res = self._req("POST", f"/{slug}/run", dict(input or {}, **kw))
        self.last = {k: v for k, v in res.items() if k != "items"}
        return res.get("items", [])
