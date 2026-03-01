from skyfield.api import load, wgs84
from datetime import datetime, timedelta, timezone
import requests
import os

# --- 1. Weather Function ---
def get_weather_status(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=cloud_cover"
    response = requests.get(url).json()
    clouds = response['current']['cloud_cover']
    
    print(f"\n--- Weather Update for Goa ---")
    print(f"Current Cloud Cover: {clouds}%")
    
    if clouds > 50:
        return "❌ High chance of clouds. Might be hard to see!"
    else:
        return "✅ Clear skies! Perfect for spotting the ISS."

# --- 2. Setup Data ---
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle'
satellites = load.tle_file(stations_url)
iss = {sat.name: sat for sat in satellites}['ISS (ZARYA)']

# My location (Goa, India)
home_lat, home_lon = 15.405528, 73.9998135
home = wgs84.latlon(home_lat, home_lon)

print("Setup complete! I found the ISS and I know where you live.")

# --- 3. Current Position ---
ts = load.timescale()
t = ts.now()
difference = iss - home
topocentric = difference.at(t)
alt, az, distance = topocentric.altaz()

if alt.degrees > 0:
    print(f"YES! Look up! The ISS is {alt.degrees:.1f} degrees above.")
else:
    print(f"Not right now. Altitude: {alt.degrees:.1f} degrees (below horizon).")

# --- 4. Search for Next Passes ---
print("\n--- Searching for the next 24 hours ---")
IST = timezone(timedelta(hours=5, minutes=30))
t0 = ts.now()
t1 = ts.from_datetime(t0.utc_datetime() + timedelta(days=1))
t_events, events = iss.find_events(home, t0, t1, altitude_degrees=10.0)

# --- 5. Display & Save Results ---
if not os.path.exists('Data'):
    os.makedirs('Data')

file_path = 'Data/pass_predictions.txt'

with open(file_path, 'w') as f:
    f.write("ISS Pass Predictions for India\n------------------------------\n")
    print("\n--- Next ISS Passes (India Standard Time) ---")
    
    for ti, event in zip(t_events, events):
        local_time = ti.astimezone(IST)
        name = ('Rise', 'Peak', 'Set')[event]
        formatted_time = local_time.strftime('%d-%m-%Y %I:%M %p')
        
        # Print to screen
        print(f"{formatted_time} IST | {name}")
        # Write to file
        f.write(f"{formatted_time} IST | {name}\n")

print(f"\nSuccess! Predictions saved to {file_path}")

# --- 6. The Weather Check ---
# We call the function here!
weather_report = get_weather_status(home_lat, home_lon)
print(weather_report)
