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
.gov-lang-btn {
    background: var(--cyan-pool);
    padding: 3px 10px;
    border-radius: 4px;
    font-weight: 700;
    color: white;
    font-size: 11px;
    border: none;
    cursor: pointer;
}
.gov-lang-btn:hover {
    background: var(--vibrant-green);
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
# Chatbot Interativo
# ==========================================
st.markdown(f"### {t('chatbot_title')}")
st.caption(t("chatbot_caption"))

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": t("chatbot_welcome")}
    ]

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "contact_email" in msg:
            mailto = f"mailto:{msg['contact_email']}"
            st.markdown(f"""<a href="{mailto}" target="_blank" style="
                display: inline-block;
                background-color: #4D9933;
                color: white !important;
                padding: 8px 20px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 8px;
            ">{t('send_email')}</a>""", unsafe_allow_html=True)

if prompt := st.chat_input(t("chatbot_input")):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_words = re.findall(r'\w+', prompt.lower())
    matched_row = None

    for idx, row in df.iterrows():
        texto_projeto = (str(row['resumo']) + " " + str(row['titulo_projeto'])).lower()
        if any(len(word) > 3 and word in texto_projeto for word in prompt_words):
            matched_row = row
            break

    if matched_row is not None:
        resposta = t("chatbot_found").format(
            proj=matched_row['titulo_projeto'],
            unit=matched_row['unidade_coordenador_projeto'],
            coord=matched_row['nome_pesquisador'],
            email=matched_row['email']
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": resposta,
            "contact_email": matched_row['email']
        })

        with st.chat_message("assistant"):
            st.markdown(resposta)
            mailto = f"mailto:{matched_row['email']}"
            st.markdown(f"""<a href="{mailto}" target="_blank" style="
                display: inline-block;
                background-color: #4D9933;
                color: white !important;
                padding: 8px 20px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 8px;
            ">{t('send_email')}</a>""", unsafe_allow_html=True)
    else:
        resposta = t("chatbot_not_found")
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)
