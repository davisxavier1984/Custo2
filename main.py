import streamlit as st
import pandas as pd
from datetime import datetime as dt
from PIL import Image

# Configuração da página principal - DEVE ser o primeiro comando Streamlit
st.set_page_config(
    page_title="Sistema de Orçamento - Mais Gestor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:suporte@maisgestor.com.br',
        'About': "# Sistema de Orçamento - Mais Gestor\nFerramentas para gestão de saúde municipal."
    }
)

# Importar módulos personalizados
from config import local_css, faixas_populacionais, VALORES_POR_FAIXA
from utils import get_logo
from database import display_save_load_section
from p1_module import display_p1_calculator
from p2_module import display_p2_calculator
from p3_module import display_p3_calculator
from summary import display_summary
from accounting_module import display_accounting_costs
from auth import init_auth, login_page, logout, change_password

# Inicializar session state para evitar erros
if "p1_qtd" not in st.session_state:
    st.session_state.p1_qtd = 1
if "p2_qtd" not in st.session_state:
    st.session_state.p2_qtd = 1
if "p2_qtd_ace" not in st.session_state:
    st.session_state.p2_qtd_ace = 0
if "faixa_populacional" not in st.session_state:
    st.session_state.faixa_populacional = faixas_populacionais[0]

# Inicializar valores dos módulos
faixa_padrao = faixas_populacionais[0]
valores_padrao = VALORES_POR_FAIXA[faixa_padrao]

# P1
if "p1_consultoria_val" not in st.session_state:
    st.session_state.p1_consultoria_val = valores_padrao.get("p1_consultoria", 0.0)
if "p1_capacitacao_val" not in st.session_state:
    st.session_state.p1_capacitacao_val = valores_padrao.get("p1_capacitacao", 0.0)
if "p1_bi_val" not in st.session_state:
    st.session_state.p1_bi_val = valores_padrao.get("p1_bi", 0.0)

# P2
if "p2_pec_val" not in st.session_state:
    st.session_state.p2_pec_val = valores_padrao.get("p2_pec", 0.0)
if "p2_app_val" not in st.session_state:
    st.session_state.p2_app_val = valores_padrao.get("p2_app", 0.0)
if "p2_regulacao_val" not in st.session_state:
    st.session_state.p2_regulacao_val = valores_padrao.get("p2_regulacao", 0.0)
if "p2_esus_val" not in st.session_state:
    st.session_state.p2_esus_val = valores_padrao.get("p2_esus", 0.0)
if "p2_hosp_val" not in st.session_state:
    st.session_state.p2_hosp_val = valores_padrao.get("p2_hosp", 0.0)

# P3
if "p3_cnes_val" not in st.session_state:
    st.session_state.p3_cnes_val = valores_padrao.get("p3_cnes", 0.0)
if "p3_investsus_val" not in st.session_state:
    st.session_state.p3_investsus_val = valores_padrao.get("p3_investsus", 0.0)
if "p3_transferegov_val" not in st.session_state:
    st.session_state.p3_transferegov_val = valores_padrao.get("p3_transferegov", 0.0)
if "p3_sismob_val" not in st.session_state:
    st.session_state.p3_sismob_val = valores_padrao.get("p3_sismob", 0.0)
if "p3_fpo_bpa_val" not in st.session_state:
    st.session_state.p3_fpo_bpa_val = valores_padrao.get("p3_fpo_bpa", 0.0)

# Inicializar autenticação
init_auth()

# Variável para controlar a exibição da tela de alteração de senha
if 'show_change_password' not in st.session_state:
    st.session_state.show_change_password = False

# Verificar autenticação
if not st.session_state.authenticated:
    login_page()
else:
    # Aplicar CSS personalizado
    local_css()

    # --- Interface Principal ---
    # Header com logo e título
    col_logo, col_title, col_date = st.columns([1, 3, 1])
    
    with col_logo:
        logo = get_logo()
        st.image(logo, width=200)
    
    with col_title:
        st.title("Sistema de Orçamento - Mais Gestor")
        st.caption("Configure o orçamento ideal para cada município com base nas necessidades e porte populacional")
    
    with col_date:
        st.markdown(f'<div class="date-display">Data: {dt.now().strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)

    # Sidebar com informações do cliente e navegação
    with st.sidebar:
        # Altura máxima para garantir que a sidebar tenha rolagem
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            min-height: 100vh;
            height: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Cliente (primeira seção)
        st.markdown('<h3>📋 Cliente</h3>', unsafe_allow_html=True)
        cliente = st.text_input("Nome do Cliente:", key="client_name", placeholder="Ex: Prefeitura de São Paulo")
        if cliente:
            st.markdown(f'<div class="success-alert">Cliente: {cliente}</div>', unsafe_allow_html=True)
        
        with st.expander("ℹ️ Informações Adicionais"):
            st.text_input("Nome do Responsável:", key="responsavel_name", placeholder="Nome do contato")
            st.text_input("Cargo/Função:", key="responsavel_cargo", placeholder="Ex: Secretário de Saúde")
            st.text_input("Email para Contato:", key="email_contato", placeholder="email@exemplo.com")
            st.text_input("Telefone:", key="telefone", placeholder="(XX) XXXXX-XXXX")
        
        # Ações
        st.markdown('<h3>⚡ Ações</h3>', unsafe_allow_html=True)
        if st.button("🔄 Limpar Todas as Entradas", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.endswith('_val'):
                    st.session_state[key] = 0.0
            st.session_state.p1_qtd = 1
            st.session_state.p2_qtd = 1
            st.session_state.p2_qtd_ace = 0
            st.session_state.faixa_populacional = faixas_populacionais[0]
            st.rerun()

        # Sobre o Sistema
        st.markdown("<h3>📖 Sobre o Sistema</h3>", unsafe_allow_html=True)
        st.markdown("""
        O Sistema de Orçamento Mais Gestor permite a criação de orçamentos personalizados 
        para serviços de saúde municipais. Configure valores com base no porte do município 
        e na quantidade de unidades de saúde.
        """)
        
        # Espaçador para garantir que o último elemento seja visível
        st.markdown("<div style='padding: 20px'></div>", unsafe_allow_html=True)
        
        # Área da conta simplificada
        st.markdown('<h3>👤 Conta</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Alterar Senha", use_container_width=True):
                st.session_state.show_change_password = True
                st.rerun()
        with col2:
            if st.button("🚪 Sair", use_container_width=True):
                logout()
        
        # Garantir espaço no final para não cortar elementos
        st.markdown("<div style='padding: 20px'></div>", unsafe_allow_html=True)

    # Mostrar tela de alteração de senha se necessário
    if st.session_state.show_change_password:
        # Botão para voltar à tela principal
        if st.button("← Voltar ao sistema", use_container_width=True):
            st.session_state.show_change_password = False
            st.rerun()
        
        # Renderizar o formulário de alteração de senha em área mais larga
        change_password()
    else:
        # Conteúdo principal com tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 P1 - Consultoria", 
            "💻 P2 - Tecnologia", 
            "🔄 P3 - Integração", 
            "📝 Resumo", 
            "💰 Contabilidade",
            "💾 Gerenciar Orçamentos"
        ])

        with tab1:
            display_p1_calculator()

        with tab2:
            display_p2_calculator()

        with tab3:
            display_p3_calculator()

        with tab4:
            display_summary()

        with tab5:
            display_accounting_costs()

        with tab6:
            display_save_load_section()

    # Footer
    st.markdown(
        '<div class="footer">© 2025 Mais Gestor - Soluções em Gestão de Saúde | Versão 2.0</div>',
        unsafe_allow_html=True
    )