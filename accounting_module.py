import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import formatar_valor_reais
import json
from datetime import datetime
import csv
import io

def initialize_session_state():
    if 'categorias' not in st.session_state:
        st.session_state.categorias = {
            "FORMAÇÃO": {"descricao": "Custos relacionados à formação e treinamento", "cor": "#2ecc71"},
            "PRODUÇÃO ARENA": {"descricao": "Custos de produção e arena", "cor": "#e74c3c"},
            "PESSOAL": {"descricao": "Custos com pessoal e recursos humanos", "cor": "#3498db"},
            "INSUMOS": {"descricao": "Custos com insumos e materiais", "cor": "#f1c40f"}
        }
    
    if 'custos_data_initialized' not in st.session_state:
        st.session_state.custos_items = list(range(1, 31))
        st.session_state.custos_descricao = [
            "Educa+",
            "Verena (Online p/ pais)",
            "Carol",
            "Mamary",
            "Verônica - Atleta",
            "Luisa Hage",
            "Wilson e Marconi (Ed. Fisica)",
            "Cachê aulas da Plataforma (40 AULAS 10 PROFS)",
            "Frete e ajudantes para carregar e descarregar o caminhão",
            "Reformas, comunicação visual,  pintura, materiais, etc",
            "Cachê, Alimentação, Hospedagem, combustível equipe técnica",
            "Hospedagem, alimentação e transporte palestrantes",
            "Cachê Monitores incluindo atendimento EJA, Uniformes",
            "Lucas - Social Media/ Relatórios/ Faturamento",
            "Sidnei - Design Gráfico",
            "Iza - Financeiro",
            "Gilson - GEROP",
            "Rodrigo - Diretoria",
            "Fernando - Arena",
            "Malheiros - Juridico",
            "Tiago - filmaker",
            "Amanda - Contabilidade",
            "Diarista - Limpeza Escritório (4x mês)",
            "Rafael - Aurea Conecta",
            "Aluguel escritório",
            "Luz escritório",
            "Internet escritório",
            "Telefone - Áurea",
            "Aluguel de Galpão",
            "Aluguel de Veiculo"
        ]
        st.session_state.custos_valores = [
            40000.00, 4500.00, 4500.00, 5500.00, 5500.00, 2000.00, 10000.00, 5000.00,
            15000.00, 4000.00, 16000.00, 6000.00, 7000.00,
            1000.00, 1500.00, 1000.00, 7000.00, 9000.00, 0.00, 7000.00, 10000.00, 850.00, 640.00, 3500.00,
            1700.00, 500.00, 280.00, 57.00, 1700.00, 5000.00
        ]
        st.session_state.custos_classificacao = [
            "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", 
            "POR CONTRATO", "POR CONTRATO", "SAZONAL",
            "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO",
            "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "POR CONTRATO", "POR CONTRATO",
            "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL",
            "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "SAZONAL"
        ]
        st.session_state.custos_categoria = [
            "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO",
            "PRODUÇÃO ARENA", "PRODUÇÃO ARENA", "PRODUÇÃO ARENA", "PRODUÇÃO ARENA", "PRODUÇÃO ARENA",
            "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", 
            "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL",
            "INSUMOS", "INSUMOS", "INSUMOS", "INSUMOS", "INSUMOS", "INSUMOS"
        ]
        st.session_state.custos_data_initialized = True

def display_dashboard():
    st.subheader("Dashboard de Custos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_custos = sum(st.session_state.custos_valores)
        st.metric("Total de Custos", formatar_valor_reais(total_custos))
    
    with col2:
        custos_fixos = sum([valor for i, valor in enumerate(st.session_state.custos_valores) 
                           if st.session_state.custos_classificacao[i] == "FIXO MENSAL"])
        st.metric("Custos Fixos", formatar_valor_reais(custos_fixos))
    
    with col3:
        custos_variaveis = total_custos - custos_fixos
        st.metric("Custos Variáveis", formatar_valor_reais(custos_variaveis))
    
    col1, col2 = st.columns(2)
    
    with col1:
        df_categoria = pd.DataFrame({
            "Categoria": st.session_state.custos_categoria,
            "Valor": st.session_state.custos_valores
        })
        fig_categoria = px.pie(
            df_categoria.groupby("Categoria").sum().reset_index(),
            values="Valor",
            names="Categoria",
            title="Distribuição por Categoria",
            color="Categoria",
            color_discrete_map={cat: info["cor"] for cat, info in st.session_state.categorias.items()}
        )
        st.plotly_chart(fig_categoria, use_container_width=True)
    
    with col2:
        df_classificacao = pd.DataFrame({
            "Classificação": st.session_state.custos_classificacao,
            "Valor": st.session_state.custos_valores
        })
        cores_classificacao = {
            "FIXO MENSAL": "#27ae60",
            "POR CONTRATO": "#f39c12",
            "SAZONAL": "#c0392b"
        }
        fig_classificacao = px.pie(
            df_classificacao.groupby("Classificação").sum().reset_index(),
            values="Valor",
            names="Classificação",
            title="Distribuição por Classificação",
            color="Classificação",
            color_discrete_map=cores_classificacao
        )
        st.plotly_chart(fig_classificacao, use_container_width=True)

def manage_categories():
    st.subheader("Gerenciamento de Categorias")
    
    with st.expander("Adicionar Nova Categoria", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_cat_nome = st.text_input("Nome da Categoria", key="new_cat_nome")
            new_cat_desc = st.text_input("Descrição", key="new_cat_desc")
        with col2:
            new_cat_cor = st.color_picker("Cor", key="new_cat_cor")
        
        if st.button("Adicionar Categoria"):
            if new_cat_nome and new_cat_nome not in st.session_state.categorias:
                st.session_state.categorias[new_cat_nome] = {
                    "descricao": new_cat_desc,
                    "cor": new_cat_cor
                }
                st.success(f"Categoria '{new_cat_nome}' adicionada com sucesso!")
                st.rerun()
            elif not new_cat_nome:
                st.error("Por favor, insira um nome para a categoria.")
            else:
                st.error("Esta categoria já existe.")
    
    st.subheader("Categorias Existentes")
    
    for cat_nome, cat_info in st.session_state.categorias.items():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{cat_nome}**")
                st.caption(cat_info["descricao"])
            
            with col2:
                novo_cor = st.color_picker("Cor", cat_info["cor"], key=f"cor_{cat_nome}")
                if novo_cor != cat_info["cor"]:
                    st.session_state.categorias[cat_nome]["cor"] = novo_cor
            
            with col3:
                if st.button("🗑️", key=f"del_{cat_nome}"):
                    if cat_nome in [cat for cat in st.session_state.custos_categoria]:
                        st.error("Não é possível excluir uma categoria em uso.")
                    else:
                        del st.session_state.categorias[cat_nome]
                        st.success(f"Categoria '{cat_nome}' excluída com sucesso!")
                        st.rerun()
            
            st.divider()

def display_items():
    st.subheader("Cadastro e Edição de Itens")
    
    with st.expander("Adicionar Novo Item", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            new_descricao = st.text_input("Descrição do Item")
            new_valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
        
        with col2:
            new_categoria = st.selectbox("Categoria", 
                                       options=sorted(st.session_state.categorias.keys()))
            new_classificacao = st.selectbox("Classificação",
                                           options=["FIXO MENSAL", "POR CONTRATO", "SAZONAL"])
        
        if st.button("Adicionar Item"):
            if new_descricao:
                st.session_state.custos_items.append(len(st.session_state.custos_items) + 1)
                st.session_state.custos_descricao.append(new_descricao)
                st.session_state.custos_valores.append(new_valor)
                st.session_state.custos_classificacao.append(new_classificacao)
                st.session_state.custos_categoria.append(new_categoria)
                st.success(f"Item '{new_descricao}' adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, preencha a descrição do item.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Buscar por descrição", "")
    
    with col2:
        filter_categoria = st.multiselect(
            "Filtrar por Categoria",
            options=sorted(set(st.session_state.custos_categoria)),
            default=[]
        )
    
    with col3:
        filter_classificacao = st.multiselect(
            "Filtrar por Classificação",
            options=sorted(set(st.session_state.custos_classificacao)),
            default=[]
        )
    
    df = pd.DataFrame({
        "ITEM": st.session_state.custos_items,
        "DESCRIÇÃO": st.session_state.custos_descricao,
        "VALOR": st.session_state.custos_valores,
        "CLASSIFICAÇÃO": st.session_state.custos_classificacao,
        "CATEGORIA": st.session_state.custos_categoria
    })
    
    if search_term:
        df = df[df["DESCRIÇÃO"].str.contains(search_term, case=False)]
    if filter_categoria:
        df = df[df["CATEGORIA"].isin(filter_categoria)]
    if filter_classificacao:
        df = df[df["CLASSIFICAÇÃO"].isin(filter_classificacao)]
    
    st.write("### Itens Cadastrados")
    
    view_type = st.radio("Tipo de Visualização", ["Cards", "Tabela"], horizontal=True)
    
    if view_type == "Cards":
        for _, item in df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"**{item['DESCRIÇÃO']}**")
                    st.caption(f"Categoria: {item['CATEGORIA']}")
                
                with col2:
                    st.markdown(f"**{formatar_valor_reais(item['VALOR'])}**")
                    st.caption(f"Classificação: {item['CLASSIFICAÇÃO']}")
                
                with col3:
                    if st.button("🗑️", key=f"del_item_{item['ITEM']}"):
                        idx = st.session_state.custos_items.index(item['ITEM'])
                        del st.session_state.custos_items[idx]
                        del st.session_state.custos_descricao[idx]
                        del st.session_state.custos_valores[idx]
                        del st.session_state.custos_classificacao[idx]
                        del st.session_state.custos_categoria[idx]
                        st.success("Item excluído com sucesso!")
                        st.rerun()
                
                st.divider()
    else:
        st.dataframe(
            df.style.apply(highlight_classificacao, axis=None),
            column_config={
                "ITEM": st.column_config.NumberColumn("ITEM", format="%d"),
                "DESCRIÇÃO": st.column_config.TextColumn("DESCRIÇÃO"),
                "VALOR": st.column_config.NumberColumn("VALOR", format="R$ %.2f"),
                "CLASSIFICAÇÃO": st.column_config.TextColumn("CLASSIFICAÇÃO"),
                "CATEGORIA": st.column_config.TextColumn("CATEGORIA"),
            },
            hide_index=True,
            use_container_width=True
        )

def display_reports():
    st.subheader("Relatórios e Análises")
    
    st.write("### Análise Temporal")
    periodo = st.selectbox("Período de Análise", ["Mensal", "Trimestral", "Anual"])
    
    dados_temporais = pd.DataFrame({
        "Período": ["Jan", "Fev", "Mar", "Abr"],
        "Custos Totais": [sum(st.session_state.custos_valores)] * 4
    })
    
    fig_temporal = px.line(
        dados_temporais,
        x="Período",
        y="Custos Totais",
        title="Evolução dos Custos",
        markers=True
    )
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    st.write("### Análise por Categoria")
    categoria_analise = st.selectbox("Selecione a Categoria", 
                                   options=sorted(st.session_state.categorias.keys()))
    
    df_categoria = pd.DataFrame({
        "Descrição": [desc for i, desc in enumerate(st.session_state.custos_descricao)
                     if st.session_state.custos_categoria[i] == categoria_analise],
        "Valor": [valor for i, valor in enumerate(st.session_state.custos_valores)
                 if st.session_state.custos_categoria[i] == categoria_analise]
    })
    
    if not df_categoria.empty:
        fig_categoria = px.bar(
            df_categoria,
            x="Descrição",
            y="Valor",
            title=f"Custos da Categoria {categoria_analise}",
            color_discrete_sequence=[st.session_state.categorias[categoria_analise]["cor"]]
        )
        fig_categoria.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_categoria, use_container_width=True)
    else:
        st.info(f"Não há itens cadastrados na categoria {categoria_analise}")

def display_settings():
    st.subheader("Configurações")
    
    st.write("### Exportar Dados")
    export_format = st.radio("Formato de Exportação", ["CSV", "JSON"], horizontal=True)
    
    if st.button("Exportar Dados"):
        if export_format == "CSV":
            df = pd.DataFrame({
                "ITEM": st.session_state.custos_items,
                "DESCRIÇÃO": st.session_state.custos_descricao,
                "VALOR": st.session_state.custos_valores,
                "CLASSIFICAÇÃO": st.session_state.custos_classificacao,
                "CATEGORIA": st.session_state.custos_categoria
            })
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "custos.csv",
                "text/csv",
                key='download-csv'
            )
        else:
            data = {
                "categorias": st.session_state.categorias,
                "itens": {
                    "items": st.session_state.custos_items,
                    "descricao": st.session_state.custos_descricao,
                    "valores": st.session_state.custos_valores,
                    "classificacao": st.session_state.custos_classificacao,
                    "categoria": st.session_state.custos_categoria
                }
            }
            json_str = json.dumps(data, indent=2)
            st.download_button(
                "Download JSON",
                json_str,
                "custos.json",
                "application/json",
                key='download-json'
            )
    
    st.write("### Importar Dados")
    uploaded_file = st.file_uploader("Escolha um arquivo para importar", type=['csv', 'json'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                st.session_state.custos_items = df["ITEM"].tolist()
                st.session_state.custos_descricao = df["DESCRIÇÃO"].tolist()
                st.session_state.custos_valores = df["VALOR"].tolist()
                st.session_state.custos_classificacao = df["CLASSIFICAÇÃO"].tolist()
                st.session_state.custos_categoria = df["CATEGORIA"].tolist()
            else:
                data = json.load(uploaded_file)
                st.session_state.categorias = data["categorias"]
                st.session_state.custos_items = data["itens"]["items"]
                st.session_state.custos_descricao = data["itens"]["descricao"]
                st.session_state.custos_valores = data["itens"]["valores"]
                st.session_state.custos_classificacao = data["itens"]["classificacao"]
                st.session_state.custos_categoria = data["itens"]["categoria"]
            
            st.success("Dados importados com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao importar dados: {str(e)}")

def display_contract_simulation():
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
            key="acc_contrato_bruto_input"  # Chave alterada para ser única
        )
        
        st.session_state.imposto_percentual_contrato = st.number_input(
            "Imposto (%):", 
            min_value=0.0, 
            max_value=100.0,
            value=st.session_state.imposto_percentual_contrato,
            format="%.2f", 
            key="acc_imposto_percentual_input"  # Chave alterada para ser única
        )
        
        st.session_state.valor_socio = st.number_input(
            "Valor Sócio (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_socio,
            format="%.2f", 
            key="acc_valor_socio_input"  # Chave alterada para ser única
        )
    
    with col_sim2:
        st.session_state.valor_fixo_mensal = st.number_input(
            "Custo Fixo Mensal (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_fixo_mensal,
            format="%.2f", 
            key="acc_valor_fixo_mensal_input"  # Chave alterada para ser única
        )
        
        st.session_state.valor_sazonal = st.number_input(
            "Custo Sazonal (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_sazonal,
            format="%.2f", 
            key="acc_valor_sazonal_input"  # Chave alterada para ser única
        )
        
        st.session_state.valor_por_contrato = st.number_input(
            "Custo Por Contrato (R$):", 
            min_value=0.0, 
            value=st.session_state.valor_por_contrato,
            format="%.2f", 
            key="acc_valor_por_contrato_input"  # Chave alterada para ser única
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

def display_accounting_costs():
    initialize_session_state()
    
    st.header("Gestão de Custos")
    st.caption("Sistema de gestão e análise de custos operacionais")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard",
        "🏷️ Categorias",
        "📝 Itens",
        "📈 Relatórios",
        "⚙️ Configurações",
        "💰 Simulação de Contrato"
    ])
    
    with tab1:
        display_dashboard()
    
    with tab2:
        manage_categories()
    
    with tab3:
        display_items()
    
    with tab4:
        display_reports()
    
    with tab5:
        display_settings()
    
    with tab6:
        display_contract_simulation()

def highlight_classificacao(df):
    cores = {
        "FIXO MENSAL": "background-color: rgba(0, 128, 0, 0.2)",
        "POR CONTRATO": "background-color: rgba(255, 215, 0, 0.2)",
        "SAZONAL": "background-color: rgba(255, 99, 71, 0.2)"
    }
    
    estilo = pd.DataFrame('', index=df.index, columns=df.columns)
    
    for i, valor in enumerate(df['CLASSIFICAÇÃO']):
        estilo.iloc[i, :] = cores.get(valor, '')
    
    return estilo