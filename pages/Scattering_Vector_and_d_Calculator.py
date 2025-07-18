import streamlit as st
import numpy as np
import plotly.graph_objects as go
import re
import scipy.constants
import math, plotly
from plotly.subplots import make_subplots
import base64

st.set_page_config(page_title="2θ, d-spacing and Q converter", page_icon='Icons/Paineira-Logo.png', layout="wide")
st.logo('Icons/Paineira-Logo.png', link='https://lnls.cnpem.br/facilities/paineira-en/', icon_image='Icons/Paineira-Layout.png', size='large')
st.markdown(
    """
    <div style="background-color: #FF4B4B; border-radius: 5px; padding: 2px; margin-bottom: 20px;">
        <h1 style="color: Black; text-align: center;"> 2θ, d-spacing and Q converter</h1>
    </div>
    """, unsafe_allow_html=True
)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64('Icons/Paineira_layout_2.png')

# Constantes
h = scipy.constants.physical_constants['Planck constant in eV/Hz'][0]
c = scipy.constants.c


def calculate_wavelength(energy):
    """Calcula o comprimento de onda (Å) a partir da energia (keV)."""
    return h * c / (energy * 1e3) * 1e10

def calculate_energy(wavelength):
    """Calcula a energia (keV) a partir do comprimento de onda (Å)."""
    return h * c / (wavelength * 1e-10) * 1e-3

def scattering_vector(wavelength, two_theta):
    """Calcula o vetor de espalhamento Q."""
    return (4 * np.pi / wavelength) * np.sin(np.deg2rad(two_theta / 2))

def calculate_d(wavelenght, two_theta):
    """Calcula o espaçamento inter-planar"""
    return (wavelenght / (2 * np.sin(np.deg2rad(two_theta / 2))))


two_theta = st.number_input('2θ (degrees)', min_value=0.0, max_value=180.0, value=10.0, step=0.0001, format='%.4f')
energy_or_wavelength = st.radio('Select the energy or wavelength of the Uploaded XRD pattern', ['Energy (keV)', 'Wavelength (Å)'])

if energy_or_wavelength == 'Energy (keV)':
    energy = st.number_input('Energy (keV)', min_value=1.0, max_value=30.0, value=25.5000, step=0.0001, format='%.2f')
    wavelength = calculate_wavelength(energy)
    Q = scattering_vector(wavelength, two_theta)
    d = calculate_d(wavelength, two_theta)
    st.markdown(
            f"""
            <div style="background-color: #333; border: 2px solid rgb(255,75,75); border-radius: 8px; padding: 10px; margin-top: 10px; margin-bottom: 10px;">
                <p style="color: white; margin: 0;">Wavelength: {wavelength:.6f} Å,  Energy: {energy:.4f} keV</p>
                <p style="color: white; margin: 0;">Q: {Q:.4f} Å⁻¹,  d: {d:.4f} Å</p>
            </div>
            """, unsafe_allow_html=True
        )

else:
    wavelength = st.number_input('Wavelength (Å)', min_value=0.1, max_value=3.0, value=0.486213, step=0.00001, format='%.6f')
    Q = scattering_vector(wavelength, two_theta)
    d = calculate_d(wavelength, two_theta)
    energy = calculate_energy(wavelength)
    st.markdown(
            f"""
            <div style="background-color: #333; border: 2px solid rgb(255,75,75); border-radius: 8px; padding: 10px; margin-top: 10px; margin-bottom: 10px;">
                <p style="color: white; margin: 0;">Wavelength: {wavelength:.6f} Å,  Energy: {energy:.4f} keV</p>
                <p style="color: white; margin: 0;">Q: {Q:.4f} Å⁻¹,  d: {d:.4f} Å</p>
            </div>
            """, unsafe_allow_html=True
        )
    