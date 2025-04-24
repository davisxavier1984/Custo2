import os
import json
import glob
import streamlit as st
import pandas as pd
from datetime import datetime as dt
from config import ORCAMENTOS_DIR

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
        "p2_comodato_val": st.session_state.get("p2_comodato_val", 0.0),
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