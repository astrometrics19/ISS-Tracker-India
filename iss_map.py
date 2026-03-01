import matplotlib.pyplot as plt
from skyfield.api import load, wgs84
import numpy as np

# 1. Setup
ts = load.timescale()
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle'
satellites = load.tle_file(stations_url)
iss = {sat.name: sat for sat in satellites}['ISS (ZARYA)']

# 2. Calculate positions for the next 90 minutes (one full orbit)
minutes = np.arange(0, 90, 1)
times = ts.now().utc_datetime()
# Create a list of times for the next 90 minutes
future_times = [ts.from_datetime(times + timedelta(minutes=m)) for m in minutes]

lats, lons = [], []
for t in future_times:
    geocentric = iss.at(t)
    subpoint = wgs84.subpoint(geocentric)
    lats.append(subpoint.latitude.degrees)
    lons.append(subpoint.longitude.degrees)

# 3. Create the Plot
plt.figure(figsize=(10, 5))
plt.plot(lons, lats, 'ro', markersize=2)
plt.title("ISS Ground Track - Next 90 Minutes")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)

# 4. Save it to your Plots folder
plt.savefig('Plots/iss_track_map.png')
print("Map saved to Plots/iss_track_map.png!")