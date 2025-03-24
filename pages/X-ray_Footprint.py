import streamlit as st
import base64
import matplotlib.pyplot as plt
import numpy as np
st.set_page_config(page_title="X-ray Footprint", page_icon='Icons/Paineira-Logo.png', layout="wide")


st.title('Work in progress...')
# Função para usar imagens como plano de fundo
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        image = f.read()
    return base64.b64encode(image).decode()

img = get_img_as_base64('Icons/Paineira-Layout.png')

# CSS customizado
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;

}}

[data-testid="stHeader"] {{
    background-color: rgba(256,0,0,0);

}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Sidebar controls
angle = st.sidebar.slider("Angle (degrees)", 0, 360, 0)
size = st.sidebar.slider("Size", 50, 200, 100)
angle_input = st.sidebar.number_input("Enter angle:", 0, 360, 0)
size_input = st.sidebar.number_input("Enter size:", 50, 200, 100)

# Sync sliders with input boxes
if angle != angle_input:
    angle = angle_input
if size != size_input:
    size = size_input

# Plotting
fig, ax = plt.subplots()
ax.set_xlim(-150, 150)
ax.set_ylim(-150, 150)
ax.set_axis_off()

# Create rotated rectangle
theta = np.radians(angle)
half_size = size / 2
corners = np.array([[-half_size, -half_size], [half_size, -half_size], 
                    [half_size, half_size], [-half_size, half_size]])
rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], 
                            [np.sin(theta), np.cos(theta)]])
rotated_corners = np.dot(corners, rotation_matrix)
poly = plt.Polygon(rotated_corners, closed=True, fill=None, edgecolor='blue', linewidth=3)
ax.add_patch(poly)
ax.set_aspect('equal')
st.pyplot(fig)