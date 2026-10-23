// Perpetual funding rates across exchanges, widest annualized spread first.
import pkg from "pushbuild";
const { Pushbuild } = pkg;
const pb = new Pushbuild(process.env.PUSHBUILD_API_KEY);
const rows = await pb.run("crypto-perp-funding-rates", { symbols: "BTC,ETH,SOL" });
console.table(rows.slice(0, 20));
