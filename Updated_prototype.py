# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, beta, lognorm, norm
from scipy.optimize import minimize
import streamlit as st
from streamlit_jupyter import StreamlitPatcher
from matplotlib.gridspec import GridSpec
from scipy.stats import gaussian_kde
# %%



    
    

# %%
st.title("Inundation Method Dashboard")

days = st.number_input("Days of Inundation", min_value=0.0, value=0.0)
day_cv = st.slider("Coefficient of Variation for the Days of Inundation (optional assumed 30%) ", min_value = 0.0, value = 0.3)

area = st.number_input("Surface Area (m²)", min_value=0.0, value=0.0)
area_cv = st.slider("Coefficient of varation for area of inundation (optional assumed 30%)", min_value = 0.0, value = 0.3) 

depth = st.number_input("Depth (m)", min_value=0.0, value=0.0)
depth_cv = st.slider("Coefficient of Variation for the Depth (optional assumed 30%) ", min_value = 0.0, value = 0.3)

# %%
alpha_days = (1/day_cv)**2
alpha_depth = (1/depth_cv)**2
alpha_area = (1/area_cv)**2

beta_days = days/alpha_days
beta_depth = depth/alpha_depth
beta_area = area/alpha_area



# %%
t = 0
vwb = []
while t<100001:
    ran_days = np.random.gamma(alpha_days, beta_days)
    if ran_days > 365:
    	ran_days = 365
    ran_depth = np.random.gamma(alpha_depth, beta_depth)
    ran_area = np.random.gamma(alpha_area, beta_area)
    vwb.append(ran_days*ran_depth*ran_area)
    t+=1

# %%
st.write(f"Mean simulated total volume: {np.mean(vwb):,.2f} m³")
st.write(f"Median: {np.median(vwb):,.2f} m³")
st.write(f"5th Percentile: {np.percentile(vwb, 5)} m³")
st.write(f"95th Percentile: {np.percentile(vwb, 95)} m³")
#st.write(f"a_days = {alpha_days}, b_days = {beta_days}")
#st.write(f"a_area = {alpha_area}, b_days = {beta_area}")
#st.write(f"a_depth= {alpha_depth}, b_days = {beta_depth}")
# %%
dom_days = np.linspace(0, min(days+100, 365),10000)
dom_area = np.linspace(0, area*2, 10000)
dom_depth = np.linspace(0, depth*2, 10000)

day_dist = gamma.pdf(dom_days, alpha_days, 0,beta_days)
area_dist = gamma.pdf(dom_area, alpha_area, 0,beta_area)
depth_dist = gamma.pdf(dom_depth, alpha_depth, 0,beta_depth)

kde = gaussian_kde(vwb)
dom_kde = np.linspace(0, max(vwb))

# %%
fig = plt.figure(constrained_layout = True, figsize=(10,6))
gs = GridSpec(3,2, figure = fig)

ax_big = fig.add_subplot(gs[:,0])
ax_big.hist(vwb, bins = 100, color = 'skyblue',edgecolor = 'black', density = True)
ax_big.plot(dom_kde, kde(dom_kde), color = 'red')
ax_big.set_title("Distribution of VWB [m³/yr]")

# %%
ax_small1 = fig.add_subplot(gs[0, 1])
ax_small1.plot(dom_days, day_dist)
ax_small1.set_title("Days of Inundation Distribution [days]")

ax_small2 = fig.add_subplot(gs[1, 1])
ax_small2.plot(dom_area, area_dist)
ax_small2.set_title("Area of Inundation Distribution [m] ")

ax_small3 = fig.add_subplot(gs[2, 1])
ax_small3.plot(dom_depth, depth_dist )
ax_small3.set_title(r"Depth of inundation [m$^{2}$]")

# Display in Streamlit
st.pyplot(fig)



# %%
# !jupytext --to py Updated_prototype.ipynb
