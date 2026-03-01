# 🛰️ ISS Satellite Pass Predictor (India)

A Python-based orbital tracking tool developed to predict visible passes of the International Space Station (ISS) for specific coordinates in India.

## 🚀 Key Features
* **Real-time Orbital Data:** Fetches live TLE (Two-Line Element) sets from CelesTrak.
* **Geodetic Calculations:** Uses the Skyfield library (SGP4 propagator) to calculate altitude and azimuth.
* **Localized Predictions:** Automatically converts UTC space-time into India Standard Time (IST).
* **Weather Integration:** Connects to Open-Meteo API to check cloud cover for upcoming passes.

## 📂 Project Structure
* `/Notebooks`: Core Python scripts and calculation logic.
* `/Data`: Exported text reports of predicted pass times.
* `/Plots`: Generated ground-track maps of the ISS orbit.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** Skyfield, Requests, Matplotlib, Datetime
* **Data Sources:** NORAD/CelesTrak, Open-Meteo API