import streamlit as st

# --- Configuração de cores e tema ---
CORES = {
    "primaria": "#0066CC",
    "secundaria": "#2E8B57",
    "texto": "#333333",
    "destaque": "#FF9900",
    "background": "#F8F9FA",
    "erro": "#DC3545"
}

# Adicionar CSS personalizado
def local_css():
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {CORES["background"]};
        }}
        h1, h2, h3 {{
            color: {CORES["primaria"]};
        }}
        .stButton>button {{
            background-color: {CORES["primaria"]};
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 15px;
        }}
        .stButton>button:hover {{
            background-color: {CORES["secundaria"]};
        }}
        .total-card {{
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            margin: 10px 0;
            border-left: 5px solid {CORES["destaque"]};
        }}
        .metric-container {{
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }}
        .highlight {{
            color: {CORES["destaque"]};
            font-weight: bold;
        }}
        .footer {{
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: white;
            padding: 10px;
            text-align: center;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        }}
        </style>
    """, unsafe_allow_html=True)

# Valores pré-configurados por faixa populacional
VALORES_POR_FAIXA = {
    "ATÉ 10 MIL HABITANTES": {
        "p1_consultoria": 7000.0,
        "p1_capacitacao": 1500.0,
        "p1_bi": 8000.0,
        "p2_pec": 20000.0,
        "p2_app": 2000.0,
        "p2_regulacao": 3000.0,
        "p2_esus": 2500.0,
        "p2_hosp": 5000.0,
        "p3_cnes": 2500.0,
        "p3_investsus": 1800.0,
        "p3_transferegov": 2000.0,
        "p3_sismob": 1500.0,
        "p3_fpo_bpa": 3000.0
    },
    "10 MIL ATÉ 30 MIL HABITANTES": {
        "p1_consultoria": 9000.0,
        "p1_capacitacao": 2000.0,
        "p1_bi": 12000.0,
        "p2_pec": 30000.0,
        "p2_app": 3500.0,
        "p2_regulacao": 4000.0,
        "p2_esus": 3500.0,
        "p2_hosp": 7000.0,
        "p3_cnes": 3000.0,
        "p3_investsus": 2500.0,
        "p3_transferegov": 2500.0,
        "p3_sismob": 2000.0,
        "p3_fpo_bpa": 3500.0
    },
    "30 A 50 MIL HABITANTES": {
        "p1_consultoria": 12000.0,
        "p1_capacitacao": 2800.0,
        "p1_bi": 16000.0,
        "p2_pec": 40000.0,
        "p2_app": 5000.0,
        "p2_regulacao": 5000.0,
        "p2_esus": 4500.0,
        "p2_hosp": 10000.0,
        "p3_cnes": 3500.0,
        "p3_investsus": 3000.0,
        "p3_transferegov": 3000.0,
        "p3_sismob": 2500.0,
        "p3_fpo_bpa": 4000.0
    },
    "60 A 100 MIL HABITANTES": {
        "p1_consultoria": 15000.0,
        "p1_capacitacao": 3500.0,
        "p1_bi": 20000.0,
        "p2_pec": 50000.0,
        "p2_app": 7500.0,
        "p2_regulacao": 7000.0,
        "p2_esus": 6000.0,
        "p2_hosp": 15000.0,
        "p3_cnes": 4000.0,
        "p3_investsus": 3500.0,
        "p3_transferegov": 3500.0,
        "p3_sismob": 3000.0,
        "p3_fpo_bpa": 5000.0
    },
    "100 A 150 MIL HABITANTES": {
        "p1_consultoria": 18000.0,
        "p1_capacitacao": 4000.0,
        "p1_bi": 25000.0,
        "p2_pec": 60000.0,
        "p2_app": 10000.0,
        "p2_regulacao": 9000.0,
        "p2_esus": 7500.0,
        "p2_hosp": 20000.0,
        "p3_cnes": 5000.0,
        "p3_investsus": 4000.0,
        "p3_transferegov": 4000.0,
        "p3_sismob": 3500.0,
        "p3_fpo_bpa": 6000.0
    },
    "150 MIL A 200 MIL HABITANTES": {
        "p1_consultoria": 20000.0,
        "p1_capacitacao": 4500.0,
        "p1_bi": 30000.0,
        "p2_pec": 70000.0,
        "p2_app": 12000.0,
        "p2_regulacao": 10000.0,
        "p2_esus": 8500.0,
        "p2_hosp": 25000.0,
        "p3_cnes": 6000.0,
        "p3_investsus": 4500.0,
        "p3_transferegov": 4500.0,
        "p3_sismob": 4000.0,
        "p3_fpo_bpa": 7000.0
    },
    "200 A 300 MIL HABITANTES": {
        "p1_consultoria": 25000.0,
        "p1_capacitacao": 5000.0,
        "p1_bi": 35000.0,
        "p2_pec": 80000.0,
        "p2_app": 15000.0,
        "p2_regulacao": 12000.0,
        "p2_esus": 10000.0,
        "p2_hosp": 30000.0,
        "p3_cnes": 7000.0,
        "p3_investsus": 5000.0,
        "p3_transferegov": 5000.0,
        "p3_sismob": 4500.0,
        "p3_fpo_bpa": 8000.0
    },
    "300 A 400 MIL HABITANTES": {
        "p1_consultoria": 30000.0,
        "p1_capacitacao": 6000.0,
        "p1_bi": 40000.0,
        "p2_pec": 100000.0,
        "p2_app": 18000.0,
        "p2_regulacao": 15000.0,
        "p2_esus": 12000.0,
        "p2_hosp": 40000.0,
        "p3_cnes": 8000.0,
        "p3_investsus": 6000.0,
        "p3_transferegov": 6000.0,
        "p3_sismob": 5000.0,
        "p3_fpo_bpa": 9000.0
    },
    "400 A 500 MIL HABITANTES": {
        "p1_consultoria": 35000.0,
        "p1_capacitacao": 7000.0,
        "p1_bi": 45000.0,
        "p2_pec": 120000.0,
        "p2_app": 20000.0,
        "p2_regulacao": 18000.0,
        "p2_esus": 15000.0,
        "p2_hosp": 50000.0,
        "p3_cnes": 9000.0,
        "p3_investsus": 7000.0,
        "p3_transferegov": 7000.0,
        "p3_sismob": 6000.0,
        "p3_fpo_bpa": 10000.0
    },
    "500 A 600 MIL HABITANTES": {
        "p1_consultoria": 40000.0,
        "p1_capacitacao": 8000.0,
        "p1_bi": 50000.0,
        "p2_pec": 140000.0,
        "p2_app": 22000.0,
        "p2_regulacao": 20000.0,
        "p2_esus": 18000.0,
        "p2_hosp": 60000.0,
        "p3_cnes": 10000.0,
        "p3_investsus": 8000.0,
        "p3_transferegov": 8000.0,
        "p3_sismob": 7000.0,
        "p3_fpo_bpa": 12000.0
    },
    "600 A 800 MIL HABITANTES": {
        "p1_consultoria": 45000.0,
        "p1_capacitacao": 9000.0,
        "p1_bi": 55000.0,
        "p2_pec": 160000.0,
        "p2_app": 25000.0,
        "p2_regulacao": 22000.0,
        "p2_esus": 20000.0,
        "p2_hosp": 70000.0,
        "p3_cnes": 12000.0,
        "p3_investsus": 9000.0,
        "p3_transferegov": 9000.0,
        "p3_sismob": 8000.0,
        "p3_fpo_bpa": 15000.0
    },
    "800 MIL A 1 MILHÃO": {
        "p1_consultoria": 50000.0,
        "p1_capacitacao": 10000.0,
        "p1_bi": 60000.0,
        "p2_pec": 180000.0,
        "p2_app": 30000.0,
        "p2_regulacao": 25000.0,
        "p2_esus": 22000.0,
        "p2_hosp": 80000.0,
        "p3_cnes": 15000.0,
        "p3_investsus": 10000.0,
        "p3_transferegov": 10000.0,
        "p3_sismob": 9000.0,
        "p3_fpo_bpa": 18000.0
    }
}

# Lista de faixas populacionais
faixas_populacionais = [
    "ATÉ 10 MIL HABITANTES",
    "10 MIL ATÉ 30 MIL HABITANTES",
    "30 A 50 MIL HABITANTES",
    "60 A 100 MIL HABITANTES",
    "100 A 150 MIL HABITANTES",
    "150 MIL A 200 MIL HABITANTES",
    "200 A 300 MIL HABITANTES",
    "300 A 400 MIL HABITANTES",
    "400 A 500 MIL HABITANTES",
    "500 A 600 MIL HABITANTES",
    "600 A 800 MIL HABITANTES",
    "800 MIL A 1 MILHÃO",
]

# Diretório para salvar os orçamentos
ORCAMENTOS_DIR = "orcamentos"