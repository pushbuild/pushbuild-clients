"""OFR Financial Stress Index over the last month next to overnight repo rates (U.S. Treasury OFR)."""
from pushbuild import Pushbuild

pb = Pushbuild()
fsi = {r["date"]: r for r in pb.run("ofr-financial-stress-funding", mode="stressIndex", maxItems=22)}
repo = {r["date"]: r["value"] for r in pb.run("ofr-financial-stress-funding", mode="series", mnemonics="REPO-DVP_AR_OO-P", maxItems=22)}
for d in sorted(fsi, reverse=True):
    print(d, "FSI", fsi[d]["fsi"], "funding", fsi[d]["funding"], "DVP repo", repo.get(d))
