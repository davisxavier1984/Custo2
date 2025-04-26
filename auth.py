import streamlit as st
import hashlib
from config import CORES
from utils import get_logo

def init_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'users' not in st.session_state:
        st.session_state.users = {
            'admin': hashlib.sha256('admin123'.encode()).hexdigest(),
        }

def login_page():
    # Configurações gerais da página
    st.markdown("""
    <style>
    /* Configurações mínimas sem HTML visível */
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Espaçamento usando componentes nativos
    st.write("")
    st.write("")
    
    # Container com coluna central
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        # Container para centralizar e organizar
        with st.container():
            # Logo centralizada
            logo = get_logo()
            st.image(logo, width=140)
            
            # Títulos com componentes nativos
            st.title("Bem-vindo", anchor=False)
            st.write("Sistema de Orçamento - Mais Gestor")
            
            # Separador simples
            st.write("---")
            
            # Formulário de login nativo
            with st.form(key="login_form"):
                username = st.text_input("Usuário")
                password = st.text_input("Senha", type="password")
                submit = st.form_submit_button(label="Entrar", use_container_width=True)
                
                if submit:
                    if verify_credentials(username, password):
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")

def verify_credentials(username, password):
    if username in st.session_state.users:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return st.session_state.users[username] == hashed_password
    return False

def logout():
    st.session_state.authenticated = False
    st.rerun()

def change_password():
    # Usando apenas elementos nativos do Streamlit
    st.title("Alterar Senha")
    
    # Usando container para melhorar o layout
    with st.container():
        # Criando o formulário
        with st.form("change_password_form"):
            st.subheader("Dados da Conta")
            
            # Campos do formulário
            current_password = st.text_input("Senha Atual", type="password")
            st.write("") # Espaço para separação
            
            new_password = st.text_input("Nova Senha", type="password")
            st.write("") # Espaço para separação
            
            confirm_password = st.text_input("Confirmar Nova Senha", type="password")
            st.write("") # Espaço para separação
            
            # Botão que ocupa toda a largura disponível
            submit = st.form_submit_button("Alterar Senha", use_container_width=True)

            if submit:
                if new_password != confirm_password:
                    st.error("As senhas não coincidem!")
                    return
                
                if verify_credentials('admin', current_password):
                    st.session_state.users['admin'] = hashlib.sha256(new_password.encode()).hexdigest()
                    st.success("Senha alterada com sucesso!")
                else:
                    st.error("Senha atual incorreta!")