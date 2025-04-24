import streamlit as st
import pandas as pd
from datetime import datetime as dt
from PIL import Image

# Importar módulos personalizados
from config import local_css, faixas_populacionais
from utils import get_logo
from database import display_save_load_section
from p1_module import display_p1_calculator
from p2_module import display_p2_calculator
from p3_module import display_p3_calculator
from summary import display_summary
from accounting_module import display_accounting_costs

# --- Configuração da Página ---
st.set_page_config(
    page_title="Sistema de Orçamento - Mais Gestor",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:suporte@maisgestor.com.br',
        'About': "# Sistema de Orçamento - Mais Gestor\nFerramentas para gestão de saúde municipal."
    }
)

# Aplicar CSS personalizado
local_css()

# --- Interface Principal ---

# Carregar logotipo
logo = get_logo()
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image(logo, width=150)

with col_title:
    st.title("Sistema de Orçamento - Mais Gestor")
    st.caption("Configure o orçamento ideal para cada município com base nas necessidades e porte populacional")

# Adicionar cabeçalho com data atual
st.markdown(
    f"""
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <p style="margin: 0; text-align: right;">Data: {dt.now().strftime('%d/%m/%Y')}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Seleção do Produto na Barra Lateral
st.sidebar.title("Navegação")

# Adicionar campo de cliente na barra lateral
cliente = st.sidebar.text_input("Nome do Cliente:", key="client_name", placeholder="Ex: Prefeitura de São Paulo")
if cliente:
    st.sidebar.success(f"📋 Cliente: {cliente}")

# Adicionar outros campos de informação do cliente
with st.sidebar.expander("Informações Adicionais"):
    st.text_input("Nome do Responsável:", key="responsavel_name", placeholder="Nome do contato")
    st.text_input("Cargo/Função:", key="responsavel_cargo", placeholder="Ex: Secretário de Saúde")
    st.text_input("Email para Contato:", key="email_contato", placeholder="email@exemplo.com")
    st.text_input("Telefone:", key="telefone", placeholder="(XX) XXXXX-XXXX")

# Abas para navegação (adicionando a nova aba de Contabilidade)
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

# Botão para Limpar entradas (funciona por produto selecionado)
with st.sidebar:
    st.markdown("### Ações")
    
    if st.button("🔄 Limpar Todas as Entradas"):
        # Resetar todos os valores
        for key in list(st.session_state.keys()):
            if key.endswith('_val'):
                st.session_state[key] = 0.0
        
        # Resetar quantidades
        st.session_state.p1_qtd = 1
        st.session_state.p2_qtd = 1
        st.session_state.p2_qtd_ace = 0
        st.session_state.faixa_populacional = faixas_populacionais[0]
        
        # Força o rerender da página para mostrar os campos limpos
        st.rerun()

    st.markdown("---")
    st.markdown("### Sobre o Sistema")
    st.markdown("""
    O Sistema de Orçamento Mais Gestor permite a criação de orçamentos personalizados 
    para serviços de saúde municipais. Configure valores com base no porte do município 
    e na quantidade de unidades de saúde.
    """)

# Rodapé
st.markdown("---")
st.caption("© 2025 Mais Gestor - Soluções em Gestão de Saúde | Versão 2.0")