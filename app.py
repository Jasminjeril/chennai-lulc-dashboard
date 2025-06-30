import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os

# Set Streamlit page config
st.set_page_config(page_title="Chennai LULC Dashboard", layout="wide")

st.markdown("<h2 style='text-align: center;'>Chennai LULC Change Detection (2018–2025)</h2>", unsafe_allow_html=True)


# Load data paths
DATA_DIR = "data"
files = {
    "NDVI 2018": "NDVI_2018_Chennai.tif",
    "NDVI 2025": "NDVI_2025_Chennai.tif",
    "NDVI Change": "NDVI_Change_2018_2025.tif",
    "NDBI 2018": "NDBI_2018_Chennai.tif",
    "NDBI 2025": "NDBI_2025_Chennai.tif",
    "NDBI Change": "NDBI_Change_2018_2025.tif"
}

# Sidebar selection
option = st.sidebar.selectbox("Select Map Layer", list(files.keys()))
selected_file = os.path.join(DATA_DIR, files[option])

# Load raster and display
with rasterio.open(selected_file) as src:
    data = src.read(1)
    profile = src.profile

# Show mean value
mean_val = np.nanmean(data)
st.sidebar.metric(label=f"Mean {option}", value=f"{mean_val:.3f}")
# Calculate and display % change insights (for NDVI/NDBI only)
if "Change" in option:
    base_key = option.replace("Change", "2018").strip()
    future_key = option.replace("Change", "2025").strip()
    base_file = os.path.join(DATA_DIR, files[base_key])
    future_file = os.path.join(DATA_DIR, files[future_key])

    with rasterio.open(base_file) as src:
        base = src.read(1)
    with rasterio.open(future_file) as src:
        future = src.read(1)

    base_mean = np.nanmean(base)
    future_mean = np.nanmean(future)
    percent_change = ((future_mean - base_mean) / abs(base_mean)) * 100

    if "NDVI" in option:
        emoji = "🌿"
        label = "Vegetation"
    else:
        emoji = "🏙️"
        label = "Built-up Area"

    st.info(f"{emoji} **{label} changed by {percent_change:.2f}% between 2018 and 2025**")

# Plot raster
st.subheader(f"🗺️ {option} Map")
fig, ax = plt.subplots(figsize=(8, 6))
nodata_val = profile.get('nodata', None)
if nodata_val is not None:
    masked = np.ma.masked_where(data == nodata_val, data)
else:
    masked = np.ma.masked_invalid(data)

cmap = "Greens" if "NDVI" in option else "Oranges"
img = ax.imshow(masked, cmap=cmap)
fig.colorbar(img, ax=ax, orientation="vertical", label=option)
ax.axis("off")
st.pyplot(fig)
st.session_state['last_fig'] = fig
st.session_state['last_section'] = 'single'

# --- NDVI & NDBI Mean Comparison Bar Chart ---
st.subheader("📊 NDVI and NDBI Comparison (2018 vs 2025)")

def load_mean(file_name):
    with rasterio.open(os.path.join(DATA_DIR, file_name)) as src:
        data = src.read(1)
        return np.nanmean(data)

ndvi_2018 = load_mean("NDVI_2018_Chennai.tif")
ndvi_2025 = load_mean("NDVI_2025_Chennai.tif")
ndbi_2018 = load_mean("NDBI_2018_Chennai.tif")
ndbi_2025 = load_mean("NDBI_2025_Chennai.tif")

labels = ["NDVI 2018", "NDVI 2025", "NDBI 2018", "NDBI 2025"]
values = [ndvi_2018, ndvi_2025, ndbi_2018, ndbi_2025]
colors = ['green', 'lightgreen', 'orange', 'orangered']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, values, color=colors)
ax.set_ylabel("Mean Value")
ax.set_title("Mean NDVI and NDBI Values")

# Add value labels on top
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, height, f'{height:.2f}', ha='center', va='bottom')

st.pyplot(fig)
st.subheader("🆚 Side-by-Side Comparison Viewer")
st.session_state['last_section'] = 'comparison'

comparison_type = st.selectbox(
    "Select Comparison Type",
    ["NDVI 2018 vs 2025", "NDBI 2018 vs 2025"]
)

def show_side_by_side(title1, file1, title2, file2, cmap):
    col1, col2 = st.columns(2)

    with rasterio.open(os.path.join(DATA_DIR, file1)) as src1:
        data1 = src1.read(1)
    with rasterio.open(os.path.join(DATA_DIR, file2)) as src2:
        data2 = src2.read(1)

    fig1, ax1 = plt.subplots()
    ax1.imshow(np.ma.masked_invalid(data1), cmap=cmap)
    ax1.set_title(title1)
    ax1.axis("off")
    col1.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.imshow(np.ma.masked_invalid(data2), cmap=cmap)
    ax2.set_title(title2)
    ax2.axis("off")
    col2.pyplot(fig2)

if comparison_type == "NDVI 2018 vs 2025":
    show_side_by_side("NDVI 2018", "NDVI_2018_Chennai.tif", "NDVI 2025", "NDVI_2025_Chennai.tif", "Greens")
else:
    show_side_by_side("NDBI 2018", "NDBI_2018_Chennai.tif", "NDBI 2025", "NDBI_2025_Chennai.tif", "Oranges")
import io
from PIL import Image

# --- Download Map Button ---
st.subheader("📥 Download Current Map as PNG")
fig_download = None

# Determine which figure to use for download
if "Comparison Viewer" in st.session_state.get('last_section', ''):
    # For side-by-side, we won’t support download (too complex)
    st.info("Download not available for side-by-side view.")
else:
    # We use the last single map figure (stored in st.session_state)
    fig_download = st.session_state.get('last_fig', None)

if fig_download:
    buf = io.BytesIO()
    fig_download.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="Download Map as PNG",
        data=buf,
        file_name=f"{option.replace(' ', '_')}.png",
        mime="image/png"
    )
