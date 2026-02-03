import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sunflower Data Collective — Growth Demo",
    layout="wide"
)

# ---------- Header ----------

st.title("🌻 Sunflower Data Collective — Growth Pattern Demo")

st.markdown("""
**Nature scales with structure. Your data should too.**

Sunflowers use the **golden angle (137.5°)** to grow without overlap.
We use the same principle when designing scalable data systems.
""")

# ---------- Controls ----------

col1, col2 = st.columns(2)

with col1:
    points = st.slider("Number of seeds (data elements)", 100, 2000, 800)

with col2:
    size = st.slider("Point size", 4, 20, 8)

# ---------- Spiral Math ----------

GOLDEN_ANGLE = np.deg2rad(137.5)

i = np.arange(points)
r = np.sqrt(i)
theta = i * GOLDEN_ANGLE

x = r * np.cos(theta)
y = r * np.sin(theta)

# ---------- Plot ----------

fig, ax = plt.subplots(figsize=(7,7))
ax.scatter(x, y, s=size, c="#f4b400")  # sunflower gold
ax.set_aspect('equal')
ax.axis('off')

st.pyplot(fig)

# ---------- Business Translation ----------

st.markdown("---")

st.header("📊 What This Means for Data Systems")

st.markdown("""
Each new point represents new data entering a system:

✅ It adds value  
✅ It does not overwrite prior structure  
✅ It fits cleanly into the model  
✅ Growth stays stable  

**If growth causes collisions — the structure is wrong.**
""")

st.info("This is the Sunflower Principle: structured growth beats reactive redesign.")
