import streamlit as st
from PIL import Image, ImageEnhance
import io

# --- CLOUD-FRIENDLY BACKGROUND REMOVAL ---
def process_transformation(input_image, time_of_day):
    """
    This function handles the AI and the lighting adjustments.
    By importing 'rembg' inside here, the app starts up much faster.
    """
    from rembg import remove
    
    # 1. Apply Realistic Lighting (Pro-Tip)
    if time_of_day == "Night":
        # Darken the subject
        enhancer = ImageEnhance.Brightness(input_image)
        input_image = enhancer.enhance(0.4) 
        # Add a cool blue 'moonlight' tint
        r, g, b = input_image.split()
        r = r.point(lambda i: i * 0.7) # Dim the reds
        b = b.point(lambda i: i * 1.3) # Boost the blues
        input_image = Image.merge("RGB", (r, g, b))
    else:
        # Subtle 'Sunlight' boost for Day mode
        enhancer = ImageEnhance.Contrast(input_image)
        input_image = enhancer.enhance(1.1)

    # 2. Remove Background
    output_image = remove(input_image)
    return output_image

# --- UI CONFIGURATION ---
st.set_page_config(page_title="SnapSurprise", page_icon="🦁")

st.title("🦁 SnapSurprise")
st.subheader("Your realistic predator photoshoot.")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Settings")
    animal = st.selectbox("Choose your Predator", ["Lion", "Anaconda", "Grizzly Bear", "Great White Shark"])
    time_of_day = st.select_slider("Lighting Environment", options=["Day", "Night"])
    st.divider()
    st.info("💡 For best results, stand in a well-lit area with a simple background.")

# --- MAIN INTERFACE ---
img_file = st.camera_input("Smile for the predator!")

if img_file:
    # Progress bar makes the wait feel shorter for the user
    with st.status("Merging you into the wild...", expanded=True) as status:
        st.write("Analyzing lighting...")
        user_img = Image.open(img_file)
        
        st.write("Removing your room (AI)...")
        final_result = process_transformation(user_img, time_of_day)
        
        status.update(label="Transformation Complete!", state="complete", expanded=False)

    # Display Result
    st.image(final_result, caption=f"You vs. The {animal} ({time_of_day} Edition)")

    # Social Sharing Simulation
    st.write("### 📲 Share your encounter:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Instagram", use_container_width=True)
    with col2:
        st.button("WhatsApp", use_container_width=True)
    with col3:
        # Allow the user to actually save the file
        buf = io.BytesIO()
        final_result.save(buf, format="PNG")
        st.download_button(
            label="Download Photo",
            data=buf.getvalue(),
            file_name="snapsurprise_wild.png",
            mime="image/png",
            use_container_width=True
        )

# --- FOOTER ---
st.markdown("---")
st.caption("Built for fun-hearted adventurers. SnapSurprise © 2026")
