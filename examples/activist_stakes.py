"""Every activist (13D) filing by a filer since 2013, largest stakes first."""
from pushbuild import Pushbuild

pb = Pushbuild()
rows = pb.run("sec-13d-13g-stakes", history=True, filerName="ICAHN", kind="13d", maxItems=500)
for r in sorted(rows, key=lambda r: -(r.get("percentOfClass") or 0))[:10]:
    print(r["filedDate"], r["targetName"], r.get("ticker"), r.get("percentOfClass"))
