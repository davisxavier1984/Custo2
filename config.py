import streamlit as st

# --- Configuração de cores e tema ---
CORES = {
    "primaria": "#0066CC",
    "secundaria": "#2E8B57",
    "texto": "#333333",
    "destaque": "#FF9900",
    "background": "#F8F9FA",
    "erro": "#DC3545",
    "sucesso": "#28A745",
    "card": "#FFFFFF"
}

# Adicionar CSS personalizado
def local_css():
    st.markdown(f"""
        <style>
        /* Remoção RADICAL de todos os espaços em branco no topo */
        .main .block-container,
        [data-testid="stSidebar"] .block-container,
        div.block-container.css-z5fcl4.ea3mdgi4,
        div.block-container.css-1y4p8pa.ea3mdgi4,
        div.withScreencast,
        div.main.css-k1vhr4.ea3mdgi5,
        div.st-emotion-cache-z5fcl4.ea3mdgi4,
        div.st-emotion-cache-1y4p8pa.ea3mdgi4,
        section[data-testid="stSidebar"] > div,
        div[data-testid="stVerticalBlock"],
        div.stApp,
        header, 
        header[data-testid="stHeader"],
        div.element-container,
        div[class^="st-emotion-cache-"] {{
            padding-top: 0 !important;
            margin-top: 0 !important;
            min-height: 0 !important;
            max-height: none !important;
            height: auto !important;
        }}
        
        /* Forçar todas as margens de todos os elementos para zero */
        div, header, section, main, aside, article, 
        div.element-container.st-emotion-cache-1n76uvr.e1f1d6gn2,
        div.element-container.st-emotion-cache-ocqkz7.e1f1d6gn3 {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Remover decorações e cabeçalhos */
        div[data-testid="stDecoration"],
        div[data-testid="stToolbar"],
        div.stDecorationContainer,
        div.stToolbar {{
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            visibility: hidden !important;
        }}
        
        /* Ajustar o container principal para colar no topo */
        .main .block-container {{
            padding: 0 1rem 5rem 1rem !important;
            max-width: 100% !important;
        }}
        
        /* Sidebar sem espaços */
        [data-testid="stSidebar"] {{
            background-color: white;
            border-right: 1px solid rgba(0,0,0,0.05);
            overflow-y: auto;
            max-height: 100vh;
        }}
        [data-testid="stSidebar"] .block-container {{
            padding: 0 !important;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 0 !important;
            margin-top: 0 !important;
            overflow-y: auto;
            max-height: 100vh;
        }}
        
        /* Estilos para alertas */
        .success-alert {{
            background-color: {CORES["sucesso"]}33;
            border-left: 4px solid {CORES["sucesso"]};
            padding: 0.5rem 1rem;
            border-radius: 4px;
            margin: 0.5rem 0;
        }}

        .error-alert {{
            background-color: {CORES["erro"]}33;
            border-left: 4px solid {CORES["erro"]};
            padding: 0.5rem 1rem;
            border-radius: 4px;
            margin: 0.5rem 0;
        }}

        /* Estilos para métricas */
        .metric-container {{
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }}

        /* Estilos para cabeçalho da página */
        .page-header {{
            background: linear-gradient(135deg, {CORES["primaria"]}22, {CORES["secundaria"]}22);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }}

        /* Data display */
        .date-display {{
            background-color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 0.9rem;
            margin-top: 2rem;
        }}

        /* Footer */
        .footer {{
            margin-top: 3rem;
            padding: 1rem;
            text-align: center;
            font-size: 0.8rem;
            color: #666;
            border-top: 1px solid #eee;
        }}
        
        /* Estilo geral da aplicação */
        .stApp {{
            background-color: {CORES["background"]};
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
        "p2_analise": 2000.0,
        "p2_apuracao": 2500.0,
        "p2_relatorios": 1800.0,
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
        "p2_analise": 3000.0,
        "p2_apuracao": 3200.0,
        "p2_relatorios": 2500.0,
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
        "p2_analise": 4000.0,
        "p2_apuracao": 4500.0,
        "p2_relatorios": 3500.0,
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
        "p2_analise": 5000.0,
        "p2_apuracao": 5500.0,
        "p2_relatorios": 4500.0,
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
        "p2_analise": 6000.0,
        "p2_apuracao": 6500.0,
        "p2_relatorios": 5500.0,
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
        "p2_analise": 7000.0,
        "p2_apuracao": 7500.0,
        "p2_relatorios": 6500.0,
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
        "p2_analise": 8000.0,
        "p2_apuracao": 8500.0,
        "p2_relatorios": 7500.0,
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
        "p2_analise": 10000.0,
        "p2_apuracao": 10500.0,
        "p2_relatorios": 9000.0,
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
        "p2_analise": 12000.0,
        "p2_apuracao": 12500.0,
        "p2_relatorios": 11000.0,
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
        "p2_analise": 14000.0,
        "p2_apuracao": 14500.0,
        "p2_relatorios": 13000.0,
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
        "p2_analise": 16000.0,
        "p2_apuracao": 16500.0,
        "p2_relatorios": 15000.0,
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
        "p2_analise": 18000.0,
        "p2_apuracao": 18500.0,
        "p2_relatorios": 17000.0,
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