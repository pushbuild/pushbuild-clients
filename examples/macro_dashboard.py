"""Latest US GDP growth (BEA), 10-year Treasury yield and crop yields in a few calls."""
from pushbuild import Pushbuild

pb = Pushbuild()
gdp = pb.run("bea-economic-data", preset="gdp-growth", maxItems=1)[0]
print("Real GDP growth", gdp["period"], gdp["value"], "%")
curve = pb.run("us-treasury-yield-curve", maxItems=1)
print("Treasury curve", curve[0])
corn = pb.run("usda-nass-agriculture-statistics", commodity="CORN", statistic="YIELD", level="national", maxItems=3)
for r in corn:
    print("Corn yield", r["year"], r["value"], r["unit"])
