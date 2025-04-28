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
    
    # Simulação de Contrato Mínimo
    st.markdown("---")
    st.header("Simulação de Contrato Mínimo")
    st.caption("Análise de lucratividade com base nos custos e valores de contrato")
    
    # Inicializar valores na session_state
    if 'contrato_bruto' not in st.session_state: st.session_state.contrato_bruto = 420000.0
    if 'imposto_percentual_contrato' not in st.session_state: st.session_state.imposto_percentual_contrato = 17.0
    if 'valor_fixo_mensal' not in st.session_state: st.session_state.valor_fixo_mensal = 12180.0
    if 'valor_sazonal' not in st.session_state: st.session_state.valor_sazonal = 500.0
    if 'valor_por_contrato' not in st.session_state: st.session_state.valor_por_contrato = 45500.0
    if 'valor_socio' not in st.session_state: st.session_state.valor_socio = 116168.0
    
    col_sim1, col_sim2 = st.columns([1, 1])
    
    with col_sim1:
        st.session_state.contrato_bruto = st.number_input(
            "Valor Contrato Bruto (R$):", 
            min_value=0.0, 
            value=st.session_state.contrato_bruto,
            format="%.2f", 
            key="p2_contrato_bruto_input"  # Chave alterada para ser única
        )
        
        st.session_state.imposto_percentual_contrato = st.number_input(
            "Imposto (%):", 
            min_value=0.0, 
            max_value=100.0,
            value=st.session_state.imposto_percentual_contrato,
            format="%.2f", 
            key="p2_imposto_percentual_input"  # Chave alterada para ser única
        )
        
        st.session_state.valor_socio = st.number_input(
            "Valor Sócio (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_socio,
            format="%.2f", 
            key="p2_valor_socio_input"  # Chave alterada para ser única
        )
    
    with col_sim2:
        st.session_state.valor_fixo_mensal = st.number_input(
            "Custo Fixo Mensal (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_fixo_mensal,
            format="%.2f", 
            key="p2_valor_fixo_mensal_input"  # Chave alterada para ser única
        )
        
        st.session_state.valor_sazonal = st.number_input(
            "Custo Sazonal (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_sazonal,
            format="%.2f", 
            key="p2_valor_sazonal_input"  # Chave alterada para ser única
        )
        
        st.session_state.valor_por_contrato = st.number_input(
            "Custo Por Contrato (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_por_contrato,
            format="%.2f", 
            key="p2_valor_por_contrato_input"  # Chave alterada para ser única
        )
    
    # Cálculos da simulação
    valor_imposto = st.session_state.contrato_bruto * (st.session_state.imposto_percentual_contrato / 100)
    total_despesas = st.session_state.valor_fixo_mensal + st.session_state.valor_sazonal + st.session_state.valor_por_contrato
    resultado_final = st.session_state.contrato_bruto - valor_imposto - total_despesas - st.session_state.valor_socio
    
    # Cálculo da lucratividade
    if st.session_state.contrato_bruto > 0:
        percentual_lucratividade = (resultado_final / st.session_state.contrato_bruto) * 100
    else:
        percentual_lucratividade = 0.0
    
    # Exibir a tabela de simulação usando HTML
    st.markdown("""
        <style>
        .tabela-simulacao {
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }
        .tabela-simulacao th {
            background-color: #0099ff;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .tabela-simulacao td {
            padding: 8px;
            border: 1px solid #ddd;
        }
        .tabela-simulacao tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .tabela-simulacao tr.resultado {
            background-color: #e8f4ea;
            font-weight: bold;
        }
        .tabela-simulacao tr.percentual {
            background-color: #e8f4ea;
        }
        .titulo-tabela {
            background-color: #0099ff;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Criar cada tabela separadamente para evitar problemas de formatação
    tabela_simulacao = f"""
        <div class="titulo-tabela">SIMULAÇÃO CONTRATO MÍNIMO</div>
        <table class="tabela-simulacao">
            <tr>
                <td style="text-align: left; font-weight: bold;">CONTRATO BRUTO</td>
                <td style="text-align: right;">R$ {st.session_state.contrato_bruto:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: left;">IMPOSTO ({st.session_state.imposto_percentual_contrato:.1f}%)</td>
                <td style="text-align: right;">R$ {valor_imposto:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: left;">FIXO MENSAL</td>
                <td style="text-align: right;">R$ {st.session_state.valor_fixo_mensal:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: left;">SAZONAL</td>
                <td style="text-align: right;">R$ {st.session_state.valor_sazonal:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: left;">POR CONTRATO</td>
                <td style="text-align: right;">R$ {st.session_state.valor_por_contrato:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: left;">SÓCIO</td>
                <td style="text-align: right;">R$ {st.session_state.valor_socio:.2f}</td>
            </tr>
            <tr class="resultado">
                <td style="text-align: left;">RESULTADO FINAL CONTRATO</td>
                <td style="text-align: right;">R$ {resultado_final:.2f}</td>
            </tr>
            <tr class="percentual">
                <td style="text-align: left;">PERCENTUAL LUCRATIVIDADE</td>
                <td style="text-align: right;">{percentual_lucratividade:.2f}%</td>
            </tr>
        </table>
    """
    
    tabela_despesas = f"""
        <div class="titulo-tabela" style="margin-top: 20px;">TOTAL DE DESPESA POR CLASSIFICAÇÃO</div>
        <table class="tabela-simulacao">
            <tr>
                <td style="text-align: left; background-color: #e8f4ea;">FIXO MENSAL</td>
                <td style="text-align: right;">R$ {st.session_state.valor_fixo_mensal:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: left; background-color: #fff2cc;">POR CONTRATO</td>
                <td style="text-align: right;">R$ {st.session_state.valor_por_contrato:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: left; background-color: #ffcccc;">SAZONAL</td>
                <td style="text-align: right;">R$ {st.session_state.valor_sazonal:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">TOTAL</td>
                <td style="text-align: right;">R$ {total_despesas:.2f}</td>
            </tr>
        </table>
    """
    
    # Exibir as tabelas
    st.markdown(tabela_simulacao, unsafe_allow_html=True)
    st.markdown(tabela_despesas, unsafe_allow_html=True)
    
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