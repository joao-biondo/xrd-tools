import streamlit as st
import base64
# Configurar a página inicial
st.set_page_config(page_title='Paineira - XRD Tools Web App', 
                   page_icon='Icons/Paineira-Logo.png', layout='wide')

# Função para usar imagens como plano de fundo
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        image = f.read()
    return base64.b64encode(image).decode()

img = get_img_as_base64('Icons/Paineira-Layout.png')
st.logo('Icons/Paineira-Logo.png', link='https://lnls.cnpem.br/facilities/paineira-en/', icon_image='Icons/Paineira-Layout.png', size='large')
# Caixa para o título (cor de fundo diferenciada)
st.markdown(
    f"""
    <div style="background-color: #FF4B4B; border-radius: 5px; padding: 2px; margin-bottom: 20px;">  
        <h1 style="color: black; text-align: center;"> XRD Tools Web App</h1>
    </div>
    """, unsafe_allow_html=True
)

st.image('Icons/Paineira-Logo.png', use_container_width=True)



# Seção "About" com fundo sólido
with st.expander('About this app', expanded=True, icon=":material/help:"):    
    st.markdown(r"""
            ### What is this app ?
            This page was desinged to be a web app for X-ray Diffraction (XRD) quick and useful tools. Here you'll find 
            a X-ray attenuation calculator and a XRD data energy conversion. Currently, a X-ray footprint calculator, for 
            reflection geometry XRD, is being developed as we look forward to put it online until the end of the semester. 
            This app was developed with the day-to-day needs of the Paineira Beamline in mind, nevertheless, it might be usefull
            to any user with a research field related to XRD experiments.
            ### Paineira Beamline
            Paineira is a beamline located at Sirius, the Brazilian synchrotron light source. Paineira is dedicated to X-ray Powder Diffraction,
            a technique for characterization of crystalline samples. The beamline is capable of *in situ* and *ex situ* XRD experiments.
            The tools present in this app are based on the daily needs of these type of experiments. 
            ### Authors
            This app was developed by:
            - João Luis Biondo Neto/joao.neto@lnls.br --> Paineira Intern
            - José Victor da Silva Izidorio --> Ilum student and Paineira Summer Intern
            - Emanuel Piveta Pozzobon --> Ilum student and Paineira Summer Intern
            """)



# CSS customizado
page_bg_img = f"""
<style>
html, body {{
    overflow: auto !important;
    font-family: "Open Sans", serif;
    font-size: larger
}}
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;

}}


/* Estilizando a seção About*/
[data-testid="stExpander"] {{
    background-color: #ff4b4b;
    border-radius: 8px;
    padding: 10px;
    font-size: 30px
}}

[data-testid="stHeader"] {{
    background-color: rgba(256,0,0,0);

}}

</style>

"""

st.markdown(page_bg_img, unsafe_allow_html=True)