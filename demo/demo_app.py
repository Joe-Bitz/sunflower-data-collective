import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

GOLDEN_ANGLE_DEGREES = 137.5
MAX_RADIUS = 10
PLOT_LIMIT = 11


def compute_spiral_points(points: int):
    golden_angle = np.deg2rad(GOLDEN_ANGLE_DEGREES)
    indices = np.arange(points)
    radius = np.sqrt(indices)
    radius = radius / radius.max() * MAX_RADIUS
    theta = indices * golden_angle
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return x, y


def build_plot(x, y, size: int):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(x, y, s=size, c="#f4b400")  # sunflower gold
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-PLOT_LIMIT, PLOT_LIMIT)
    ax.set_ylim(-PLOT_LIMIT, PLOT_LIMIT)
    return fig


st.set_page_config(page_title="Sunflower Data Collective — Growth Demo", layout="centered")

# ---------- Header ----------

st.title("🌻 Sunflower Data Collective — Growth Pattern Demo")

st.markdown(
    """
**Nature scales with structure. Your data should too.**

Sunflowers use the **golden angle (137.5°)** to grow without overlap.
We use the same principle when designing scalable data systems.
"""
)

# ---------- Controls ----------

col1, col2 = st.columns(2)

with col1:
    points = st.slider("Number of seeds (data elements)", 100, 2000, 800)

with col2:
    size = st.slider("Point size", 4, 20, 8)

# ---------- Spiral Math ----------

x, y = compute_spiral_points(points)

# ---------- Plot ----------

fig = build_plot(x, y, size)
st.pyplot(fig)
plt.close(fig)

# ---------- Business Translation ----------

st.markdown("---")

st.header("📊 What This Means for Data Systems")

st.markdown(
    """
Each new point represents new data entering a system:

- It adds value
- It does not overwrite prior structure
- It fits cleanly into the model
- Growth stays stable

**If growth causes collisions — the structure is wrong.**
"""
)

st.info("This is the Sunflower Principle: structured growth beats reactive redesign.")
