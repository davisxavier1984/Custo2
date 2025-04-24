import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime as dt
from utils import formatar_valor_reais, metric_card, create_comparison_chart, generate_pdf_link

def display_summary():
    st.header("Resumo do Orçamento Completo")
    st.caption("Visualize o orçamento consolidado com todos os serviços selecionados.")
    
    # Configurações financeiras - adicionando campos para comissão, lucro e impostos
    with st.expander("⚙️ Configurações Financeiras", expanded=False):
        st.subheader("Ajustes Financeiros")
        
        # Inicializar valores no session_state
        if 'comissao_percentual' not in st.session_state: st.session_state.comissao_percentual = 5.0
        if 'lucro_percentual' not in st.session_state: st.session_state.lucro_percentual = 20.0
        if 'imposto_percentual' not in st.session_state: st.session_state.imposto_percentual = 8.65
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            comissao_percentual = st.number_input(
                "Comissão (%)",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.comissao_percentual,
                step=0.5,
                format="%.2f",
                key="comissao_percentual",
                help="Percentual para comissão de vendas"
            )
        
        with col2:
            lucro_percentual = st.number_input(
                "Lucro (%)",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.lucro_percentual,
                step=0.5,
                format="%.2f",
                key="lucro_percentual",
                help="Percentual de lucro sobre o valor"
            )
            
        with col3:
            imposto_percentual = st.number_input(
                "Impostos (%)",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.imposto_percentual,
                step=0.05,
                format="%.2f",
                key="imposto_percentual",
                help="Percentual de impostos sobre o valor"
            )
    
    # Recuperar valores dos orçamentos
    total_p1 = st.session_state.get('total_p1', 0)
    total_p2 = st.session_state.get('total_p2', 0)
    total_p3 = st.session_state.get('total_p3', 0)
    
    # Valor base sem adicionais
    total_base_mensal = total_p1 + total_p2
    
    # Cálculos de valores adicionais
    comissao_valor = total_base_mensal * (st.session_state.comissao_percentual / 100)
    lucro_valor = total_base_mensal * (st.session_state.lucro_percentual / 100)
    impostos_valor = total_base_mensal * (st.session_state.imposto_percentual / 100)
    
    # Total com adicionais
    total_geral_mensal = total_base_mensal + comissao_valor + lucro_valor + impostos_valor
    total_geral_anual = total_geral_mensal * 12 + total_p3
    
    # Exibir informações do cliente
    cliente = st.session_state.get('client_name', '')
    faixa = st.session_state.get('faixa_populacional', '')
    
    if cliente:
        st.subheader(f"Cliente: {cliente}")
    st.subheader(f"Faixa Populacional: {faixa}")
    
    # Criar tabela resumo
    st.markdown("### Valores Mensais")
    
    dados_mensais = pd.DataFrame({
        'Categoria': ['P1 - Consultoria', 'P2 - Tecnologia', 'Subtotal', 'Comissão', 'Lucro', 'Impostos', 'Total Mensal'],
        'Valor': [total_p1, total_p2, total_base_mensal, comissao_valor, lucro_valor, impostos_valor, total_geral_mensal]
    })
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Exibir tabela de valores
        st.dataframe(
            dados_mensais,
            column_config={
                "Categoria": st.column_config.TextColumn("Categoria"),
                "Valor": st.column_config.NumberColumn(
                    "Valor Mensal",
                    format="R$ %.2f",
                )
            },
            hide_index=True,
        )
    
    with col2:
        if total_geral_mensal > 0:
            # Gráfico de pizza
            fig = px.pie(
                dados_mensais[:-1],  # Remover a linha de total
                values='Valor', 
                names='Categoria',
                hole=.4,
                color_discrete_sequence=['#0066CC', '#2E8B57']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Exibir o total P3 (Sistemas de Integração)
    st.markdown("### Valores Únicos/Anuais")
    st.metric("P3 - Sistemas de Integração", formatar_valor_reais(total_p3))
    
    # Card do orçamento total com detalhamento
    st.markdown(f"""
    <div class="total-card" style="background-color: #f8f9fa; border-left-color: #0066CC; padding: 25px;">
        <h2 style="margin-bottom: 5px;">ORÇAMENTO TOTAL</h2>
        <p style="font-size: 0.9em; margin-bottom: 15px;">Valor mensal de serviços contínuos + sistemas de integração</p>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div>
                <p style="font-size: 0.9em; margin: 0;">Valor Base Mensal:</p>
                <h4 style="margin: 0;">{formatar_valor_reais(total_base_mensal)}</h4>
                <p style="font-size: 0.9em; margin: 5px 0 0 0;">Comissão ({st.session_state.comissao_percentual}%): {formatar_valor_reais(comissao_valor)}</p>
                <p style="font-size: 0.9em; margin: 0;">Lucro ({st.session_state.lucro_percentual}%): {formatar_valor_reais(lucro_valor)}</p>
                <p style="font-size: 0.9em; margin: 0;">Impostos ({st.session_state.imposto_percentual}%): {formatar_valor_reais(impostos_valor)}</p>
                <h3 style="margin: 10px 0 0 0;">Total Mensal: {formatar_valor_reais(total_geral_mensal)}</h3>
            </div>
            <div>
                <p style="font-size: 0.9em; margin: 0;">Valor Anual:</p>
                <h3 style="margin: 0;">{formatar_valor_reais(total_geral_anual)}</h3>
                <p style="font-size: 0.8em; margin: 5px 0 0 0;">(12x mensal + P3)</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Atualizar dados detalhados para incluir comodato
    if 'p2_comodato_val' not in st.session_state: st.session_state.p2_comodato_val = 0
    
    dados_detalhados = pd.DataFrame({
        'Serviço': [
            'Consultoria', 'Capacitação', 'BI Inteligente',
            'PEC Servidor', 'App ACE', 'Comodato Aparelhos', 'Regulação', 'eSUS Farma', 'Sistema Hospitalar',
            'CNES', 'InvestSUS', 'TransfereGov', 'SISMOB', 'FPO e BPA'
        ],
        'Valor': [
            st.session_state.p1_consultoria_val, 
            st.session_state.p1_capacitacao_val,
            st.session_state.p1_bi_val,
            st.session_state.p2_pec_val,
            st.session_state.p2_app_val,
            st.session_state.p2_comodato_val,
            st.session_state.p2_regulacao_val,
            st.session_state.p2_esus_val,
            st.session_state.p2_hosp_val,
            st.session_state.p3_cnes_val,
            st.session_state.p3_investsus_val,
            st.session_state.p3_transferegov_val,
            st.session_state.p3_sismob_val,
            st.session_state.p3_fpo_bpa_val
        ],
        'Categoria': [
            'P1', 'P1', 'P1',
            'P2', 'P2', 'P2', 'P2', 'P2', 'P2',
            'P3', 'P3', 'P3', 'P3', 'P3'
        ]
    })
    
    # Filtrar valores maiores que zero
    dados_filtrados = dados_detalhados[dados_detalhados['Valor'] > 0]
    
    if not dados_filtrados.empty:
        fig = create_comparison_chart(
            dados_filtrados, 
            'Comparativo de Todos os Serviços Selecionados'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Configure os valores dos serviços nas abas anteriores para visualizar o comparativo.")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Baixar Orçamento em CSV",
            data=dados_detalhados.to_csv(index=False).encode('utf-8'),
            file_name=f"orcamento_mais_gestor_{dt.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        generate_pdf_link()