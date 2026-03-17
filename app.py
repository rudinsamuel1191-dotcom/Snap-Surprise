import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
from rembg import remove
import io
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="SnapSurprise | Apex Photo Booth", page_icon="🦁")

st.title("🦁 SnapSurprise")
st.markdown("### Pose with predators. Stay alive (virtually).")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("📸 Photoshoot Settings")
animal = st.sidebar.selectbox("Select your Predator", ["Lion", "Anaconda", "Grizzly Bear", "Great White Shark"])
time_of_day = st.sidebar.select_slider("Time of Day", options=["Day", "Night"])

st.sidebar.markdown("---")
st.sidebar.info("Tip: For the best look, stand against a plain wall!")

# --- LOGIC: ASSET MAPPING ---
# In a real repo, you'd have these images in a folder. 
# Here we define the vibe for the 'Ultra-Realistic' backgrounds.
bg_descriptions = {
    "Lion": "African Savanna",
    "Anaconda": "Amazon Rainforest",
    "Grizzly Bear": "Alaskan Forest",
    "Great White Shark": "Deep Ocean"
}

# --- STEP 1: CAPTURE PHOTO ---
img_file = st.camera_input("Take a seat next to the beast!")

if img_file:
    with st.spinner("AI is dragging you into the wild..."):
        # Load User Image
        input_image = Image.open(img_file)
        
        # --- PRO TIP: LIGHTING MATCHING ---
        if time_of_day == "Night":
            # Darken the user
            enhancer = ImageEnhance.Brightness(input_image)
            input_image = enhancer.enhance(0.5) 
            # Add a blue 'moonlight' tint
            r, g, b = input_image.split()
            r = r.point(lambda i: i * 0.8) # Reduce red
            b = b.point(lambda i: i * 1.2) # Boost blue
            input_image = Image.merge("RGB", (r, g, b))
        
        # --- STEP 2: REMOVE BACKGROUND ---
        # This removes the user's room background
        user_no_bg = remove(input_image)
        
        # --- STEP 3: COMPOSITE (Mockup Logic) ---
        # Note: In a full build, you'd overlay this on a high-res JPG.
        # For this script, we'll show your 'cutout' ready for the habitat.
        st.image(user_no_bg, caption=f"You, processed for the {bg_descriptions[animal]} at {time_of_day}!")
        
        # --- STEP 4: SHARING ---
        st.success("Photo Ready!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("📲 Share to Instagram")
        with col2:
            st.button("🐦 Share to Twitter")
        with col3:
            st.download_button("💾 Download High-Res", data=img_file, file_name="snap_surprise.png")

# --- FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ for fun-hearted explorers.")
