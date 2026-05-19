import streamlit as st
import pandas as pd
import unicodedata
import re

# ==========================================
# Configurações Iniciais
# ==========================================
st.set_page_config(page_title="UFG Responde", layout="wide")

# ==========================================
# Sistema de Tradução (i18n)
# ==========================================
TRANSLATIONS = {
    "pt": {
        "subtitle": "Vamos colocar em prática a missão da UFG",
        "title": "Você pergunta, UFG RESPONDE",
        "search_placeholder": "🔍 Digite uma palavra-chave (ex: água, solo, carbono, saúde)",
        "what_looking": "O que você está procurando?",
        "all": "Todos",
        "researcher": "Pesquisador",
        "project": "Projeto",
        "lab": "Laboratório",
        "publications": "Publicações",
        "refine": "Filtrar Busca",
        "area": "Grande Área",
        "status": "Status do Projeto",
        "unit": "Unidade",
        "all_f": "Todas",
        "all_m": "Todos",
        "results": "Resultados",
        "chatbot_title": "💬 Assistente Virtual UFG RESPONDE",
        "chatbot_caption": "Converse comigo para encontrar a informação que você precisa!",
        "chatbot_welcome": "Olá! Sou o assistente de triagem. Diga-me qual assunto você procura (ex: 'análise de solo' ou 'matemática')",
        "chatbot_input": "Digite sua pergunta ou tema...",
        "chatbot_found": "Encontrei! 📋 **Projeto:** {proj}\n\n📍 **Unidade:** {unit}\n\n👤 **Coordenador:** {coord}\n\n📧 **E-mail:** {email}",
        "chatbot_not_found": "Não encontrei resultados com esse termo na base de dados atual. Poderia tentar outras palavras-chave?",
        "send_email": "✉️ Enviar E-mail de Contato",
        "col_project": "Projeto",
        "col_unit": "Unidade",
        "col_coord": "Coordenador",
        "col_email": "E-mail",
        "col_status": "Status",
        "col_lab": "Laboratório",
        "col_pubs": "Publicações",
        "skip_content": "Ir para o conteúdo [1]",
        "skip_menu": "Ir para o menu [2]",
        "skip_search": "Ir para busca [3]",
        "access_info": "Acesso à Informação",
        "high_contrast": "Alto Contraste",
        "libras": "Libras",
        "chat_btn_open": "💬 Assistente",
        "chat_btn_close": "✕ Fechar Chat",
        "chat_panel_title": "Assistente UFG Responde",
        "chat_panel_subtitle": "Olá! Como posso ajudá-lo hoje?",
    },
    "en": {
        "subtitle": "Let's put UFG's mission into practice",
        "title": "You ask, UFG ANSWERS",
        "search_placeholder": "🔍 Type a keyword (e.g.: water, soil, carbon, health)",
        "what_looking": "What are you looking for?",
        "all": "All",
        "researcher": "Researcher",
        "project": "Project",
        "lab": "Laboratory",
        "publications": "Publications",
        "refine": "Filter Search",
        "area": "Major Area",
        "status": "Project Status",
        "unit": "Unit",
        "all_f": "All",
        "all_m": "All",
        "results": "Results",
        "chatbot_title": "💬 UFG ANSWERS Virtual Assistant",
        "chatbot_caption": "Chat with me to find the information you need!",
        "chatbot_welcome": "Hello! I'm the triage assistant. Tell me what subject you are looking for (e.g.: 'soil analysis' or 'mathematics')",
        "chatbot_input": "Type your question or topic...",
        "chatbot_found": "Found it! 📋 **Project:** {proj}\n\n📍 **Unit:** {unit}\n\n👤 **Coordinator:** {coord}\n\n📧 **E-mail:** {email}",
        "chatbot_not_found": "I didn't find results with that term in the current database. Could you try other keywords?",
        "send_email": "✉️ Send Contact E-mail",
        "col_project": "Project",
        "col_unit": "Unit",
        "col_coord": "Coordinator",
        "col_email": "E-mail",
        "col_status": "Status",
        "col_lab": "Laboratory",
        "col_pubs": "Publications",
        "skip_content": "Skip to content [1]",
        "skip_menu": "Skip to menu [2]",
        "skip_search": "Skip to search [3]",
        "access_info": "Access Information",
        "high_contrast": "High Contrast",
        "libras": "Libras (Sign Language)",
        "chat_btn_open": "💬 Assistant",
        "chat_btn_close": "✕ Close Chat",
        "chat_panel_title": "UFG Answers Assistant",
        "chat_panel_subtitle": "Hello! How may I assist you today?",
    },
    "es": {
        "subtitle": "Pongamos en práctica la misión de la UFG",
        "title": "Tú preguntas, UFG RESPONDE",
        "search_placeholder": "🔍 Escriba una palabra clave (ej.: agua, suelo, carbono, salud)",
        "what_looking": "¿Qué estás buscando?",
        "all": "Todos",
        "researcher": "Investigador",
        "project": "Proyecto",
        "lab": "Laboratorio",
        "publications": "Publicaciones",
        "refine": "Filtrar Búsqueda",
        "area": "Gran Área",
        "status": "Estado del Proyecto",
        "unit": "Unidad",
        "all_f": "Todas",
        "all_m": "Todos",
        "results": "Resultados",
        "chatbot_title": "💬 Asistente Virtual UFG RESPONDE",
        "chatbot_caption": "¡Habla conmigo para encontrar la información que necesitas!",
        "chatbot_welcome": "¡Hola! Soy el asistente de triaje. Dime qué tema buscas (ej.: 'análisis de suelo' o 'matemáticas')",
        "chatbot_input": "Escribe tu pregunta o tema...",
        "chatbot_found": "¡Encontrado! 📋 **Proyecto:** {proj}\n\n📍 **Unidad:** {unit}\n\n👤 **Coordinador:** {coord}\n\n📧 **E-mail:** {email}",
        "chatbot_not_found": "No encontré resultados con ese término en la base de datos actual. ¿Podrías probar con otras palabras clave?",
        "send_email": "✉️ Enviar E-mail de Contacto",
        "col_project": "Proyecto",
        "col_unit": "Unidad",
        "col_coord": "Coordinador",
        "col_email": "E-mail",
        "col_status": "Estado",
        "col_lab": "Laboratorio",
        "col_pubs": "Publicaciones",
        "skip_content": "Ir al contenido [1]",
        "skip_menu": "Ir al menú [2]",
        "skip_search": "Ir a búsqueda [3]",
        "access_info": "Acceso a la Información",
        "high_contrast": "Alto Contraste",
        "libras": "Libras (Lengua de Señas)",
        "chat_btn_open": "💬 Asistente",
        "chat_btn_close": "✕ Cerrar Chat",
        "chat_panel_title": "Asistente UFG Responde",
        "chat_panel_subtitle": "¡Hola! ¿En qué puedo ayudarle hoy?",
    },
}

# Inicializar idioma
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

def t(key):
    """Retorna o texto traduzido para o idioma atual."""
    return TRANSLATIONS[st.session_state.lang].get(key, key)


# ==========================================
# CSS Global
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
    --primary-navy: #0A2A56;
    --vibrant-green: #4D9933;
    --cyan-pool: #00A1C9;
    --bg-light: #F8F9FA;
}

.stApp {
    background-color: var(--primary-navy);
    background-image: linear-gradient(180deg, var(--primary-navy) 0%, #051630 100%);
    font-family: 'Inter', sans-serif;
}

/* Textos em branco */
h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
    color: white !important;
    font-family: 'Inter', sans-serif;
}
a { color: var(--cyan-pool) !important; }

/* Inputs */
.stTextInput > div > div > input, [data-baseweb="select"] {
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: black !important;
    border-radius: 10px;
}

/* Bolhas de Chat */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    backdrop-filter: blur(8px);
}

/* Chat input */
[data-testid="stChatInput"] textarea {
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: black !important;
    border-radius: 10px;
}

/* Botões Principais */
.stButton > button {
    background-color: var(--cyan-pool);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background-color: var(--vibrant-green);
    color: white;
    border: none;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(77,153,51,0.4);
}

/* Barra de Acessibilidade */
.gov-accessibility-bar {
    background-color: #222;
    padding: 6px 4%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    border-bottom: 2px solid var(--cyan-pool);
    font-family: 'Inter', Arial, sans-serif;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
}
.gov-links a {
    margin-right: 15px;
    color: #ccc !important;
    text-decoration: none;
    font-size: 11px;
}
.gov-links a:hover {
    text-decoration: underline;
    color: white !important;
}
.gov-controls {
    display: flex;
    align-items: center;
    gap: 10px;
}
.gov-controls span, .gov-controls div {
    display: flex;
    align-items: center;
    cursor: pointer;
}
.gov-controls-btn {
    background: #444;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 600;
    color: #eee;
    font-size: 11px;
    transition: background 0.2s;
}
.gov-controls-btn:hover {
    background: #666;
}

/* Espaçamento para não ficar sob a barra fixa */
.block-container {
    padding-top: 3.5rem !important;
}

/* Tabela / Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Radio buttons */
[data-testid="stRadio"] > div {
    gap: 0.5rem;
}
[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    padding: 6px 14px !important;
    transition: all 0.2s;
}
[data-testid="stRadio"] label:hover {
    background: rgba(0,161,201,0.3);
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.15) !important;
}

/* ========== CHAT FLUTUANTE ========== */
.chat-fab {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 99999;
    background: linear-gradient(135deg, #00A1C9, #0A2A56);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 14px 22px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 6px 24px rgba(0,161,201,0.5);
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.3px;
}
.chat-fab:hover {
    background: linear-gradient(135deg, #4D9933, #0A2A56);
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(77,153,51,0.5);
}

/* Painel lateral de chat */
.chat-panel {
    position: fixed;
    top: 0;
    right: 0;
    width: 380px;
    height: 100vh;
    background: linear-gradient(180deg, #0d1f3c 0%, #071428 100%);
    border-left: 2px solid rgba(0,161,201,0.4);
    z-index: 99998;
    display: flex;
    flex-direction: column;
    box-shadow: -8px 0 32px rgba(0,0,0,0.5);
    font-family: 'Inter', sans-serif;
    animation: slideInRight 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to   { transform: translateX(0);   opacity: 1; }
}
.chat-panel-header {
    background: linear-gradient(135deg, #00A1C9, #0A2A56);
    padding: 18px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.chat-panel-header h3 {
    margin: 0;
    font-size: 15px;
    font-weight: 700;
    color: white;
}
.chat-panel-header p {
    margin: 2px 0 0 0;
    font-size: 11px;
    color: rgba(255,255,255,0.75);
}
.chat-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-right: 12px;
    flex-shrink: 0;
}
.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 18px 14px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }

.chat-bubble {
    max-width: 82%;
    padding: 10px 14px;
    border-radius: 16px;
    font-size: 13px;
    line-height: 1.5;
    word-break: break-word;
}
.chat-bubble.bot {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    color: white;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
}
.chat-bubble.user {
    background: linear-gradient(135deg, #00A1C9, #007fa0);
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
    text-align: right;
}
.chat-bubble a {
    color: #7FFFAA !important;
    font-weight: 700;
}
.chat-timestamp {
    font-size: 10px;
    color: rgba(255,255,255,0.4);
    margin-top: 2px;
}
.chat-bubble.bot .chat-timestamp { text-align: left; }
.chat-bubble.user .chat-timestamp { text-align: right; }

.chat-input-area {
    padding: 14px;
    border-top: 1px solid rgba(255,255,255,0.1);
    background: rgba(0,0,0,0.2);
    display: flex;
    gap: 8px;
    align-items: center;
}
.chat-close-btn {
    background: rgba(255,255,255,0.15);
    border: none;
    color: white;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}
.chat-close-btn:hover {
    background: rgba(255,0,0,0.3);
}
/* Overlay escuro ao abrir chat */
.chat-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.35);
    z-index: 99990;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# Barra de Acessibilidade com troca real de idioma
# ==========================================
st.markdown(f"""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<div class="gov-accessibility-bar">
    <div class="gov-links">
        <a href="#conteudo">{t('skip_content')}</a>
        <a href="#menu">{t('skip_menu')}</a>
        <a href="#busca">{t('skip_search')}</a>
    </div>
    <div class="gov-controls">
        <span class="gov-controls-btn"><i class="fa-solid fa-circle-info" style="color: #FFD700; margin-right: 4px;"></i> {t('access_info')}</span>
        <span class="gov-controls-btn" title="A+">A+</span>
        <span class="gov-controls-btn" title="A-">A-</span>
        <span class="gov-controls-btn"><i class="fa-solid fa-circle-half-stroke" style="margin-right: 4px;"></i> {t('high_contrast')}</span>
        <span class="gov-controls-btn"><i class="fa-solid fa-hands-asl-interpreting" style="color: #00A1C9; margin-right: 4px;"></i> {t('libras')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Seletor de idioma FUNCIONAL via Streamlit (troca real de idioma)
lang_labels = {"pt": "🇧🇷 Português", "en": "🇺🇸 English", "es": "🇪🇸 Español"}
col_lang_spacer, col_lang = st.columns([4, 1])
with col_lang:
    selected_lang = st.selectbox(
        "🌐",
        options=["pt", "en", "es"],
        format_func=lambda x: lang_labels[x],
        index=["pt", "en", "es"].index(st.session_state.lang),
        key="lang_selector",
        label_visibility="collapsed"
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

# Widget VLibras
st.markdown("""
<div vw class="enabled">
  <div vw-access-button class="active"></div>
  <div vw-plugin-wrapper>
    <div class="vw-plugin-top-wrapper"></div>
  </div>
</div>
<script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
<script>
  new window.VLibras.Widget('https://vlibras.gov.br/app');
</script>
""", unsafe_allow_html=True)


# ==========================================
# Textos Iniciais ANTES da Logo
# ==========================================
st.markdown("<div id='conteudo'></div>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center; margin-top: 0.5rem; color: #4D9933 !important;'>{t('subtitle')}</h4>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; margin-bottom: 1.5rem; font-size: 2.5rem;'>{t('title')}</h1>", unsafe_allow_html=True)

# Logo centralizada e proporcional
col1, col2, col3 = st.columns([1.5, 1, 1.5])
with col2:
    try:
        st.image("UFG_RESPONDE.jpeg", use_container_width=True)
    except:
        st.info("[Placeholder: Logo UFG_RESPONDE]")


# ==========================================
# Carregamento de Dados
# ==========================================
@st.cache_data
def load_and_augment_data():
    try:
        df_pesquisa = pd.read_csv("da_projetos_pesquisa.csv", encoding="utf-8")
    except UnicodeDecodeError:
        df_pesquisa = pd.read_csv("da_projetos_pesquisa.csv", encoding="latin1")

    try:
        df_extensao = pd.read_csv("da_bolsas_extensao.csv", encoding="utf-8")
    except UnicodeDecodeError:
        df_extensao = pd.read_csv("da_bolsas_extensao.csv", encoding="latin1")

    df_pesquisa = df_pesquisa.rename(columns={
        'coordenador_projeto_pesquisa': 'nome_pesquisador',
        'titulo_projeto_pesquisa': 'titulo_projeto',
        'status_projeto_pesquisa': 'status'
    })

    df_extensao = df_extensao.rename(columns={
        'coordenador': 'nome_pesquisador',
        'titulo': 'titulo_projeto',
        'situacao': 'status',
        'unidade': 'unidade_coordenador_projeto'
    })
    df_extensao['grande_area'] = 'Extensão'

    df = pd.concat([df_pesquisa, df_extensao], ignore_index=True)

    df['nome_pesquisador'] = df['nome_pesquisador'].fillna("Desconhecido")
    df['unidade_coordenador_projeto'] = df['unidade_coordenador_projeto'].fillna("Não informada")
    df['titulo_projeto'] = df['titulo_projeto'].fillna("Sem Título")
    df['status'] = df['status'].fillna("Não informado")
    df['grande_area'] = df['grande_area'].fillna("Não informada")
    df['resumo'] = df['titulo_projeto']
    df['publicacoes'] = "Registros pendentes"

    def generate_email(nome):
        nfkd_form = unicodedata.normalize('NFKD', str(nome))
        clean_name = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        clean_name = clean_name.lower().replace(" ", "_")
        return f"{clean_name}@ufg.br"

    df['email'] = df['nome_pesquisador'].apply(generate_email)

    lab_map = {
        "INSTITUTO DE INFORMÁTICA": "Laboratório de Inteligência Artificial",
        "ESCOLA DE AGRONOMIA": "Laboratório de Análise de Solos",
        "INSTITUTO DE QUÍMICA": "Laboratório de Química de Materiais",
        "FACULDADE DE MEDICINA": "Laboratório de Saúde Pública"
    }
    df['laboratorio'] = df['unidade_coordenador_projeto'].str.upper().map(lab_map).fillna("Laboratório Central Padrão")

    return df

df = load_and_augment_data()


# ==========================================
# Busca e Filtros
# ==========================================
st.markdown("<div id='busca'></div>", unsafe_allow_html=True)

search_query = st.text_input(t("search_placeholder"), label_visibility="collapsed", placeholder=t("search_placeholder"))

if search_query:
    # 1) PRIMEIRO: O que você está procurando? (com Todos)
    st.markdown(f"#### {t('what_looking')}")
    tipo_busca = st.radio(
        t("what_looking"),
        [t("all"), t("researcher"), t("project"), t("lab"), t("publications")],
        horizontal=True,
        label_visibility="collapsed"
    )

    # 2) DEPOIS: Filtros adicionais
    st.markdown(f"#### {t('refine')}")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_area = st.selectbox(t("area"), options=[t("all_f")] + sorted(df['grande_area'].unique().tolist()))
    with col_f2:
        f_status = st.selectbox(t("status"), options=[t("all_m")] + sorted(df['status'].unique().tolist()))
    with col_f3:
        f_unidade = st.selectbox(t("unit"), options=[t("all_f")] + sorted(df['unidade_coordenador_projeto'].unique().tolist()))

    # Lógica de Filtragem
    filtered_df = df.copy()
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

    if f_area != t("all_f"):
        filtered_df = filtered_df[filtered_df['grande_area'] == f_area]
    if f_status != t("all_m"):
        filtered_df = filtered_df[filtered_df['status'] == f_status]
    if f_unidade != t("all_f"):
        filtered_df = filtered_df[filtered_df['unidade_coordenador_projeto'] == f_unidade]

    # 3) Resultados formatados com as colunas corretas
    st.markdown(f"#### {t('results')} ({len(filtered_df)})")

    if tipo_busca == t("all"):
        display_df = filtered_df[['titulo_projeto', 'unidade_coordenador_projeto', 'nome_pesquisador', 'email']].copy()
        display_df.columns = [t('col_project'), t('col_unit'), t('col_coord'), t('col_email')]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    elif tipo_busca == t("researcher"):
        display_df = filtered_df[['nome_pesquisador', 'email', 'unidade_coordenador_projeto']].copy()
        display_df.columns = [t('col_coord'), t('col_email'), t('col_unit')]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    elif tipo_busca == t("project"):
        display_df = filtered_df[['titulo_projeto', 'unidade_coordenador_projeto', 'nome_pesquisador', 'email', 'status']].copy()
        display_df.columns = [t('col_project'), t('col_unit'), t('col_coord'), t('col_email'), t('col_status')]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    elif tipo_busca == t("lab"):
        display_df = filtered_df[['laboratorio', 'unidade_coordenador_projeto', 'nome_pesquisador', 'email']].copy()
        display_df.columns = [t('col_lab'), t('col_unit'), t('col_coord'), t('col_email')]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    elif tipo_busca == t("publications"):
        display_df = filtered_df[['titulo_projeto', 'publicacoes', 'nome_pesquisador', 'email']].copy()
        display_df.columns = [t('col_project'), t('col_pubs'), t('col_coord'), t('col_email')]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()


# ==========================================
# Chat Flutuante (Painel Lateral)
# ==========================================

# Inicializa estado do chat — limpa mensagens a cada nova visita ao site
if "chat_session_started" not in st.session_state:
    st.session_state.chat_session_started = True
    st.session_state.messages = []  # Limpo a cada nova sessão
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# ---- BOTÃO FLUTUANTE (sempre visível) ----
if not st.session_state.chat_open:
    st.markdown(f"""
    <form method="post" style="position:fixed; bottom:28px; right:28px; z-index:99999;">
    </form>
    """, unsafe_allow_html=True)
    if st.button(t("chat_btn_open"), key="open_chat",
                 help="Abrir o assistente virtual",
                 type="primary"):
        st.session_state.chat_open = True
        st.rerun()
    # CSS para posicionar botão como FAB
    st.markdown("""
    <style>
    [data-testid="stBaseButton-primary"] {
        position: fixed !important;
        bottom: 28px !important;
        right: 28px !important;
        z-index: 99999 !important;
        border-radius: 50px !important;
        background: linear-gradient(135deg, #00A1C9, #0A2A56) !important;
        padding: 14px 22px !important;
        font-size: 15px !important;
        box-shadow: 0 6px 24px rgba(0,161,201,0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---- PAINEL LATERAL DE CHAT ----
if st.session_state.chat_open:
    import datetime

    # Mensagem inicial de boas-vindas (sempre fresca)
    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "assistant",
            "content": (
                f"Olá! Seja muito bem-vindo(a) ao **Assistente UFG Responde**. 😊\n\n"
                f"Estou aqui para ajudá-lo(a) a encontrar projetos, pesquisadores, "
                f"laboratórios e publicações da Universidade Federal de Goiás.\n\n"
                f"Por favor, informe o tema ou a palavra-chave que você está buscando."
            ) if st.session_state.lang == "pt" else (
                "Hello! Welcome to the **UFG Answers Assistant**. 😊\n\n"
                "I'm here to help you find projects, researchers, labs and publications from UFG.\n\n"
                "Please share the topic or keyword you are looking for."
            ) if st.session_state.lang == "en" else (
                "¡Hola! Bienvenido(a) al **Asistente UFG Responde**. 😊\n\n"
                "Estoy aquí para ayudarle a encontrar proyectos, investigadores, "
                "laboratorios y publicaciones de la UFG.\n\n"
                "Por favor, indíqueme el tema o la palabra clave que está buscando."
            ),
            "time": datetime.datetime.now().strftime("%H:%M")
        }]

    # Renderiza o painel como HTML puro (cabeçalho + bolhas)
    header_html = f"""
    <div class="chat-overlay" onclick=""></div>
    <div class="chat-panel">
        <div class="chat-panel-header">
            <div style="display:flex;align-items:center;">
                <div class="chat-avatar">🤖</div>
                <div>
                    <h3>{t('chat_panel_title')}</h3>
                    <p>{t('chat_panel_subtitle')}</p>
                </div>
            </div>
        </div>
        <div class="chat-messages" id="chat-messages">
    """

    bubbles_html = ""
    for msg in st.session_state.messages:
        css_class = "bot" if msg["role"] == "assistant" else "user"
        time_str = msg.get("time", "")
        content = msg["content"].replace("\n", "<br>")
        # Formata link de e-mail se presente
        if "contact_email" in msg:
            mailto = f"mailto:{msg['contact_email']}"
            content += f'<br><br><a href="{mailto}" style="background:#4D9933;color:white!important;padding:7px 16px;border-radius:8px;text-decoration:none;font-weight:700;font-size:12px;">{t("send_email")}</a>'
        bubbles_html += f"""
        <div style="display:flex;flex-direction:column;align-items:{'flex-start' if css_class=='bot' else 'flex-end'}">
            <div class="chat-bubble {css_class}">{content}</div>
            <span class="chat-timestamp">{time_str}</span>
        </div>
        """

    footer_html = """
        </div>
    </div>
    <script>
        var msgs = document.getElementById('chat-messages');
        if (msgs) msgs.scrollTop = msgs.scrollHeight;
    </script>
    """

    st.markdown(header_html + bubbles_html + footer_html, unsafe_allow_html=True)

    # Input e botão fechar em colunas Streamlit normais
    col_inp, col_close = st.columns([5, 1])
    with col_inp:
        user_input = st.chat_input(t("chatbot_input"), key="chat_side_input")
    with col_close:
        if st.button(t("chat_btn_close"), key="close_chat"):
            st.session_state.chat_open = False
            st.rerun()

    # Processa a mensagem do usuário
    if user_input:
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": now
        })

        prompt_words = re.findall(r'\w+', user_input.lower())
        matched_row = None
        for idx, row in df.iterrows():
            texto = (str(row.get('resumo','')) + " " + str(row.get('titulo_projeto',''))).lower()
            if any(len(w) > 3 and w in texto for w in prompt_words):
                matched_row = row
                break

        if matched_row is not None:
            if st.session_state.lang == "pt":
                resposta = (
                    f"Que ótimo! Encontrei uma correspondência para o tema informado. 🎉\n\n"
                    f"📋 **Projeto:** {matched_row['titulo_projeto']}\n\n"
                    f"📍 **Unidade:** {matched_row['unidade_coordenador_projeto']}\n\n"
                    f"👤 **Coordenador(a):** {matched_row['nome_pesquisador']}\n\n"
                    f"📧 **E-mail de contato:** {matched_row['email']}\n\n"
                    f"Caso deseje entrar em contato, clique no botão abaixo. Posso ajudá-lo(a) com mais alguma informação?"
                )
            elif st.session_state.lang == "en":
                resposta = (
                    f"Great news! I found a match for the topic you provided. 🎉\n\n"
                    f"📋 **Project:** {matched_row['titulo_projeto']}\n\n"
                    f"📍 **Unit:** {matched_row['unidade_coordenador_projeto']}\n\n"
                    f"👤 **Coordinator:** {matched_row['nome_pesquisador']}\n\n"
                    f"📧 **Contact e-mail:** {matched_row['email']}\n\n"
                    f"Please click the button below to get in touch. Is there anything else I can help you with?"
                )
            else:
                resposta = (
                    f"¡Excelente! Encontré una coincidencia para el tema indicado. 🎉\n\n"
                    f"📋 **Proyecto:** {matched_row['titulo_projeto']}\n\n"
                    f"📍 **Unidad:** {matched_row['unidade_coordenador_projeto']}\n\n"
                    f"👤 **Coordinador(a):** {matched_row['nome_pesquisador']}\n\n"
                    f"📧 **E-mail de contacto:** {matched_row['email']}\n\n"
                    f"Si desea ponerse en contacto, haga clic en el botón. ¿Puedo ayudarle con algo más?"
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": resposta,
                "contact_email": matched_row['email'],
                "time": now
            })
        else:
            if st.session_state.lang == "pt":
                resposta = (
                    "Peço desculpas, mas não encontrei resultados para o termo informado na nossa base de dados. 😔\n\n"
                    "Poderia, por gentileza, tentar descrever o tema com outras palavras-chave? "
                    "Estou à disposição para ajudá-lo(a)!"
                )
            elif st.session_state.lang == "en":
                resposta = (
                    "I apologize, but I couldn't find any results for that term in our database. 😔\n\n"
                    "Could you please try describing the topic with different keywords? "
                    "I'm here to help!"
                )
            else:
                resposta = (
                    "Lo siento, no encontré resultados para el término indicado en nuestra base de datos. 😔\n\n"
                    "¿Podría intentar describir el tema con otras palabras clave? "
                    "Estoy aquí para ayudarle."
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": resposta,
                "time": now
            })

        st.rerun()
