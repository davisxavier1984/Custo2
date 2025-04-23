import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from PIL import Image
import os
import base64
import io
import plotly.graph_objects as go
import numpy as np
import json
import glob
from datetime import datetime as dt

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

# Configuração de cores e tema
CORES = {
    "primaria": "#0066CC",
    "secundaria": "#2E8B57",
    "texto": "#333333",
    "destaque": "#FF9900",
    "background": "#F8F9FA",
    "erro": "#DC3545"
}

# Adicionar CSS personalizado
def local_css():
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {CORES["background"]};
        }}
        h1, h2, h3 {{
            color: {CORES["primaria"]};
        }}
        .stButton>button {{
            background-color: {CORES["primaria"]};
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 15px;
        }}
        .stButton>button:hover {{
            background-color: {CORES["secundaria"]};
        }}
        .total-card {{
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            margin: 10px 0;
            border-left: 5px solid {CORES["destaque"]};
        }}
        .metric-container {{
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }}
        .highlight {{
            color: {CORES["destaque"]};
            font-weight: bold;
        }}
        .footer {{
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: white;
            padding: 10px;
            text-align: center;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        }}
        </style>
    """, unsafe_allow_html=True)

local_css()

# Carregar e exibir logo
@st.cache_data
def get_logo():
    try:
        return Image.open("logo.png")
    except:
        # Cria uma imagem de placeholder se a logo não existir
        img = Image.new('RGB', (200, 100), color=(0, 102, 204))
        return img

def add_bg_from_base64(base64_string):
    base64_message = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(base64_message, unsafe_allow_html=True)

# --- Dados e Configurações Globais ---

# Valores pré-configurados por faixa populacional
VALORES_POR_FAIXA = {
    "ATÉ 10 MIL HABITANTES": {
        "p1_consultoria": 7000.0,
        "p1_capacitacao": 1500.0,
        "p1_bi": 8000.0,
        "p2_pec": 20000.0,
        "p2_app": 2000.0,
        "p2_regulacao": 3000.0,
        "p2_esus": 2500.0,
        "p2_hosp": 5000.0,
        "p3_cnes": 2500.0,
        "p3_investsus": 1800.0,
        "p3_transferegov": 2000.0,
        "p3_sismob": 1500.0,
        "p3_fpo_bpa": 3000.0
    },
    "10 MIL ATÉ 30 MIL HABITANTES": {
        "p1_consultoria": 9000.0,
        "p1_capacitacao": 2000.0,
        "p1_bi": 12000.0,
        "p2_pec": 30000.0,
        "p2_app": 3500.0,
        "p2_regulacao": 4000.0,
        "p2_esus": 3500.0,
        "p2_hosp": 7000.0,
        "p3_cnes": 3000.0,
        "p3_investsus": 2500.0,
        "p3_transferegov": 2500.0,
        "p3_sismob": 2000.0,
        "p3_fpo_bpa": 3500.0
    },
    "30 A 50 MIL HABITANTES": {
        "p1_consultoria": 12000.0,
        "p1_capacitacao": 2800.0,
        "p1_bi": 16000.0,
        "p2_pec": 40000.0,
        "p2_app": 5000.0,
        "p2_regulacao": 5000.0,
        "p2_esus": 4500.0,
        "p2_hosp": 10000.0,
        "p3_cnes": 3500.0,
        "p3_investsus": 3000.0,
        "p3_transferegov": 3000.0,
        "p3_sismob": 2500.0,
        "p3_fpo_bpa": 4000.0
    },
    "60 A 100 MIL HABITANTES": {
        "p1_consultoria": 15000.0,
        "p1_capacitacao": 3500.0,
        "p1_bi": 20000.0,
        "p2_pec": 50000.0,
        "p2_app": 7500.0,
        "p2_regulacao": 7000.0,
        "p2_esus": 6000.0,
        "p2_hosp": 15000.0,
        "p3_cnes": 4000.0,
        "p3_investsus": 3500.0,
        "p3_transferegov": 3500.0,
        "p3_sismob": 3000.0,
        "p3_fpo_bpa": 5000.0
    },
    "100 A 150 MIL HABITANTES": {
        "p1_consultoria": 18000.0,
        "p1_capacitacao": 4000.0,
        "p1_bi": 25000.0,
        "p2_pec": 60000.0,
        "p2_app": 10000.0,
        "p2_regulacao": 9000.0,
        "p2_esus": 7500.0,
        "p2_hosp": 20000.0,
        "p3_cnes": 5000.0,
        "p3_investsus": 4000.0,
        "p3_transferegov": 4000.0,
        "p3_sismob": 3500.0,
        "p3_fpo_bpa": 6000.0
    },
    "150 MIL A 200 MIL HABITANTES": {
        "p1_consultoria": 20000.0,
        "p1_capacitacao": 4500.0,
        "p1_bi": 30000.0,
        "p2_pec": 70000.0,
        "p2_app": 12000.0,
        "p2_regulacao": 10000.0,
        "p2_esus": 8500.0,
        "p2_hosp": 25000.0,
        "p3_cnes": 6000.0,
        "p3_investsus": 4500.0,
        "p3_transferegov": 4500.0,
        "p3_sismob": 4000.0,
        "p3_fpo_bpa": 7000.0
    },
    "200 A 300 MIL HABITANTES": {
        "p1_consultoria": 25000.0,
        "p1_capacitacao": 5000.0,
        "p1_bi": 35000.0,
        "p2_pec": 80000.0,
        "p2_app": 15000.0,
        "p2_regulacao": 12000.0,
        "p2_esus": 10000.0,
        "p2_hosp": 30000.0,
        "p3_cnes": 7000.0,
        "p3_investsus": 5000.0,
        "p3_transferegov": 5000.0,
        "p3_sismob": 4500.0,
        "p3_fpo_bpa": 8000.0
    },
    "300 A 400 MIL HABITANTES": {
        "p1_consultoria": 30000.0,
        "p1_capacitacao": 6000.0,
        "p1_bi": 40000.0,
        "p2_pec": 100000.0,
        "p2_app": 18000.0,
        "p2_regulacao": 15000.0,
        "p2_esus": 12000.0,
        "p2_hosp": 40000.0,
        "p3_cnes": 8000.0,
        "p3_investsus": 6000.0,
        "p3_transferegov": 6000.0,
        "p3_sismob": 5000.0,
        "p3_fpo_bpa": 9000.0
    },
    "400 A 500 MIL HABITANTES": {
        "p1_consultoria": 35000.0,
        "p1_capacitacao": 7000.0,
        "p1_bi": 45000.0,
        "p2_pec": 120000.0,
        "p2_app": 20000.0,
        "p2_regulacao": 18000.0,
        "p2_esus": 15000.0,
        "p2_hosp": 50000.0,
        "p3_cnes": 9000.0,
        "p3_investsus": 7000.0,
        "p3_transferegov": 7000.0,
        "p3_sismob": 6000.0,
        "p3_fpo_bpa": 10000.0
    },
    "500 A 600 MIL HABITANTES": {
        "p1_consultoria": 40000.0,
        "p1_capacitacao": 8000.0,
        "p1_bi": 50000.0,
        "p2_pec": 140000.0,
        "p2_app": 22000.0,
        "p2_regulacao": 20000.0,
        "p2_esus": 18000.0,
        "p2_hosp": 60000.0,
        "p3_cnes": 10000.0,
        "p3_investsus": 8000.0,
        "p3_transferegov": 8000.0,
        "p3_sismob": 7000.0,
        "p3_fpo_bpa": 12000.0
    },
    "600 A 800 MIL HABITANTES": {
        "p1_consultoria": 45000.0,
        "p1_capacitacao": 9000.0,
        "p1_bi": 55000.0,
        "p2_pec": 160000.0,
        "p2_app": 25000.0,
        "p2_regulacao": 22000.0,
        "p2_esus": 20000.0,
        "p2_hosp": 70000.0,
        "p3_cnes": 12000.0,
        "p3_investsus": 9000.0,
        "p3_transferegov": 9000.0,
        "p3_sismob": 8000.0,
        "p3_fpo_bpa": 15000.0
    },
    "800 MIL A 1 MILHÃO": {
        "p1_consultoria": 50000.0,
        "p1_capacitacao": 10000.0,
        "p1_bi": 60000.0,
        "p2_pec": 180000.0,
        "p2_app": 30000.0,
        "p2_regulacao": 25000.0,
        "p2_esus": 22000.0,
        "p2_hosp": 80000.0,
        "p3_cnes": 15000.0,
        "p3_investsus": 10000.0,
        "p3_transferegov": 10000.0,
        "p3_sismob": 9000.0,
        "p3_fpo_bpa": 18000.0
    }
}

# Lista de faixas populacionais - definida globalmente
faixas_populacionais = [
    "ATÉ 10 MIL HABITANTES",
    "10 MIL ATÉ 30 MIL HABITANTES",
    "30 A 50 MIL HABITANTES",
    "60 A 100 MIL HABITANTES",
    "100 A 150 MIL HABITANTES",
    "150 MIL A 200 MIL HABITANTES",
    "200 A 300 MIL HABITANTES",
    "300 A 400 MIL HABITANTES",
    "400 A 500 MIL HABITANTES",
    "500 A 600 MIL HABITANTES",
    "600 A 800 MIL HABITANTES",
    "800 MIL A 1 MILHÃO",
]

# --- Funções Utilitárias ---

# Função para formatar valores em Reais
def formatar_valor_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Função para criar um card de métrica estilizado
def metric_card(title, value, delta=None, prefix="R$"):
    # Formatando valor para o padrão brasileiro (vírgula para decimal, ponto para milhar)
    valor_formatado = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    html = f"""
    <div class="metric-container">
        <p style="font-size:0.9rem; color:gray">{title}</p>
        <h2 style="font-size:1.8rem; margin:0">{prefix} {valor_formatado}</h2>
    """
    if delta:
        delta_color = "green" if delta >= 0 else "red"
        delta_arrow = "↑" if delta >= 0 else "↓"
        delta_formatado = f"{abs(delta):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        html += f"""
        <p style="font-size:0.9rem; margin:0; color:{delta_color}">
            {delta_arrow} {delta_formatado} ({abs(delta/value*100 if value else 0):.1f}%)
        </p>
        """
    html += "</div>"
    
    return st.markdown(html, unsafe_allow_html=True)

# Função para criar gráficos de comparação
def create_comparison_chart(dados, titulo):
    fig = px.bar(
        dados, 
        x="Serviço", 
        y="Valor", 
        color="Categoria",
        title=titulo,
        color_discrete_map={
            "P1": CORES["primaria"], 
            "P2": CORES["secundaria"], 
            "P3": CORES["destaque"]
        }
    )
    fig.update_layout(
        plot_bgcolor="white",
        font=dict(family="Arial", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, l=50, r=30, b=50)
    )
    return fig

# Função para gerar PDF do orçamento
def generate_pdf_link():
    # Simulação da geração de PDF - em produção, você usaria uma biblioteca como ReportLab
    return st.markdown(
        """
        <div style="text-align:center; margin: 20px 0">
            <a href="#" style="background-color:#0066CC; color:white; padding:10px 20px; 
            border-radius:5px; text-decoration:none; font-weight:bold;">
            📄 Gerar PDF do Orçamento</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- Funções para Salvar e Carregar Orçamentos ---

# Diretório para salvar os orçamentos
ORCAMENTOS_DIR = "orcamentos"

def garantir_diretorio_orcamentos():
    """Garante que o diretório para salvar os orçamentos existe"""
    if not os.path.exists(ORCAMENTOS_DIR):
        os.makedirs(ORCAMENTOS_DIR)
        
def coletar_dados_orcamento():
    """Coleta todos os dados do orçamento atual do session_state"""
    dados = {
        # Informações do cliente
        "cliente": st.session_state.get("client_name", ""),
        "responsavel": st.session_state.get("responsavel_name", ""),
        "cargo": st.session_state.get("responsavel_cargo", ""),
        "email": st.session_state.get("email_contato", ""),
        "telefone": st.session_state.get("telefone", ""),
        "data_criacao": dt.now().strftime("%d/%m/%Y %H:%M:%S"),
        
        # Configurações gerais
        "faixa_populacional": st.session_state.get("faixa_populacional", ""),
        "p1_qtd": st.session_state.get("p1_qtd", 1),
        "p2_qtd": st.session_state.get("p2_qtd", 1),
        "p2_qtd_ace": st.session_state.get("p2_qtd_ace", 0),
        "has_hospital": st.session_state.get("has_hospital", False),
        
        # Valores P1
        "p1_consultoria_val": st.session_state.get("p1_consultoria_val", 0.0),
        "p1_capacitacao_val": st.session_state.get("p1_capacitacao_val", 0.0),
        "p1_bi_val": st.session_state.get("p1_bi_val", 0.0),
        
        # Valores P2
        "p2_pec_val": st.session_state.get("p2_pec_val", 0.0),
        "p2_app_val": st.session_state.get("p2_app_val", 0.0),
        "p2_regulacao_val": st.session_state.get("p2_regulacao_val", 0.0),
        "p2_esus_val": st.session_state.get("p2_esus_val", 0.0),
        "p2_hosp_val": st.session_state.get("p2_hosp_val", 0.0),
        
        # Valores P3
        "p3_cnes_val": st.session_state.get("p3_cnes_val", 0.0),
        "p3_investsus_val": st.session_state.get("p3_investsus_val", 0.0),
        "p3_transferegov_val": st.session_state.get("p3_transferegov_val", 0.0),
        "p3_sismob_val": st.session_state.get("p3_sismob_val", 0.0),
        "p3_fpo_bpa_val": st.session_state.get("p3_fpo_bpa_val", 0.0),
        
        # Totais calculados
        "total_p1": st.session_state.get("total_p1", 0.0),
        "total_p2": st.session_state.get("total_p2", 0.0),
        "total_p3": st.session_state.get("total_p3", 0.0),
    }
    
    return dados

def salvar_orcamento(nome_arquivo=None):
    """Salva o orçamento atual em um arquivo JSON"""
    garantir_diretorio_orcamentos()
    
    # Coletar dados do orçamento
    dados = coletar_dados_orcamento()
    
    # Se não foi fornecido um nome de arquivo, usar o nome do cliente e a data
    if not nome_arquivo:
        cliente = dados["cliente"] if dados["cliente"] else "orcamento"
        cliente = cliente.replace(" ", "_").lower()
        timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{cliente}_{timestamp}.json"
    
    # Garantir que a extensão .json esteja presente
    if not nome_arquivo.endswith('.json'):
        nome_arquivo += '.json'
    
    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(ORCAMENTOS_DIR, nome_arquivo)
    
    # Salvar em formato JSON
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    
    return nome_arquivo

def listar_orcamentos():
    """Lista todos os orçamentos salvos"""
    garantir_diretorio_orcamentos()
    arquivos = glob.glob(os.path.join(ORCAMENTOS_DIR, "*.json"))
    
    # Ordenar arquivos por data de modificação (mais recente primeiro)
    arquivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Retorna lista de tuplas com nome e data de orçamentos
    resultado = []
    for arquivo in arquivos:
        nome_arquivo = os.path.basename(arquivo)
        data_modificacao = dt.fromtimestamp(os.path.getmtime(arquivo)).strftime("%d/%m/%Y %H:%M:%S")
        
        # Tenta extrair informações do cliente do arquivo
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                cliente = dados.get("cliente", "")
                faixa = dados.get("faixa_populacional", "")
                resultado.append((nome_arquivo, cliente, faixa, data_modificacao))
        except:
            resultado.append((nome_arquivo, "Erro ao ler arquivo", "", data_modificacao))
    
    return resultado

def carregar_orcamento(nome_arquivo):
    """Carrega um orçamento salvo anteriormente"""
    caminho_arquivo = os.path.join(ORCAMENTOS_DIR, nome_arquivo)
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Atualizar o session_state com os dados carregados
        for chave, valor in dados.items():
            if chave not in ['data_criacao', 'total_p1', 'total_p2', 'total_p3']:
                st.session_state[chave] = valor
        
        return True, "Orçamento carregado com sucesso!"
    except Exception as e:
        return False, f"Erro ao carregar orçamento: {str(e)}"

def excluir_orcamento(nome_arquivo):
    """Exclui um orçamento salvo"""
    caminho_arquivo = os.path.join(ORCAMENTOS_DIR, nome_arquivo)
    
    try:
        os.remove(caminho_arquivo)
        return True, "Orçamento excluído com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir orçamento: {str(e)}"

def display_save_load_section():
    """Exibe a seção para salvar e carregar orçamentos"""
    st.header("Gerenciar Orçamentos")
    st.caption("Salve, carregue ou exclua orçamentos.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Salvar Orçamento Atual")
        
        # Verificar se há cliente definido
        cliente = st.session_state.get("client_name", "")
        
        # Sugerir nome de arquivo
        nome_sugerido = ""
        if cliente:
            nome_sugerido = f"{cliente.replace(' ', '_').lower()}_{dt.now().strftime('%Y%m%d')}"
        
        nome_arquivo = st.text_input("Nome do arquivo (opcional):", 
                                   value=nome_sugerido,
                                   placeholder="Ex: prefeitura_sao_paulo_20250422")
        
        if st.button("💾 Salvar Orçamento Atual"):
            try:
                nome_salvo = salvar_orcamento(nome_arquivo)
                st.success(f"Orçamento salvo com sucesso em: {nome_salvo}")
            except Exception as e:
                st.error(f"Erro ao salvar orçamento: {str(e)}")
    
    with col2:
        st.subheader("Orçamentos Salvos")
        
        # Listar orçamentos disponíveis
        orcamentos = listar_orcamentos()
        
        if not orcamentos:
            st.info("Nenhum orçamento salvo encontrado.")
        else:
            # Criar um DataFrame para exibir informações organizadas
            df_orcamentos = pd.DataFrame(orcamentos, columns=["Arquivo", "Cliente", "Faixa Populacional", "Data"])
            
            # Exibir a tabela de orçamentos
            st.dataframe(
                df_orcamentos,
                column_config={
                    "Arquivo": st.column_config.TextColumn("Arquivo"),
                    "Cliente": st.column_config.TextColumn("Cliente"),
                    "Faixa Populacional": st.column_config.TextColumn("Faixa"),
                    "Data": st.column_config.TextColumn("Data")
                },
                hide_index=True,
            )
            
            # Seleção de orçamento para carregar
            opcoes_orcamentos = [orç[0] for orç in orcamentos]
            orcamento_selecionado = st.selectbox("Selecione um orçamento:", opcoes_orcamentos)
            
            col_carregar, col_excluir = st.columns(2)
            
            with col_carregar:
                if st.button("📂 Carregar Orçamento"):
                    sucesso, mensagem = carregar_orcamento(orcamento_selecionado)
                    if sucesso:
                        st.success(mensagem)
                        st.rerun()  # Recarregar a página para exibir os novos valores
                    else:
                        st.error(mensagem)
            
            with col_excluir:
                if st.button("🗑️ Excluir Orçamento"):
                    sucesso, mensagem = excluir_orcamento(orcamento_selecionado)
                    if sucesso:
                        st.success(mensagem)
                        st.rerun()  # Recarregar a página para atualizar a lista
                    else:
                        st.error(mensagem)

# --- Funções de Cálculo e Exibição ---

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


def display_p2_calculator():
    st.header("P2 - Serviços Tecnológicos")
    st.caption("Configure os valores mensais de serviços tecnológicos com base nas necessidades do município.")

    col1, col2 = st.columns([1.2, 2])

    with col1:
        if 'p2_qtd' not in st.session_state: st.session_state.p2_qtd = 1
        if 'p2_qtd_ace' not in st.session_state: st.session_state.p2_qtd_ace = 0
        
        # Reutilizar a faixa populacional já selecionada
        faixa = st.session_state.get('faixa_populacional', faixas_populacionais[0])
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

    # Cálculo Total
    total_p2 = val_pec + val_app + val_regulacao + val_esus + val_hosp
    
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
        metric_card("eSUS Farma", val_esus)
    
    with col3:
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
            'Serviço': ['PEC Servidor', app_label, 'Sistema de Regulação', 'eSUS Farma', 'Sistema Hospitalar'],
            'Valor': [val_pec, val_app, val_regulacao, val_esus, val_hosp]
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


def display_p3_calculator():
    st.header("P3 - Sistemas de Saúde")
    st.caption("Configure os valores de sistemas oficiais de integração com o Ministério da Saúde.")

    # Usar faixas_populacionais já definida globalmente
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
                st.session_state.p3_transferegov_val = 2000.0
                st.session_state.p3_sismob_val = 1500.0
                st.session_state.p3_fpo_bpa_val = 3000.0
                
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

def display_summary():
    st.header("Resumo do Orçamento Completo")
    st.caption("Visualize o orçamento consolidado com todos os serviços selecionados.")
    
    # Recuperar valores dos orçamentos
    total_p1 = st.session_state.get('total_p1', 0)
    total_p2 = st.session_state.get('total_p2', 0)
    total_p3 = st.session_state.get('total_p3', 0)
    
    total_geral_mensal = total_p1 + total_p2
    total_geral_anual = total_geral_mensal * 12 + total_p3
    
    # Exibir informações do cliente
    cliente = st.session_state.get('client_name', '')
    faixa = st.session_state.get('faixa_populacional', faixas_populacionais[0])
    
    if cliente:
        st.subheader(f"Cliente: {cliente}")
    st.subheader(f"Faixa Populacional: {faixa}")
    
    # Criar tabela resumo
    st.markdown("### Valores Mensais")
    
    dados_mensais = pd.DataFrame({
        'Categoria': ['P1 - Consultoria', 'P2 - Tecnologia', 'Total Mensal'],
        'Valor': [total_p1, total_p2, total_geral_mensal]
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
    
    # Card do orçamento total
    st.markdown(f"""
    <div class="total-card" style="background-color: #f8f9fa; border-left-color: #0066CC; padding: 25px;">
        <h2 style="margin-bottom: 5px;">ORÇAMENTO TOTAL</h2>
        <p style="font-size: 0.9em; margin-bottom: 15px;">Valor mensal de serviços contínuos + sistemas de integração</p>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div>
                <p style="font-size: 0.9em; margin: 0;">Valor Mensal:</p>
                <h3 style="margin: 0;">{formatar_valor_reais(total_geral_mensal)}</h3>
            </div>
            <div>
                <p style="font-size: 0.9em; margin: 0;">Valor Anual:</p>
                <h3 style="margin: 0;">{formatar_valor_reais(total_geral_anual)}</h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de barras comparativo
    st.markdown("### Comparativo de Serviços")
    
    # Calcular valores detalhados para o gráfico
    if 'p1_consultoria_val' not in st.session_state: st.session_state.p1_consultoria_val = 0
    if 'p1_capacitacao_val' not in st.session_state: st.session_state.p1_capacitacao_val = 0
    if 'p1_bi_val' not in st.session_state: st.session_state.p1_bi_val = 0
    if 'p2_pec_val' not in st.session_state: st.session_state.p2_pec_val = 0
    if 'p2_app_val' not in st.session_state: st.session_state.p2_app_val = 0
    if 'p2_regulacao_val' not in st.session_state: st.session_state.p2_regulacao_val = 0
    if 'p2_esus_val' not in st.session_state: st.session_state.p2_esus_val = 0
    if 'p2_hosp_val' not in st.session_state: st.session_state.p2_hosp_val = 0
    if 'p3_cnes_val' not in st.session_state: st.session_state.p3_cnes_val = 0
    if 'p3_investsus_val' not in st.session_state: st.session_state.p3_investsus_val = 0
    if 'p3_transferegov_val' not in st.session_state: st.session_state.p3_transferegov_val = 0
    if 'p3_sismob_val' not in st.session_state: st.session_state.p3_sismob_val = 0
    if 'p3_fpo_bpa_val' not in st.session_state: st.session_state.p3_fpo_bpa_val = 0
    
    dados_detalhados = pd.DataFrame({
        'Serviço': [
            'Consultoria', 'Capacitação', 'BI Inteligente',
            'PEC Servidor', 'App ACE', 'Regulação', 'eSUS Farma', 'Sistema Hospitalar',
            'CNES', 'InvestSUS', 'TransfereGov', 'SISMOB', 'FPO e BPA'
        ],
        'Valor': [
            st.session_state.p1_consultoria_val, 
            st.session_state.p1_capacitacao_val,
            st.session_state.p1_bi_val,
            st.session_state.p2_pec_val,
            st.session_state.p2_app_val,
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
            'P2', 'P2', 'P2', 'P2', 'P2',
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

# Abas para navegação
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 P1 - Consultoria", "💻 P2 - Tecnologia", "🔄 P3 - Integração", "📝 Resumo", "💾 Gerenciar Orçamentos"])

with tab1:
    display_p1_calculator()

with tab2:
    display_p2_calculator()

with tab3:
    display_p3_calculator()

with tab4:
    display_summary()

with tab5:
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
        st.session_state.p3_faixa = faixas_populacionais[0]
        
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