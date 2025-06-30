# 🌍 Chennai LULC Change Detection Dashboard
[![Streamlit](https://img.shields.io/badge/Live-Dashboard-success?logo=streamlit)](https://chennai-lulc-dashboard-etm7d28sotgwhtnsytdvqb.streamlit.app/)
![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-brightgreen?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Deployed-blue)
![License](https://img.shields.io/badge/License-MIT-green)


This is an interactive geospatial dashboard that visualizes **Land Use and Land Cover (LULC)** changes in **Chennai, India** between **2018 and 2025**. It uses NDVI (vegetation) and NDBI (built-up) indices derived from Sentinel-2 satellite imagery.

Built using **Google Earth Engine**, **QGIS**, and **Streamlit**.

---

## 📌 Features

- 🛰️ Uses Sentinel-2 imagery from Google Earth Engine
- 🌿 Calculates NDVI (Normalized Difference Vegetation Index)
- 🏙️ Calculates NDBI (Normalized Difference Built-up Index)
- 📊 Shows mean value insights and % change
- 🗺️ Side-by-side comparison viewer for NDVI and NDBI
- 📥 Download maps as PNG images

---

## 🗃️ Project Structure

chennai-lulc-dashboard/
├── app.py # Streamlit dashboard
├── requirements.txt # Required Python packages
├── data/ # GeoTIFF files for NDVI & NDBI
│ ├── NDVI_2018_Chennai.tif
│ ├── NDVI_2025_Chennai.tif
│ ├── NDVI_Change_2018_2025.tif
│ ├── NDBI_2018_Chennai.tif
│ ├── NDBI_2025_Chennai.tif
│ ├── NDBI_Change_2018_2025.tif
