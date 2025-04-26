import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import io
from config import CORES
from datetime import datetime as dt
import tempfile
import os
from fpdf import FPDF
import matplotlib.pyplot as plt

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

# Função para criar uma métrica simples sem card
def metric_card(title, value, delta=None, prefix="R$"):
    # Formatando valor para o padrão brasileiro (vírgula para decimal, ponto para milhar)
    valor_formatado = f"{prefix} {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Usando o componente nativo do Streamlit
    if delta:
        delta_formatado = f"{delta:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.metric(title, valor_formatado, delta=delta_formatado)
    else:
        st.metric(title, valor_formatado)

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
def generate_pdf_report():
    # Recuperar todos os dados necessários do session_state
    cliente = st.session_state.get('client_name', 'Cliente não especificado')
    faixa_populacional = st.session_state.get('faixa_populacional', '')
    responsavel = st.session_state.get('responsavel_name', '')
    cargo = st.session_state.get('responsavel_cargo', '')
    email = st.session_state.get('email_contato', '')
    telefone = st.session_state.get('telefone', '')
    
    # Recuperar valores dos orçamentos
    total_p1 = st.session_state.get('total_p1', 0)
    total_p2 = st.session_state.get('total_p2', 0)
    total_p3 = st.session_state.get('total_p3', 0)
    
    # Configurações financeiras
    comissao_percentual = st.session_state.get('comissao_percentual', 5.0)
    lucro_percentual = st.session_state.get('lucro_percentual', 20.0)
    imposto_percentual = st.session_state.get('imposto_percentual', 8.65)
    
    # Cálculos
    total_base_mensal = total_p1 + total_p2
    comissao_valor = total_base_mensal * (comissao_percentual / 100)
    lucro_valor = total_base_mensal * (lucro_percentual / 100)
    impostos_valor = total_base_mensal * (imposto_percentual / 100)
    total_geral_mensal = total_base_mensal + comissao_valor + lucro_valor + impostos_valor
    total_geral_anual = total_geral_mensal * 12 + total_p3
    
    # Valores detalhados dos serviços
    servicos_p1 = {
        'Consultoria': st.session_state.get('p1_consultoria_val', 0),
        'Capacitação': st.session_state.get('p1_capacitacao_val', 0),
        'BI Inteligente': st.session_state.get('p1_bi_val', 0)
    }
    
    servicos_p2 = {
        'PEC Servidor': st.session_state.get('p2_pec_val', 0),
        'App ACE': st.session_state.get('p2_app_val', 0),
        'Comodato Aparelhos': st.session_state.get('p2_comodato_val', 0),
        'Regulação': st.session_state.get('p2_regulacao_val', 0),
        'eSUS Farma': st.session_state.get('p2_esus_val', 0),
        'Sistema Hospitalar': st.session_state.get('p2_hosp_val', 0)
    }
    
    servicos_p3 = {
        'CNES': st.session_state.get('p3_cnes_val', 0),
        'InvestSUS': st.session_state.get('p3_investsus_val', 0),
        'TransfereGov': st.session_state.get('p3_transferegov_val', 0),
        'SISMOB': st.session_state.get('p3_sismob_val', 0),
        'FPO e BPA': st.session_state.get('p3_fpo_bpa_val', 0)
    }
    
    # Criar um gráfico para incluir no PDF
    dados_grafico = []
    categorias = []
    
    for nome, valor in servicos_p1.items():
        if valor > 0:
            dados_grafico.append(valor)
            categorias.append(nome)
    
    for nome, valor in servicos_p2.items():
        if valor > 0:
            dados_grafico.append(valor)
            categorias.append(nome)
    
    # Salvar o gráfico em um arquivo temporário se houver dados
    chart_path = None
    if dados_grafico:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categorias, dados_grafico, color=[CORES["primaria"], CORES["secundaria"]])
        plt.title('Serviços Mensais')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Salvar temporariamente o gráfico
        chart_path = os.path.join(tempfile.gettempdir(), 'chart.png')
        plt.savefig(chart_path)
        plt.close()
    
    # Criar o PDF usando FPDF
    class PDF(FPDF):
        def header(self):
            # Logo reduzida para um tamanho menor (33 -> 25)
            try:
                self.image("logo.png", 10, 8, 25)
            except:
                pass
            # Título
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Mais Gestor - Orçamento Detalhado', 0, 1, 'C')
            # Data
            self.set_font('Arial', '', 10)
            self.cell(0, 10, f'Data: {dt.now().strftime("%d/%m/%Y")}', 0, 1, 'R')
            # Linha
            self.line(10, 30, 200, 30)
            # Espaçamento após cabeçalho
            self.ln(10)

    # Inicializar PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Informações do cliente
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'INFORMAÇÕES DO CLIENTE', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f'Cliente: {cliente}', 0, 1)
    pdf.cell(0, 8, f'Faixa Populacional: {faixa_populacional}', 0, 1)
    
    if responsavel or cargo or email or telefone:
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, 'Contato:', 0, 1)
        pdf.set_font('Arial', '', 11)
        if responsavel: pdf.cell(0, 8, f'Nome: {responsavel}', 0, 1)
        if cargo: pdf.cell(0, 8, f'Cargo: {cargo}', 0, 1)
        if email: pdf.cell(0, 8, f'Email: {email}', 0, 1)
        if telefone: pdf.cell(0, 8, f'Telefone: {telefone}', 0, 1)
    
    # Resumo financeiro
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'RESUMO FINANCEIRO MENSAL', 0, 1)
    
    # Tabela de valores mensais
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 10)
    
    # Cabeçalho da tabela
    pdf.cell(90, 8, 'Serviço', 1, 0, 'C', 1)
    pdf.cell(90, 8, 'Valor Mensal (R$)', 1, 1, 'C', 1)
    
    # Dados da tabela
    pdf.set_font('Arial', '', 10)
    pdf.cell(90, 8, 'P1 - Consultoria', 1, 0)
    pdf.cell(90, 8, f'{total_p1:,.2f}'.replace(',', '.'), 1, 1, 'R')
    
    pdf.cell(90, 8, 'P2 - Tecnologia', 1, 0)
    pdf.cell(90, 8, f'{total_p2:,.2f}'.replace(',', '.'), 1, 1, 'R')
    
    pdf.cell(90, 8, 'Subtotal', 1, 0)
    pdf.cell(90, 8, f'{total_base_mensal:,.2f}'.replace(',', '.'), 1, 1, 'R')
    
    pdf.cell(90, 8, f'Comissão ({comissao_percentual}%)', 1, 0)
    pdf.cell(90, 8, f'{comissao_valor:,.2f}'.replace(',', '.'), 1, 1, 'R')
    
    pdf.cell(90, 8, f'Lucro ({lucro_percentual}%)', 1, 0)
    pdf.cell(90, 8, f'{lucro_valor:,.2f}'.replace(',', '.'), 1, 1, 'R')
    
    pdf.cell(90, 8, f'Impostos ({imposto_percentual}%)', 1, 0)
    pdf.cell(90, 8, f'{impostos_valor:,.2f}'.replace(',', '.'), 1, 1, 'R')
    
    # Total mensal com destaque
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(90, 8, 'TOTAL MENSAL', 1, 0, 'L', 1)
    pdf.cell(90, 8, f'{total_geral_mensal:,.2f}'.replace(',', '.'), 1, 1, 'R', 1)
    
    # P3 - Sistemas de Integração
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'SISTEMAS DE INTEGRAÇÃO (P3)', 0, 1)
    
    # Adicionar os serviços P3 se houver algum valor
    any_p3 = any(valor > 0 for valor in servicos_p3.values())
    
    if any_p3:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(90, 8, 'Serviço', 1, 0, 'C', 1)
        pdf.cell(90, 8, 'Valor (R$)', 1, 1, 'C', 1)
        
        pdf.set_font('Arial', '', 10)
        for nome, valor in servicos_p3.items():
            if valor > 0:
                pdf.cell(90, 8, nome, 1, 0)
                pdf.cell(90, 8, f'{valor:,.2f}'.replace(',', '.'), 1, 1, 'R')
        
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(90, 8, 'TOTAL P3', 1, 0, 'L', 1)
        pdf.cell(90, 8, f'{total_p3:,.2f}'.replace(',', '.'), 1, 1, 'R', 1)
    else:
        pdf.cell(0, 8, 'Nenhum serviço de integração selecionado.', 0, 1)
    
    # Total geral (anual)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'TOTAL DO ORÇAMENTO', 0, 1)
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, f'Total Anual: R$ {total_geral_anual:,.2f}'.replace(',', '.'), 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f'(12 x Mensal + Sistemas de Integração)', 0, 1)
    
    # Adicionar gráfico se disponível
    if chart_path and os.path.exists(chart_path):
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'GRÁFICO DE SERVIÇOS MENSAIS', 0, 1, 'C')
        pdf.image(chart_path, x=25, w=160)
        
        # Remover arquivo temporário
        try:
            os.remove(chart_path)
        except:
            pass
    
    # Rodapé
    pdf.ln(15)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, '© 2025 Mais Gestor - Soluções em Gestão de Saúde | Versão 2.0', 0, 1, 'C')
    
    # Salvar PDF em um arquivo temporário
    pdf_path = os.path.join(tempfile.gettempdir(), f'orcamento_{cliente.lower().replace(" ", "_")}_{dt.now().strftime("%Y%m%d")}.pdf')
    pdf.output(pdf_path)
    
    return pdf_path

# Função para o botão de download do PDF
def generate_pdf_link():
    if st.button('📄 Gerar PDF do Orçamento'):
        with st.spinner('Gerando PDF...'):
            try:
                pdf_path = generate_pdf_report()
                
                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                
                # Nome do arquivo para download
                cliente = st.session_state.get('client_name', 'cliente')
                file_name = f'orcamento_{cliente.lower().replace(" ", "_")}_{dt.now().strftime("%Y%m%d")}.pdf'
                
                # Criar botão de download
                st.download_button(
                    label="📥 Baixar PDF do Orçamento",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime="application/pdf",
                )
                
                st.success("PDF gerado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {str(e)}")
                st.info("Verifique se todas as informações necessárias foram preenchidas.")