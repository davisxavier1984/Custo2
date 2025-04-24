import streamlit as st
import pandas as pd
import plotly.express as px
from config import VALORES_POR_FAIXA
from utils import formatar_valor_reais, metric_card

def display_p2_calculator():
    st.header("P2 - Serviços Tecnológicos")
    st.caption("Configure os valores mensais de serviços tecnológicos com base nas necessidades do município.")

    col1, col2 = st.columns([1.2, 2])

    with col1:
        if 'p2_qtd' not in st.session_state: st.session_state.p2_qtd = 1
        if 'p2_qtd_ace' not in st.session_state: st.session_state.p2_qtd_ace = 0
        
        # Reutilizar a faixa populacional já selecionada
        faixa = st.session_state.get('faixa_populacional', None)
        st.subheader(f"Faixa: {faixa}")
        
        qtd_unidades_p2 = st.number_input(
            "Quantidade de Unidades:", 
            min_value=1, 
            step=1, 
            key="p2_qtd",
            help="Número de unidades que receberão os serviços tecnológicos"
        )
        
        # Campo para quantidade de ACE
        qtd_ace = st.number_input(
            "Quantidade de ACE:", 
            min_value=0, 
            step=1, 
            key="p2_qtd_ace",
            help="Número de Agentes de Combate às Endemias que utilizarão o aplicativo"
        )
        
        # Explicação sobre ACE
        if qtd_ace > 0:
            st.info(f"💡 O valor do App ACE será calculado considerando {qtd_ace} agentes")
        
        # Sugerir valores com base na faixa populacional
        if st.button("📊 Sugerir Valores de Serviços", help="Preenche com valores sugeridos para esta faixa populacional"):
            if faixa in VALORES_POR_FAIXA:
                valores_sugeridos = VALORES_POR_FAIXA[faixa]
                # Ajustar valores com base no número de unidades
                fator_ajuste = max(1.0, qtd_unidades_p2 / 5)
                
                st.session_state.p2_pec_val = valores_sugeridos.get("p2_pec", 20000.0) * fator_ajuste
                
                # Calcular valor do aplicativo ACE baseado na quantidade de agentes
                # Base de R$ 50,00 por agente + valor base do município
                valor_base_app = valores_sugeridos.get("p2_app", 2000.0)
                if qtd_ace > 0:
                    st.session_state.p2_app_val = valor_base_app + (qtd_ace * 50.0)
                else:
                    st.session_state.p2_app_val = valor_base_app
                
                # Definir outros valores com valores padrão
                st.session_state.p2_regulacao_val = valores_sugeridos.get("p2_regulacao", 5000.0) * fator_ajuste
                st.session_state.p2_esus_val = valores_sugeridos.get("p2_esus", 3500.0) * fator_ajuste
                st.session_state.p2_hosp_val = valores_sugeridos.get("p2_hosp", 8000.0) * fator_ajuste
                
                st.success(f"Valores tecnológicos sugeridos aplicados!")

        # Opções adicionais
        st.write("### Opções Adicionais")
        
        if 'has_hospital' not in st.session_state: st.session_state.has_hospital = False
        has_hospital = st.checkbox("Município possui hospital?", key="has_hospital")
        
        if has_hospital and st.session_state.p2_hosp_val == 0:
            st.session_state.p2_hosp_val = 8000.0 * max(1.0, qtd_unidades_p2 / 5)

    with col2:
        st.subheader("Valores dos Serviços Tecnológicos")
        
        # Inputs para valores
        if 'p2_pec_val' not in st.session_state: st.session_state.p2_pec_val = 0.0
        if 'p2_app_val' not in st.session_state: st.session_state.p2_app_val = 0.0
        if 'p2_comodato_val' not in st.session_state: st.session_state.p2_comodato_val = 0.0
        if 'p2_regulacao_val' not in st.session_state: st.session_state.p2_regulacao_val = 0.0
        if 'p2_esus_val' not in st.session_state: st.session_state.p2_esus_val = 0.0
        if 'p2_hosp_val' not in st.session_state: st.session_state.p2_hosp_val = 0.0

        col_a, col_b = st.columns(2)
        
        with col_a:
            val_pec = st.number_input(
                "PEC Servidor com BI Inteligente:",
                min_value=0.0,
                format="%.2f",
                key="p2_pec_val",
                help="Prontuário Eletrônico do Cidadão com análises avançadas"
            )
            
            # Atualizar descrição para incluir informação sobre agentes
            app_description = "Aplicativo para Agentes Comunitários de Endemias"
            if qtd_ace > 0:
                app_description += f" ({qtd_ace} agentes)"
                
            val_app = st.number_input(
                "Aplicativo Visita ACE:",
                min_value=0.0,
                format="%.2f",
                key="p2_app_val",
                help=app_description
            )
            
            # Novo campo para Comodato
            val_comodato = st.number_input(
                "COMODATO APARELHO SMARTPHONE OU TABLET:",
                min_value=0.0,
                format="%.2f",
                key="p2_comodato_val",
                help="Valor para comodato de aparelhos para uso dos aplicativos"
            )
            
            val_regulacao = st.number_input(
                "Sistema de Regulação:",
                min_value=0.0,
                format="%.2f",
                key="p2_regulacao_val",
                help="Sistema para gerenciamento de filas e regulação de serviços"
            )
            
        with col_b:
            val_esus = st.number_input(
                "eSUS Farma:",
                min_value=0.0,
                format="%.2f",
                key="p2_esus_val",
                help="Sistema de gestão farmacêutica integrado ao eSUS"
            )
            
            val_hosp = st.number_input(
                "Sistema Hospitalar:",
                min_value=0.0,
                format="%.2f",
                key="p2_hosp_val",
                help="Solução completa para gestão hospitalar"
            )

    # Cálculo Total - atualizando para incluir o valor de comodato
    total_p2 = val_pec + val_app + val_comodato + val_regulacao + val_esus + val_hosp
    
    # Exibição dos resultados em cards visuais
    st.markdown("### Resumo dos Serviços Tecnológicos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("PEC Servidor", val_pec)
        metric_card("Sistema de Regulação", val_regulacao)
    
    with col2:
        # Adicionar informação da quantidade de ACE no card se aplicável
        app_title = "Aplicativo ACE"
        if qtd_ace > 0:
            app_title += f" ({qtd_ace} agentes)"
        metric_card(app_title, val_app)
        metric_card("Comodato Aparelhos", val_comodato)
    
    with col3:
        metric_card("eSUS Farma", val_esus)
        metric_card("Sistema Hospitalar", val_hosp)
    
    # Card do total
    st.markdown(f"""
    <div class="total-card">
        <h3>TOTAL MENSAL P2 - SERVIÇOS TECNOLÓGICOS</h3>
        <h2>{formatar_valor_reais(total_p2)}</h2>
        <p>Valor estimado anual: {formatar_valor_reais(total_p2 * 12)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de distribuição
    if total_p2 > 0:
        # Modificar o título do App ACE para incluir informação sobre quantidade de agentes
        app_label = 'App Visita ACE'
        if qtd_ace > 0:
            app_label += f' ({qtd_ace} agentes)'
            
        dados = pd.DataFrame({
            'Serviço': ['PEC Servidor', app_label, 'Comodato Aparelhos', 'Sistema de Regulação', 'eSUS Farma', 'Sistema Hospitalar'],
            'Valor': [val_pec, val_app, val_comodato, val_regulacao, val_esus, val_hosp]
        })
        
        fig = px.bar(
            dados, 
            x='Serviço', 
            y='Valor', 
            title='Comparativo de Serviços Tecnológicos',
            color='Valor',
            color_continuous_scale='Teal'
        )
        fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Salvar o total na session_state para exibição consolidada
    st.session_state.total_p2 = total_p2