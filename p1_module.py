import streamlit as st
import pandas as pd
import plotly.express as px
from config import VALORES_POR_FAIXA, faixas_populacionais
from utils import formatar_valor_reais, metric_card

def display_p1_calculator():
    st.header("P1 - Consultoria e Incremento")
    st.caption("Configure os valores mensais de consultoria com base na quantidade de unidades.")

    # Usar colunas para melhor layout
    col1, col2 = st.columns([1.2, 2]) 

    with col1:
        # Usar session_state para guardar o valor entre interações
        if 'p1_qtd' not in st.session_state:
            st.session_state.p1_qtd = 1
        
        # Seleção de faixa populacional para valores sugeridos
        if 'faixa_populacional' not in st.session_state:
            st.session_state.faixa_populacional = faixas_populacionais[0]
            
        faixa = st.selectbox(
            "Faixa Populacional do Município:",
            options=faixas_populacionais,
            key="faixa_populacional",
            help="Selecione a faixa populacional para sugestão de valores"
        )
        
        qtd_unidades = st.number_input(
            "Quantidade de Unidades de Saúde:", 
            min_value=1, 
            step=1, 
            key="p1_qtd",
            help="Informe o número total de unidades de saúde do município"
        )
        
        # Sugerir valores com base na faixa populacional
        if st.button("📊 Sugerir Valores", help="Preenche com valores sugeridos para esta faixa populacional"):
            if faixa in VALORES_POR_FAIXA:
                valores_sugeridos = VALORES_POR_FAIXA[faixa]
                # Ajustar valores com base no número de unidades
                fator_ajuste = max(1.0, qtd_unidades / 5)  # Ajuste a cada 5 unidades
                
                st.session_state.p1_consultoria_val = valores_sugeridos["p1_consultoria"] * fator_ajuste
                st.session_state.p1_capacitacao_val = valores_sugeridos["p1_capacitacao"] * fator_ajuste
                st.session_state.p1_bi_val = valores_sugeridos["p1_bi"] * fator_ajuste
                
                st.success(f"Valores sugeridos aplicados para {faixa} com {qtd_unidades} unidades!")
        
        st.info("💡 Os valores sugeridos são calculados com base na faixa populacional e na quantidade de unidades.")
        
    with col2:
        st.subheader("Valores dos Serviços")
        # Inputs para valores - operador digita
        if 'p1_consultoria_val' not in st.session_state: st.session_state.p1_consultoria_val = 0.0
        if 'p1_capacitacao_val' not in st.session_state: st.session_state.p1_capacitacao_val = 0.0
        if 'p1_bi_val' not in st.session_state: st.session_state.p1_bi_val = 0.0

        col_a, col_b = st.columns(2)
        
        with col_a:
            val_consultoria = st.number_input(
                "Valor Consultoria e Incremento:",
                min_value=0.0,
                format="%.2f",
                key="p1_consultoria_val",
                help="Valor mensal para serviços de consultoria em gestão de saúde"
            )
            
            val_capacitacao = st.number_input(
                "Valor Capacitação Profissionais:",
                min_value=0.0,
                format="%.2f",
                key="p1_capacitacao_val",
                help="Valor mensal para capacitação de profissionais (4h/mês)"
            )
        
        with col_b:
            val_bi = st.number_input(
                "Valor BI Inteligente:",
                min_value=0.0,
                format="%.2f",
                key="p1_bi_val",
                help="Valor mensal para serviços de Business Intelligence aplicados à saúde"
            )
            
            # Espaço para alinhamento visual
            st.write("")
            st.write("")

    # Cálculo Total
    total_p1 = val_consultoria + val_capacitacao + val_bi
    
    # Exibição dos resultados em cards visuais
    st.markdown("### Resumo do Orçamento")
    cols = st.columns([1, 1, 1])
    
    with cols[0]:
        metric_card("Consultoria e Incremento", val_consultoria)
    
    with cols[1]:
        metric_card("Capacitação de Profissionais", val_capacitacao)
    
    with cols[2]:
        metric_card("BI Inteligente", val_bi)
    
    # Card do total
    st.markdown(f"""
    <div class="total-card">
        <h3>TOTAL MENSAL P1</h3>
        <h2>{formatar_valor_reais(total_p1)}</h2>
        <p>Valor estimado anual: {formatar_valor_reais(total_p1 * 12)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de distribuição
    if total_p1 > 0:
        dados = pd.DataFrame({
            'Serviço': ['Consultoria', 'Capacitação', 'BI Inteligente'],
            'Valor': [val_consultoria, val_capacitacao, val_bi],
            'Porcentagem': [val_consultoria/total_p1*100, val_capacitacao/total_p1*100, val_bi/total_p1*100]
        })
        
        fig = px.pie(
            dados, 
            values='Valor', 
            names='Serviço',
            title='Distribuição dos Serviços P1',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Salvar o total na session_state para exibição consolidada
    st.session_state.total_p1 = total_p1