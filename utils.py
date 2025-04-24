import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import io
from config import CORES

# --- Funções Utilitárias ---

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