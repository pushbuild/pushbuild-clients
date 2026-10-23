// Client for the Pushbuild data APIs (https://pushbuild.com/apis): 350+ official and public data sources behind one key.
//   const { Pushbuild } = require("pushbuild");
//   const pb = new Pushbuild(process.env.PUSHBUILD_API_KEY);
//   const rows = await pb.run("us-treasury-yield-curve", { maxItems: 5 });
const VERSION = "0.1.0";

class PushbuildError extends Error {
  constructor(status, message) {
    super(`${status}: ${message}`);
    this.status = status;
  }
}

class Pushbuild {
  constructor(apiKey = process.env.PUSHBUILD_API_KEY, { baseUrl = "https://api.pushbuild.com", timeoutMs = 300000 } = {}) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.timeoutMs = timeoutMs;
    this.last = {};
  }

  async _req(method, path, body) {
    const headers = { "User-Agent": `pushbuild-js/${VERSION}`, Accept: "application/json" };
    if (this.apiKey) headers["X-API-Key"] = this.apiKey;
    if (body !== undefined) headers["Content-Type"] = "application/json";
    const r = await fetch(this.baseUrl + path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(this.timeoutMs) });
    const text = await r.text();
    let data;
    try { data = JSON.parse(text); } catch { data = text; }
    if (!r.ok) throw new PushbuildError(r.status, (data && data.detail) || text);
    return data;
  }

  /** Slugs of every API you can run. */
  async apis() { return (await this._req("GET", "/health")).apis; }

  /** The OpenAPI document of one API. */
  openapi(slug) { return this._req("GET", `/openapi/${slug}.json`); }

  /** Run one API and return its rows. */
  async run(slug, input = {}) {
    const res = await this._req("POST", `/${slug}/run`, input);
    const { items, ...meta } = res;
    this.last = meta;
    return items || [];
  }
}

module.exports = { Pushbuild, PushbuildError };
