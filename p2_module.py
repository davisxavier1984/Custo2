import streamlit as st
import pandas as pd
import plotly.express as px
from config import VALORES_POR_FAIXA, faixas_populacionais
from utils import formatar_valor_reais, metric_card

def display_p2_calculator():
    st.header("P2 - Contabilidade de Custos")
    st.caption("Configure os valores mensais para contabilidade de custos com base na quantidade de unidades.")
    
    # Usar colunas para melhor layout
    col1, col2 = st.columns([1.2, 2])
    
    with col1:
        # Usar session_state para guardar o valor entre interações
        if 'p2_qtd' not in st.session_state:
            st.session_state.p2_qtd = 1
            
        # Reutilizar a faixa populacional já selecionada
        faixa = st.session_state.get('faixa_populacional', faixas_populacionais[0])
        st.subheader(f"Faixa: {faixa}")
        
        qtd_unidades = st.number_input(
            "Quantidade de Unidades de Saúde:", 
            min_value=1, 
            step=1, 
            key="p2_qtd",
            help="Informe o número total de unidades de saúde do município"
        )
        
        # Sugerir valores com base na faixa populacional
        if st.button("📊 Sugerir Valores", key="p2_sugerir", help="Preenche com valores sugeridos para esta faixa populacional"):
            if faixa in VALORES_POR_FAIXA:
                valores_sugeridos = VALORES_POR_FAIXA[faixa]
                # Ajustar valores com base no número de unidades
                fator_ajuste = max(1.0, qtd_unidades / 5)  # Ajuste a cada 5 unidades
                
                st.session_state.p2_analise_val = valores_sugeridos["p2_analise"] * fator_ajuste
                st.session_state.p2_apuracao_val = valores_sugeridos["p2_apuracao"] * fator_ajuste
                st.session_state.p2_relatorios_val = valores_sugeridos["p2_relatorios"] * fator_ajuste
                
                st.success(f"Valores sugeridos aplicados para {faixa} com {qtd_unidades} unidades!")
        
        st.info("💡 Os valores sugeridos são calculados com base na faixa populacional e na quantidade de unidades.")
        
    with col2:
        st.subheader("Valores dos Serviços")
        # Inputs para valores - operador digita
        if 'p2_analise_val' not in st.session_state: st.session_state.p2_analise_val = 0.0
        if 'p2_apuracao_val' not in st.session_state: st.session_state.p2_apuracao_val = 0.0
        if 'p2_relatorios_val' not in st.session_state: st.session_state.p2_relatorios_val = 0.0
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            val_analise = st.number_input(
                "Análise de Produção:",
                min_value=0.0,
                format="%.2f",
                key="p2_analise_val",
                help="Valor mensal para análise detalhada da produção em saúde"
            )
            
            val_apuracao = st.number_input(
                "Apuração de Custos:",
                min_value=0.0,
                format="%.2f",
                key="p2_apuracao_val",
                help="Valor mensal para apuração de custos dos serviços de saúde"
            )
        
        with col_b:
            val_relatorios = st.number_input(
                "Relatórios Gerenciais:",
                min_value=0.0,
                format="%.2f",
                key="p2_relatorios_val",
                help="Valor mensal para geração de relatórios gerenciais"
            )
            
            # Espaço para alinhamento visual
            st.write("")
            st.write("")
    
    # Cálculo do total
    total_p2 = val_analise + val_apuracao + val_relatorios
    
    # Exibição dos resultados com métricas simples
    st.markdown("### Resumo do Orçamento")
    cols = st.columns([1, 1, 1])
    
    with cols[0]:
        metric_card("Análise de Produção", val_analise)
    
    with cols[1]:
        metric_card("Apuração de Custos", val_apuracao)
    
    with cols[2]:
        metric_card("Relatórios Gerenciais", val_relatorios)
    
    # Total sem card, usando métrica padrão
    st.subheader("TOTAL MENSAL P2")
    st.metric("Total", formatar_valor_reais(total_p2), delta=f"Anual: {formatar_valor_reais(total_p2 * 12)}")
    
    # Gráfico de distribuição
    if total_p2 > 0:
        dados = pd.DataFrame({
            'Serviço': ['Análise de Produção', 'Apuração de Custos', 'Relatórios Gerenciais'],
            'Valor': [val_analise, val_apuracao, val_relatorios],
            'Porcentagem': [val_analise/total_p2*100, val_apuracao/total_p2*100, val_relatorios/total_p2*100]
        })
        
        fig = px.pie(
            dados, 
            values='Valor', 
            names='Serviço',
            title='Distribuição dos Serviços P2',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Salvar o total na session_state para exibição consolidada
    st.session_state.total_p2 = total_p2