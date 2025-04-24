import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import formatar_valor_reais

def display_accounting_costs():
    st.header("Custos Reais - AUREA")
    st.caption("Análise detalhada dos custos operacionais e simulação de contrato")
    
    # Inicialização dos dados no session_state se não existirem
    if 'custos_data_initialized' not in st.session_state:
        # Dados dos custos
        st.session_state.custos_items = list(range(1, 31))
        st.session_state.custos_descricao = [
            # FORMAÇÃO
            "Educa+",
            "Verena (Online p/ pais)",
            "Carol",
            "Mamary",
            "Verônica - Atleta",
            "Luisa Hage",
            "Wilson e Marconi (Ed. Fisica)",
            "Cachê aulas da Plataforma (40 AULAS 10 PROFS)",
            # PRODUÇÃO ARENA
            "Frete e ajudantes para carregar e descarregar o caminhão",
            "Reformas, comunicação visual,  pintura, materiais, etc",
            "Cachê, Alimentação, Hospedagem, combustível equipe técnica",
            "Hospedagem, alimentação e transporte palestrantes",
            "Cachê Monitores incluindo atendimento EJA, Uniformes",
            # PESSOAL
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
            # INSUMOS
            "Aluguel escritório",
            "Luz escritório",
            "Internet escritório",
            "Telefone - Áurea",
            "Aluguel de Galpão",
            "Aluguel de Veiculo"
        ]
        st.session_state.custos_valores = [
            # FORMAÇÃO
            40000.00, 4500.00, 4500.00, 5500.00, 5500.00, 2000.00, 10000.00, 5000.00,
            # PRODUÇÃO ARENA
            15000.00, 4000.00, 16000.00, 6000.00, 7000.00,
            # PESSOAL
            1000.00, 1500.00, 1000.00, 7000.00, 9000.00, 0.00, 7000.00, 10000.00, 850.00, 640.00, 3500.00,
            # INSUMOS
            1700.00, 500.00, 280.00, 57.00, 1700.00, 5000.00
        ]
        st.session_state.custos_classificacao = [
            # FORMAÇÃO
            "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", 
            "POR CONTRATO", "POR CONTRATO", "SAZONAL",
            # PRODUÇÃO ARENA
            "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "POR CONTRATO",
            # PESSOAL
            "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "POR CONTRATO", "POR CONTRATO",
            "POR CONTRATO", "POR CONTRATO", "POR CONTRATO", "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL",
            # INSUMOS
            "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "FIXO MENSAL", "SAZONAL"
        ]
        st.session_state.custos_categoria = [
            # FORMAÇÃO
            "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO", "FORMAÇÃO",
            # PRODUÇÃO ARENA
            "PRODUÇÃO ARENA", "PRODUÇÃO ARENA", "PRODUÇÃO ARENA", "PRODUÇÃO ARENA", "PRODUÇÃO ARENA",
            # PESSOAL
            "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL", 
            "PESSOAL", "PESSOAL", "PESSOAL", "PESSOAL",
            # INSUMOS
            "INSUMOS", "INSUMOS", "INSUMOS", "INSUMOS", "INSUMOS", "INSUMOS"
        ]
        
        # Dados da simulação de contrato
        st.session_state.simulacao_descricao = [
            "CONTRATO BRUTO", "IMPOSTO (17%)", "CONTRATO LIQUIDO 01",
            "TT (60%)", "CONTRATO LIQUIDO 02", "CUSTO FIXO",
            "RESULTADO FINAL CONTRATO", "PERCENTUAL LUCRATIVIDADE"
        ]
        st.session_state.simulacao_valores = [
            530000.00, 90100.00, 439900.00, 
            263940.00, 175960.00, 175727.00,
            233.00, 0.13
        ]
        st.session_state.simulacao_observacao = [
            "", "", "",
            "FERNANDO", "R$ 14.076,80", "RESULTADO",
            "-R$ 13.843,80", ""
        ]
        
        # Despesas por classificação
        st.session_state.despesas_classificacao = ["FIXO MENSAL", "POR CONTRATO", "SAZONAL"]
        st.session_state.despesas_valores = [12727.00, 153000.00, 10000.00]
        
        st.session_state.custos_data_initialized = True
    
    # Construir os dataframes a partir dos dados do session_state
    custos_data = {
        "ITEM": st.session_state.custos_items,
        "DESCRIÇÃO": st.session_state.custos_descricao,
        "VALOR": st.session_state.custos_valores,
        "CLASSIFICAÇÃO": st.session_state.custos_classificacao,
        "CATEGORIA": st.session_state.custos_categoria
    }
    
    df_custos = pd.DataFrame(custos_data)
    
    simulacao_data = {
        "DESCRIÇÃO": st.session_state.simulacao_descricao,
        "VALOR": st.session_state.simulacao_valores,
        "OBSERVAÇÃO": st.session_state.simulacao_observacao
    }
    
    df_simulacao = pd.DataFrame(simulacao_data)
    
    despesas_class_data = {
        "CLASSIFICAÇÃO": st.session_state.despesas_classificacao,
        "VALOR": st.session_state.despesas_valores
    }
    
    df_despesas_class = pd.DataFrame(despesas_class_data)

    # Visualização dos dados de custos
    st.subheader("Detalhamento de Custos")
    
    # Botão para editar valores
    edit_custos = st.checkbox("Editar Valores de Custos", key="edit_custos_values")
    
    if edit_custos:
        st.info("Edite os valores dos custos abaixo. As alterações serão aplicadas automaticamente.")
        
        # Selecionar categoria para editar
        categoria_edit = st.selectbox(
            "Selecione a categoria para editar:", 
            options=sorted(set(st.session_state.custos_categoria)),
            key="categoria_edit"
        )
        
        # Filtrar itens pela categoria selecionada
        indices_categoria = [i for i, cat in enumerate(st.session_state.custos_categoria) if cat == categoria_edit]
        
        # Criar colunas para edição mais organizada
        col1, col2 = st.columns(2)
        
        with col1:
            for i in indices_categoria[:len(indices_categoria)//2 + len(indices_categoria)%2]:
                st.session_state.custos_valores[i] = st.number_input(
                    f"{st.session_state.custos_descricao[i]} ({st.session_state.custos_classificacao[i]})",
                    min_value=0.0,
                    value=float(st.session_state.custos_valores[i]),
                    format="%.2f",
                    key=f"custo_valor_{i}"
                )
        
        with col2:
            for i in indices_categoria[len(indices_categoria)//2 + len(indices_categoria)%2:]:
                st.session_state.custos_valores[i] = st.number_input(
                    f"{st.session_state.custos_descricao[i]} ({st.session_state.custos_classificacao[i]})",
                    min_value=0.0,
                    value=float(st.session_state.custos_valores[i]),
                    format="%.2f",
                    key=f"custo_valor_{i}"
                )
        
        # Botão para adicionar novo item
        with st.expander("Adicionar novo item"):
            new_descricao = st.text_input("Descrição:", key="new_item_desc")
            new_valor = st.number_input("Valor:", min_value=0.0, format="%.2f", key="new_item_val")
            new_classificacao = st.selectbox(
                "Classificação:", 
                options=["FIXO MENSAL", "POR CONTRATO", "SAZONAL"],
                key="new_item_class"
            )
            new_categoria = st.selectbox(
                "Categoria:", 
                options=["FORMAÇÃO", "PRODUÇÃO ARENA", "PESSOAL", "INSUMOS"],
                key="new_item_cat"
            )
            
            if st.button("Adicionar Item", key="add_new_item"):
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
    
    # Reconstruir o dataframe com os valores atualizados
    custos_data = {
        "ITEM": st.session_state.custos_items,
        "DESCRIÇÃO": st.session_state.custos_descricao,
        "VALOR": st.session_state.custos_valores,
        "CLASSIFICAÇÃO": st.session_state.custos_classificacao,
        "CATEGORIA": st.session_state.custos_categoria
    }
    
    df_custos = pd.DataFrame(custos_data)
    
    # Filtros para visualização
    categoria_filter = st.multiselect("Filtrar por Categoria:", 
                                     options=sorted(df_custos["CATEGORIA"].unique()),
                                     default=list(df_custos["CATEGORIA"].unique()))
    
    classificacao_filter = st.multiselect("Filtrar por Classificação:",
                                        options=sorted(df_custos["CLASSIFICAÇÃO"].unique()),
                                        default=list(df_custos["CLASSIFICAÇÃO"].unique()))
    
    # Aplicar filtros
    df_filtered = df_custos[
        (df_custos["CATEGORIA"].isin(categoria_filter)) &
        (df_custos["CLASSIFICAÇÃO"].isin(classificacao_filter))
    ]
    
    # Exibir tabela de custos formatada
    st.dataframe(
        df_filtered,
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
    
    # Totais
    total_custos = df_filtered["VALOR"].sum()
    st.markdown(f"**TOTAL: {formatar_valor_reais(total_custos)}**")
    
    # Visualizações gráficas
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de custos por categoria
        fig_categoria = px.pie(
            df_filtered, 
            values="VALOR", 
            names="CATEGORIA",
            title="Distribuição de Custos por Categoria",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_categoria, use_container_width=True)
    
    with col2:
        # Gráfico de custos por classificação
        fig_class = px.pie(
            df_filtered,
            values="VALOR",
            names="CLASSIFICAÇÃO",
            title="Distribuição por Classificação",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_class, use_container_width=True)
    
    # Gráfico de barras por item
    st.subheader("Detalhamento por Item")
    top_n = st.slider("Mostrar top itens:", min_value=5, max_value=30, value=10)
    
    # Ordenar e pegar os top N itens por valor
    top_items = df_filtered.sort_values("VALOR", ascending=False).head(top_n)
    
    fig_items = px.bar(
        top_items,
        x="DESCRIÇÃO",
        y="VALOR",
        color="CATEGORIA",
        title=f"Top {top_n} Itens por Valor",
        text_auto='.2s',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_items.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_items, use_container_width=True)
    
    # Simulação de Contrato
    st.header("Simulação de Contrato Mínimo")
    
    # Opção para editar simulação
    edit_simulacao = st.checkbox("Editar Valores da Simulação", key="edit_simulacao_values")
    
    if edit_simulacao:
        st.info("Edite os valores da simulação de contrato. Alguns valores são calculados automaticamente.")
        
        # Campos editáveis
        st.session_state.simulacao_valores[0] = st.number_input(
            "CONTRATO BRUTO",
            min_value=0.0,
            value=st.session_state.simulacao_valores[0],
            format="%.2f",
            key="sim_contrato_bruto"
        )
        
        # Imposto (%) - permitir editar a porcentagem
        imposto_percent = (st.session_state.simulacao_valores[1] / st.session_state.simulacao_valores[0]) * 100 if st.session_state.simulacao_valores[0] > 0 else 17.0
        
        new_imposto_percent = st.number_input(
            "IMPOSTO (%)",
            min_value=0.0,
            max_value=100.0,
            value=imposto_percent,
            format="%.2f",
            key="sim_imposto_percent"
        )
        
        # Recalcular o valor do imposto
        st.session_state.simulacao_valores[1] = st.session_state.simulacao_valores[0] * (new_imposto_percent / 100)
        
        # Contrato líquido 01 (calculado)
        st.session_state.simulacao_valores[2] = st.session_state.simulacao_valores[0] - st.session_state.simulacao_valores[1]
        st.text(f"CONTRATO LIQUIDO 01: {formatar_valor_reais(st.session_state.simulacao_valores[2])}")
        
        # TT (%) - permitir editar a porcentagem
        tt_percent = (st.session_state.simulacao_valores[3] / st.session_state.simulacao_valores[2]) * 100 if st.session_state.simulacao_valores[2] > 0 else 60.0
        
        new_tt_percent = st.number_input(
            "TT (%)",
            min_value=0.0,
            max_value=100.0,
            value=tt_percent,
            format="%.2f",
            key="sim_tt_percent"
        )
        
        # Recalcular o valor do TT
        st.session_state.simulacao_valores[3] = st.session_state.simulacao_valores[2] * (new_tt_percent / 100)
        
        # Editar observação do TT
        st.session_state.simulacao_observacao[3] = st.text_input(
            "Observação para TT",
            value=st.session_state.simulacao_observacao[3],
            key="obs_tt"
        )
        
        # Contrato líquido 02 (calculado)
        st.session_state.simulacao_valores[4] = st.session_state.simulacao_valores[2] - st.session_state.simulacao_valores[3]
        st.text(f"CONTRATO LIQUIDO 02: {formatar_valor_reais(st.session_state.simulacao_valores[4])}")
        
        # Editar observação do CONTRATO LÍQUIDO 02
        st.session_state.simulacao_observacao[4] = st.text_input(
            "Observação para CONTRATO LIQUIDO 02",
            value=st.session_state.simulacao_observacao[4],
            key="obs_cliq02"
        )
        
        # CUSTO FIXO
        st.session_state.simulacao_valores[5] = st.number_input(
            "CUSTO FIXO",
            min_value=0.0,
            value=st.session_state.simulacao_valores[5],
            format="%.2f",
            key="sim_custo_fixo"
        )
        
        # Editar observação do CUSTO FIXO
        st.session_state.simulacao_observacao[5] = st.text_input(
            "Observação para CUSTO FIXO",
            value=st.session_state.simulacao_observacao[5],
            key="obs_custo_fixo"
        )
        
        # RESULTADO FINAL (calculado)
        st.session_state.simulacao_valores[6] = st.session_state.simulacao_valores[4] - st.session_state.simulacao_valores[5]
        st.text(f"RESULTADO FINAL CONTRATO: {formatar_valor_reais(st.session_state.simulacao_valores[6])}")
        
        # Editar observação do RESULTADO FINAL
        st.session_state.simulacao_observacao[6] = st.text_input(
            "Observação para RESULTADO FINAL",
            value=st.session_state.simulacao_observacao[6],
            key="obs_resultado"
        )
        
        # PERCENTUAL LUCRATIVIDADE (calculado)
        if st.session_state.simulacao_valores[0] > 0:
            st.session_state.simulacao_valores[7] = st.session_state.simulacao_valores[6] / st.session_state.simulacao_valores[0]
        st.text(f"PERCENTUAL LUCRATIVIDADE: {st.session_state.simulacao_valores[7] * 100:.2f}%")
    
    # Reconstruir o dataframe de simulação
    simulacao_data = {
        "DESCRIÇÃO": st.session_state.simulacao_descricao,
        "VALOR": st.session_state.simulacao_valores,
        "OBSERVAÇÃO": st.session_state.simulacao_observacao
    }
    
    df_simulacao = pd.DataFrame(simulacao_data)
    
    # Converter o formato do percentual de lucratividade para percentual
    df_simulacao.loc[df_simulacao["DESCRIÇÃO"] == "PERCENTUAL LUCRATIVIDADE", "VALOR"] = \
        df_simulacao.loc[df_simulacao["DESCRIÇÃO"] == "PERCENTUAL LUCRATIVIDADE", "VALOR"] * 100
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Criar colunas temporárias formatadas para evitar o uso de função lambda
        df_simulacao_display = df_simulacao.copy()
        
        # Formatar os valores monetários
        for i, row in df_simulacao_display.iterrows():
            if row["DESCRIÇÃO"] != "PERCENTUAL LUCRATIVIDADE":
                df_simulacao_display.at[i, "VALOR_FORMATADO"] = f"R$ {row['VALOR']:,.2f}"
            else:
                df_simulacao_display.at[i, "VALOR_FORMATADO"] = f"{row['VALOR']:.2f}%"
        
        # Tabela de simulação usando as colunas pré-formatadas
        st.dataframe(
            df_simulacao_display[["DESCRIÇÃO", "VALOR_FORMATADO", "OBSERVAÇÃO"]],
            column_config={
                "DESCRIÇÃO": st.column_config.TextColumn("DESCRIÇÃO"),
                "VALOR_FORMATADO": st.column_config.TextColumn("VALOR"),
                "OBSERVAÇÃO": st.column_config.TextColumn("OBSERVAÇÃO")
            },
            hide_index=True,
            use_container_width=True
        )
    
    with col2:
        # Gráfico de waterfall da simulação
        simulacao_waterfall = df_simulacao.iloc[0:7].copy()  # Excluindo a linha de percentual
        
        # Definir os valores incrementais para o waterfall
        valores = simulacao_waterfall["VALOR"].tolist()
        incrementos = [
            valores[0],  # CONTRATO BRUTO (valor inicial)
            -valores[1],  # IMPOSTO (negativo - subtração)
            0,  # CONTRATO LIQUIDO 01 (calculado automaticamente)
            -valores[3],  # TT (negativo - subtração)
            0,  # CONTRATO LIQUIDO 02 (calculado automaticamente)
            -valores[5],  # CUSTO FIXO (negativo - subtração)
            0,  # RESULTADO FINAL (calculado automaticamente)
        ]
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="Simulação de Contrato", 
            orientation="v",
            measure=["absolute", "relative", "total", "relative", "total", "relative", "total"],
            x=simulacao_waterfall["DESCRIÇÃO"],
            y=incrementos,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "Crimson"}},
            increasing={"marker": {"color": "Teal"}},
            totals={"marker": {"color": "RoyalBlue"}}
        ))
        
        fig_waterfall.update_layout(
            title="Fluxo de Valor do Contrato",
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_waterfall, use_container_width=True)
    
    # Total de despesa por classificação
    st.subheader("Total de Despesa por Classificação")
    
    # Opção para editar despesas por classificação
    edit_despesas = st.checkbox("Editar Despesas por Classificação", key="edit_despesas_values")
    
    if edit_despesas:
        st.info("Edite os valores das despesas por classificação.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state.despesas_valores[0] = st.number_input(
                "FIXO MENSAL",
                min_value=0.0,
                value=st.session_state.despesas_valores[0],
                format="%.2f",
                key="desp_fixo"
            )
        
        with col2:
            st.session_state.despesas_valores[1] = st.number_input(
                "POR CONTRATO",
                min_value=0.0,
                value=st.session_state.despesas_valores[1],
                format="%.2f",
                key="desp_contrato"
            )
        
        with col3:
            st.session_state.despesas_valores[2] = st.number_input(
                "SAZONAL",
                min_value=0.0,
                value=st.session_state.despesas_valores[2],
                format="%.2f",
                key="desp_sazonal"
            )
    
    # Reconstruir o dataframe de despesas
    despesas_class_data = {
        "CLASSIFICAÇÃO": st.session_state.despesas_classificacao,
        "VALOR": st.session_state.despesas_valores
    }
    
    df_despesas_class = pd.DataFrame(despesas_class_data)
    
    fig_despesa_class = px.bar(
        df_despesas_class,
        x="CLASSIFICAÇÃO",
        y="VALOR",
        color="CLASSIFICAÇÃO",
        text_auto='.2s',
        title="Despesas por Classificação",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    st.plotly_chart(fig_despesa_class, use_container_width=True)
    
    # Análise de Lucratividade
    st.subheader("Análise de Lucratividade")
    
    # Cálculos de lucratividade
    contrato_bruto = df_simulacao.loc[df_simulacao["DESCRIÇÃO"] == "CONTRATO BRUTO", "VALOR"].values[0]
    resultado_final = df_simulacao.loc[df_simulacao["DESCRIÇÃO"] == "RESULTADO FINAL CONTRATO", "VALOR"].values[0]
    percentual_lucro = (resultado_final / contrato_bruto) * 100
    
    # Criar colunas para as métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Contrato Bruto",
            value=f"R$ {contrato_bruto:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    
    with col2:
        st.metric(
            label="Resultado Final",
            value=f"R$ {resultado_final:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            delta=f"{percentual_lucro:.2f}%"
        )
    
    with col3:
        st.metric(
            label="Custo Total",
            value=f"R$ {total_custos:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            delta=f"{(total_custos/contrato_bruto)*100:.2f}% do Contrato"
        )
    
    # Conclusões e recomendações - também pode ser editável
    if 'conclusao_analise' not in st.session_state:
        st.session_state.conclusao_analise = """
        **Análise Geral:**
        
        O contrato apresenta uma margem de lucratividade extremamente baixa (0,13%), 
        com um resultado final de apenas R$ 233,00 em um contrato bruto de R$ 530.000,00.
        
        **Recomendações:**
        1. Revisar os custos "POR CONTRATO" que representam o maior percentual das despesas
        2. Analisar a possibilidade de renegociação do percentual de TT (60%)
        3. Buscar eficiências operacionais nos custos fixos mensais
        """
    
    # Botão para editar a conclusão
    edit_conclusao = st.checkbox("Editar Conclusão e Recomendações", key="edit_conclusao")
    
    if edit_conclusao:
        st.session_state.conclusao_analise = st.text_area(
            "Editar Conclusão e Recomendações:",
            value=st.session_state.conclusao_analise,
            height=200,
            key="text_conclusao"
        )
    
    # Exibir a conclusão
    st.info(st.session_state.conclusao_analise)