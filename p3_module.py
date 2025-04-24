import streamlit as st
import pandas as pd
import plotly.express as px
from config import VALORES_POR_FAIXA, faixas_populacionais
from utils import formatar_valor_reais, metric_card

def display_p3_calculator():
    st.header("P3 - Sistemas de Saúde")
    st.caption("Configure os valores de sistemas oficiais de integração com o Ministério da Saúde.")

    col1, col2 = st.columns([1.2, 2])

    with col1:
        # Reutilizar a faixa populacional já selecionada
        faixa = st.session_state.get('faixa_populacional', faixas_populacionais[0])
        st.subheader(f"Faixa: {faixa}")
        
        # Sugerir valores com base na faixa populacional
        if st.button("📊 Sugerir Valores de Integração", help="Preenche com valores sugeridos para esta faixa populacional"):
            if faixa in VALORES_POR_FAIXA:
                valores_sugeridos = VALORES_POR_FAIXA[faixa]
                
                st.session_state.p3_cnes_val = valores_sugeridos.get("p3_cnes", 2500.0)
                st.session_state.p3_investsus_val = valores_sugeridos.get("p3_investsus", 1800.0)
                # Definir outros valores com valores padrão
                st.session_state.p3_transferegov_val = valores_sugeridos.get("p3_transferegov", 2000.0)
                st.session_state.p3_sismob_val = valores_sugeridos.get("p3_sismob", 1500.0)
                st.session_state.p3_fpo_bpa_val = valores_sugeridos.get("p3_fpo_bpa", 3000.0)
                
                st.success(f"Valores de integração sugeridos aplicados!")
                
        # Adicionar algumas informações sobre os sistemas
        with st.expander("ℹ️ Informações sobre Sistemas de Integração"):
            st.markdown("""
            * **CNES**: Cadastro Nacional de Estabelecimentos de Saúde
            * **InvestSUS**: Plataforma para gestão dos recursos da enfermagem
            * **TransfereGov**: Integração com sistema de transferências do Governo Federal
            * **SISMOB**: Sistema de Monitoramento de Obras
            * **FPO e BPA**: Ficha de Programação Orçamentária e Boletim de Produção Ambulatorial
            """)

    with col2:
        st.subheader("Valores dos Sistemas de Integração")
        
        # Inputs para valores
        if 'p3_cnes_val' not in st.session_state: st.session_state.p3_cnes_val = 0.0
        if 'p3_investsus_val' not in st.session_state: st.session_state.p3_investsus_val = 0.0
        if 'p3_transferegov_val' not in st.session_state: st.session_state.p3_transferegov_val = 0.0
        if 'p3_sismob_val' not in st.session_state: st.session_state.p3_sismob_val = 0.0
        if 'p3_fpo_bpa_val' not in st.session_state: st.session_state.p3_fpo_bpa_val = 0.0

        col_a, col_b = st.columns(2)
        
        with col_a:
            val_cnes = st.number_input(
                "Integração CNES:",
                min_value=0.0,
                format="%.2f",
                key="p3_cnes_val",
                help="Sistema de integração com o Cadastro Nacional de Estabelecimentos de Saúde"
            )
            
            val_investsus = st.number_input(
                "InvestSUS (Piso da Enfermagem):",
                min_value=0.0,
                format="%.2f",
                key="p3_investsus_val",
                help="Sistema para gestão dos recursos da enfermagem"
            )
            
            val_transferegov = st.number_input(
                "Integração TransfereGov:",
                min_value=0.0,
                format="%.2f",
                key="p3_transferegov_val",
                help="Integração com sistema de transferências do Governo Federal"
            )
            
        with col_b:
            val_sismob = st.number_input(
                "Integração SISMOB:",
                min_value=0.0,
                format="%.2f",
                key="p3_sismob_val",
                help="Integração com o Sistema de Monitoramento de Obras"
            )
            
            val_fpo_bpa = st.number_input(
                "Sistema FPO e BPA:",
                min_value=0.0,
                format="%.2f",
                key="p3_fpo_bpa_val",
                help="Sistema para Ficha de Programação Orçamentária e Boletim de Produção Ambulatorial"
            )

    # Cálculo Total
    total_p3 = val_cnes + val_investsus + val_transferegov + val_sismob + val_fpo_bpa
    
    # Exibição dos resultados em cards visuais
    st.markdown("### Resumo dos Sistemas de Integração")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("CNES", val_cnes)
        metric_card("TransfereGov", val_transferegov)
    
    with col2:
        metric_card("InvestSUS", val_investsus)
        metric_card("SISMOB", val_sismob)
    
    with col3:
        metric_card("FPO e BPA", val_fpo_bpa)
    
    # Card do total
    st.markdown(f"""
    <div class="total-card">
        <h3>TOTAL P3 - SISTEMAS DE INTEGRAÇÃO</h3>
        <h2>{formatar_valor_reais(total_p3)}</h2>
        <p>Valor único ou anual: {formatar_valor_reais(total_p3)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de comparação
    if total_p3 > 0:
        dados = pd.DataFrame({
            'Sistema': ['CNES', 'InvestSUS', 'TransfereGov', 'SISMOB', 'FPO e BPA'],
            'Valor': [val_cnes, val_investsus, val_transferegov, val_sismob, val_fpo_bpa]
        })
        
        fig = px.bar(
            dados, 
            x='Sistema', 
            y='Valor', 
            title='Distribuição de Custos por Sistema',
            color='Sistema',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Salvar o total na session_state para exibição consolidada
    st.session_state.total_p3 = total_p3