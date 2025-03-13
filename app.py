import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64, scipy.constants
from plotly.subplots import make_subplots

# Constantes físicas
h = scipy.constants.physical_constants['Planck constant in eV/Hz'][0]
c = scipy.constants.c

# Configurar a página inicial
st.set_page_config(page_title='XRD - Energy Converter and Scattering Vector', 
                   page_icon='Icons/Paineira-Logo.png', layout='wide')

# Caixa para o título (cor de fundo diferenciada)
st.markdown(
    """
    <div style="background-color: #FF4B4B; border-radius: 5px; padding: 2px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">XRD - Energy Converter and Scattering Vector</h1>
    </div>
    """, unsafe_allow_html=True
)

# Seção "About" com fundo sólido
with st.expander('How it works'):
    st.markdown(
    """
    This tool is designed to compare X-ray diffraction (XRD) patterns at different energy levels, allowing users to visualize how the diffraction pattern changes when the energy of the X-rays is modified. It also provides the ability to calculate the scattering vector (Q) for the data, which can be useful for further analysis of the crystal structure.

    The program enables users to:

    - Convert an XRD pattern collected at a specific energy to a new energy level (keV) or wavelength (Å).
    Generate graphs that compare the diffraction patterns at the original and new energy levels.
    - Calculate the scattering vector (Q) to support additional crystallographic analysis.
    - This tool is particularly useful for researchers who need to analyze how changes in X-ray energy affect the diffraction pattern, facilitating comparisons and insights into material properties.

    #### Important Note:
    For the tool to recognize the dataset correctly, the angle column must be labeled "2theta (degree)" and the intensity column must be labeled "Intensity". Please ensure your data follows this format before uploading.



    #### Scientific Basis:
    The diffraction pattern is calculated using **Bragg's Law**:

    $$
    n\lambda = 2d \sin (\\theta)
    $$

    where:
    -  $\lambda$ is the wavelength of the X-rays
    -  $d$ is the distance between lattice planes
    -  $\\theta$ is the angle of diffraction
    -  $n$ is the diffraction order (usually taken as 1 for first-order diffraction)

    The scattering vector \( $Q$ \) is related to the diffraction angle \( $\\theta$ \) and the wavelength \( $\lambda$ \) by:

    $$
    Q = \\frac{4\pi}{\lambda} \sin(\\theta)
    $$

    This vector represents the momentum transfer during the scattering process and provides crucial information about the crystal structure of materials.

    #### References:
    - PEIN, Andreas; PUHR, Barbara; JONES, Andrew. The Non-Ambient XRD Guide. Graz: Anton Paar GmbH, 2023.
    - ANTON PAAR GmbH. SAXS Guide: Getting Acquainted with the Principles. Graz: Anton Paar GmbH, 2013.
    """, unsafe_allow_html=True
)

# Função para usar imagens como plano de fundo
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        image = f.read()
    return base64.b64encode(image).decode()

img = get_img_as_base64('Icons/Paineira-Layout.png')

# CSS customizado
page_bg_image = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

html, body {{
    overflow: auto !important;
    font-family: "Open Sans", serif;
}}

[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{img}");
}}

[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.1);
    z-index: 0;
    pointer-events: none;
}}

[data-testid="stAppViewContainer"] > * {{
    position: relative;
    z-index: 1;
    color: white;
}}

[data-testid="stMarkdownContainer"] {{
    color: white;
    font-weight: 400;
}}

h1, h2, h3, h4, h5, h6 {{
    font-weight: 700;
}}

/* Estilizando a seção About*/
[data-testid="stExpander"],
[data-testid="stFileUploader"] {{
    background-color: #262730;
    border-radius: 8px;
    padding: 10px;
}}

/* Componentes de seleção e entrada numérica */
[data-testid="stRadio"],
[data-testid="stNumberInput"] {{
    background-color: #262730;
    border-radius: 8px;
    padding: 10px;
}}

/* Botão de converter - NOVA BORDA */
div[data-testid="stButton"] > button {{
    background-color: #4CAF50;
    color: white;
    border: 2px solid #262730 !important;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}}

div[data-testid="stButton"] > button:hover {{
    background-color: #45a049;
}}

/* Botões de download - NOVA BORDA */
div[data-testid="stDownloadButton"] > button {{
    background-color: #4CAF50;
    color: white;
    border: 2px solid #262730 !important;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}}

div[data-testid="stDownloadButton"] > button:hover {{
    background-color: #45a049;
}}
</style>
"""
st.markdown(page_bg_image, unsafe_allow_html=True)

# Funções auxiliares para os cálculos
def calculate_wavelength(energy):
    """Calcula o comprimento de onda (Å) a partir da energia (keV)."""
    return h * c / (energy * 1e3) * 1e10

def calculate_energy(wavelength):
    """Calcula a energia (keV) a partir do comprimento de onda (Å)."""
    return h * c / (wavelength * 1e-10) * 1e-3

def calculate_new_2theta(two_theta, original_energy, new_energy):
    """Calcula o novo ângulo 2θ para uma nova energia."""
    return 2 * np.rad2deg(np.arcsin((original_energy / new_energy) * np.sin(np.deg2rad(two_theta / 2))))

def scattering_vector(wavelength, two_theta):
    """Calcula o vetor de espalhamento Q."""
    return (4 * np.pi / wavelength) * np.sin(np.deg2rad(two_theta / 2))

def generate_plots(two_theta, intensity, new_2theta, Q):
    """Gera os gráficos com destaque suave."""
    fig = make_subplots(
        rows=1, 
        cols=2, 
        subplot_titles=['2θ vs Intensity', 'Scattering Vector (Å⁻¹) vs Intensity'],
        horizontal_spacing=0.1
    )
    
    # Gráfico 1: Difratograma com nova energia
    fig.add_trace(go.Scatter(x=two_theta, y=intensity, line=dict(width=2, color='blue'), name=f'Original Energy {energy} keV'), row=1, col=1)
    fig.add_trace(go.Scatter(x=new_2theta, y=intensity, line=dict(width=2, color='red'), name=f'New Energy {new_energy} keV'), row=1, col=1)
    
    # Gráfico 2: Vetor de espalhamento
    fig.add_trace(go.Scatter(x=Q, y=intensity, line=dict(width=2, color='purple'), name=f'Scattering Vector{energy} keV'), row=1, col=2)

    

    # Layout ajustado
    fig.update_layout(
        font=dict(color='black'),
        legend=dict(font=dict(color='black')),
        plot_bgcolor='rgba(248, 249, 250, 0.9)',  # Fundo mais suave
        paper_bgcolor='rgba(248, 249, 250, 0.9)',  # Cor harmonizada
        margin=dict(l=20, r=20, t=100, b=20),  # Margem superior aumentada
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        annotations=[
            dict(
                x=0.225,
                y=1.18,  # Posição ajustada para cima
                xanchor='center',
                yanchor='top',
                text='2θ vs Intensity',
                showarrow=False,
                font=dict(size=16, color='black')
            ),
            dict(
                x=0.775,
                y=1.18,  # Posição ajustada para cima
                xanchor='center',
                yanchor='top',
                text='Scattering Vector (Å⁻¹) vs Intensity',
                showarrow=False,
                font=dict(size=16, color='black')
            )
        ]
    )
    
    fig.update_xaxes(title_text='2θ (degree)', row=1, col=1)
    fig.update_yaxes(title_text='Intensity (a.u.)', row=1, col=1)
    fig.update_xaxes(title_text='Scattering Vector (Å⁻¹)', row=1, col=2)
    fig.update_yaxes(title_text='Intensity (a.u.)', row=1, col=2)
    
    return fig

# --- Persistência do gráfico usando session_state ---
if "chart_generated" not in st.session_state:
    st.session_state.chart_generated = False

# Seleção entre energia e comprimento de onda e inputs numéricos
energy_or_wavelength = st.radio('Select the energy or wavelength of the Uploaded XRD pattern', ['Energy (keV)', 'Wavelength (Å)'])

if energy_or_wavelength == 'Energy (keV)':
    energy = st.number_input('Energy (keV)', min_value=1.0, max_value=30.0, value=25.5000, step=0.0001, format='%.2f')
    wavelength = calculate_wavelength(energy)
    new_energy = st.number_input('New Energy (keV)', min_value=1.0, max_value=30.0, value=None, step=0.0001, format='%.2f')
    if new_energy:
        new_wavelength = calculate_wavelength(new_energy)
        st.markdown(
            f"""
            <div style="background-color: #333; border: 2px solid rgb(255,75,75); border-radius: 8px; padding: 10px; margin-top: 10px; margin-bottom: 10px;">
                <p style="color: white; margin: 0;"><strong>Original:</strong> Wavelength: {wavelength:.4f} Å, Energy: {energy:.2f} keV</p>
                <p style="color: white; margin: 0;"><strong>New:</strong> Wavelength: {new_wavelength:.4f} Å, Energy: {new_energy:.2f} keV</p>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color: #333; border: 2px solid rgb(255,75,75); border-radius: 8px; padding: 10px; margin-top: 10px; margin-bottom: 10px;">
                <p style="color: white; margin: 0;">Wavelength: {wavelength:.4f} Å, Energy: {energy:.2f} keV</p>
            </div>
            """, unsafe_allow_html=True
        )
else:
    wavelength = st.number_input('Wavelength (Å)', min_value=0.1, max_value=3.0, value=0.4862, step=0.0001, format='%.4f')
    energy = calculate_energy(wavelength)
    new_wavelength = st.number_input('New Wavelength (Å)', min_value=0.1, max_value=3.0, value=None, step=0.0001, format='%.4f')
    if new_wavelength:
        new_energy = calculate_energy(new_wavelength)
        st.markdown(
            f"""
            <div style="background-color: #333; border: 2px solid rgb(255,75,75); border-radius: 8px; padding: 10px; margin-top: 10px; margin-bottom: 10px;">
                <p style="color: white; margin: 0;"><strong>Original:</strong> Wavelength: {wavelength:.4f} Å,  Energy: {energy:.2f} keV</p>
                <p style="color: white; margin: 0;"><strong>New:</strong>  Wavelength: {new_wavelength:.4f} Å,  Energy: {new_energy:.2f} keV</p>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color: #333; border: 2px solid rgb(255,75,75); border-radius: 8px; padding: 10px; margin-top: 10px; margin-bottom: 10px;">
                <p style="color: white; margin: 0;">Wavelength: {wavelength:.4f} Å, Energy: {energy:.2f} keV</p>
            </div>
            """, unsafe_allow_html=True
        )

# Upload de arquivo XRD
input_XRD = st.file_uploader('Upload the XRD pattern', type=['txt', 'csv'])

# Botão para converter e gerar os gráficos
if st.button('Convert and plot both graphs (2θ x Intensity and Scattering Vector x Intensity)'):
    if input_XRD is not None:
        try:
            input_df = pd.read_csv(input_XRD, sep=',')
            two_theta = input_df['2theta (degree)']
            intensity = input_df['Intensity']

            new_2theta = calculate_new_2theta(two_theta, energy, new_energy)
            
            Q = scattering_vector(wavelength, two_theta)
       

            fig = generate_plots(two_theta, intensity, new_2theta, Q)
            st.session_state.chart_generated = True
            st.session_state.fig = fig


            st.session_state.new_diffractogram = pd.DataFrame({'2theta (degree)': new_2theta, 'Intensity': intensity}).to_csv(index=False)

            st.session_state.scattering_data = pd.DataFrame({'Scattering Vector (Å⁻¹)': Q, 'Intensity': intensity}).to_csv(index=False)


        except Exception as e:
            st.error(f'Error processing the file: {e}')
    else:
        st.error('Please upload a valid XRD pattern file.')

# Exibir gráficos e botões de download
if st.session_state.chart_generated:
    # Container simplificado sem borda
    st.plotly_chart(st.session_state.fig, use_container_width=True)
    
    # Botões de download
    col_left, col_center, col_right = st.columns([1,2,1])
    with col_center:
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download New Diffractogram",
                data=st.session_state.new_diffractogram,
                file_name=f'New_Diffractogram_{new_energy:.2f}keV_{new_wavelength:.4f}Å.csv',
                mime='text/csv'
            )
        with col2:
            st.download_button(
                label="Download Scattering Vector Data",
                data=st.session_state.scattering_data,
                file_name=f'Scattering_Vector_{new_energy:.2f}keV_{new_wavelength:.4f}Å.csv',
                mime='text/csv'
            )