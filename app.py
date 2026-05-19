import streamlit as st
import pandas as pd
import unicodedata
import re

# ==========================================
# Configurações Iniciais e CSS (Tarefas 1 e 2)
# ==========================================
st.set_page_config(page_title="UFG Responde", layout="wide")

st.markdown("""
<style>
/* Tarefa 1: Identidade Visual e Cores */
:root {
    --primary-navy: #0A2A56;
    --vibrant-green: #4D9933;
    --cyan-pool: #00A1C9;
    --bg-light: #F8F9FA;
}

.stApp {
    background-color: var(--bg-light);
}

/* Headers e Textos */
h1, h2, h3 { color: var(--primary-navy) !important; font-family: sans-serif; }
h4, h5, h6 { color: var(--vibrant-green) !important; font-family: sans-serif; }
a { color: var(--cyan-pool) !important; }

/* Botões Principais */
.stButton > button {
    background-color: var(--primary-navy);
    color: white;
    border: none;
}
.stButton > button:hover {
    background-color: var(--vibrant-green);
    color: white;
    border: none;
}

/* Tarefa 2: Barra de Acessibilidade (Fidelidade ao Print) */
.gov-accessibility-bar {
    background-color: #f2f2f2;
    padding: 5px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    border-bottom: 1px solid #ddd;
    font-family: Arial, sans-serif;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
}
.gov-links a {
    margin-right: 15px;
    color: #333;
    text-decoration: none;
}
.gov-links a:hover {
    text-decoration: underline;
}
.gov-controls {
    display: flex;
    align-items: center;
    gap: 15px;
}
.gov-controls span, .gov-controls div {
    display: flex;
    align-items: center;
    cursor: pointer;
}
.gov-controls-btn {
    background: #e0e0e0;
    padding: 2px 6px;
    border-radius: 3px;
    font-weight: bold;
    color: #333;
}
.gov-controls-btn:hover {
    background: #d0d0d0;
}
.info-icon {
    background: #FFD700;
    color: black;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 14px;
}
.contrast-icon {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: linear-gradient(90deg, black 50%, white 50%);
    border: 1px solid black;
}

/* Espaçamento para o main container não ficar sob a barra absolute */
.block-container {
    padding-top: 5rem !important;
}

/* Botão de E-mail destacado */
.email-btn > button {
    background-color: var(--vibrant-green);
    font-weight: bold;
}
.email-btn > button:hover {
    background-color: var(--primary-navy);
}
</style>
""", unsafe_allow_html=True)

# Inserindo Barra de Acessibilidade
st.markdown("""
<div class="gov-accessibility-bar">
    <div class="gov-links">
        <a href="#conteudo">Ir para o conteúdo [1]</a>
        <a href="#menu">Ir para o menu [2]</a>
        <a href="#busca">Ir para busca [3]</a>
    </div>
    <div class="gov-controls">
        <span class="info-icon" title="Acesso à Informação">i</span>
        <span><img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Brazil.svg" width="16" style="margin-right:4px;"> Português (Brasil) ∨</span>
        <span class="gov-controls-btn">A+</span>
        <span class="gov-controls-btn">A-</span>
        <span class="contrast-icon" title="Alto Contraste"></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Inserindo Widget do VLibras (Tarefa 2)
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
# Tarefa 1 (Logos) e Tarefa 3 (Textos Iniciais)
# ==========================================
st.markdown("<div id='conteudo'></div>", unsafe_allow_html=True)

col_logo1, col_space, col_logo2 = st.columns([1, 2, 1])
with col_logo1:
    # Usando imagem local baseada nos arquivos encontrados, ou placeholder se falhar
    try:
        st.image("UFG.png", width=150)
    except:
        st.info("[Placeholder: Logo UFG]")
with col_logo2:
    try:
        st.image("UFG_RESPONDE.jpeg", width=150)
    except:
        st.info("[Placeholder: Logo UFG_RESPONDE]")

st.markdown("<h4 style='text-align: center;'>Vamos colocar em prática a missão da UFG</h4>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Você pergunta, UFG RESPONDE</h1>", unsafe_allow_html=True)


# ==========================================
# Tarefa 4: Importação e Tratamento dos Dados
# ==========================================
@st.cache_data
def load_and_augment_data():
    # Criação de conjunto de dados fictícios (mockados)
    dados = {
        "nome_pesquisador": ["João da Silva", "Maria Oliveira", "Carlos Santos", "Ana Souza", "Fernanda Lima"],
        "unidade_coordenador_projeto": ["Instituto de Informática", "Escola de Agronomia", "Instituto de Química", "", "Faculdade de Medicina"],
        "titulo_projeto": ["Inteligência Artificial na Saúde", "Manejo de Solo Sustentável", "Novos Materiais de Carbono", "Estudos Sociais", "Tratamento de Água"],
        "resumo": ["Uso de IA para diagnósticos precisos", "Análise de solo e água para agricultura", "Materiais inovadores com base em carbono", "Impactos culturais na sociedade moderna", "Purificação de água com baixo custo"],
        "status": ["Em Andamento", "Concluído", "Em Andamento", "Em Andamento", "Concluído"],
        "grande_area": ["Ciências Exatas e da Terra", "Ciências Agrárias", "Ciências Exatas e da Terra", "Ciências Humanas", "Ciências da Saúde"],
        "publicacoes": ["Artigo IEEE 2023", "Revista Agro 2022", "Nature Materials 2023", "Revista Sociedade 2021", "Health & Water 2023"]
    }
    df = pd.DataFrame(dados)
    
    # Geração Automática de E-mail
    def generate_email(nome):
        # Letras minúsculas, sem espaços ou acentos
        nfkd_form = unicodedata.normalize('NFKD', nome)
        clean_name = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        clean_name = clean_name.lower().replace(" ", "_")
        return f"{clean_name}@ufg.br"
        
    df['email'] = df['nome_pesquisador'].apply(generate_email)
    
    # Mapeamento de Laboratório Físico
    lab_map = {
        "Instituto de Informática": "Laboratório de Inteligência Artificial",
        "Escola de Agronomia": "Laboratório de Análise de Solos",
        "Instituto de Química": "Laboratório de Química de Materiais",
        "Faculdade de Medicina": "Laboratório de Saúde Pública"
    }
    # Caso campo esteja vazio ou não mapeado, atribui lab padrão
    df['laboratorio'] = df['unidade_coordenador_projeto'].map(lab_map).fillna("Laboratório Central Padrão")
    
    return df

df = load_and_augment_data()


# ==========================================
# Tarefa 5: Mecanismo de Busca e Filtros
# ==========================================
st.markdown("<div id='busca'></div>", unsafe_allow_html=True)
st.markdown("### Busca de Projetos e Pesquisadores")

search_query = st.text_input("🔍 Digite uma palavra-chave (ex: água, solo, carbono, saúde)")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    f_area = st.selectbox("Grande Área", options=["Todas"] + list(df['grande_area'].unique()))
with col_f2:
    f_status = st.selectbox("Status do Projeto", options=["Todos"] + list(df['status'].unique()))
with col_f3:
    f_unidade = st.selectbox("Unidade", options=["Todas"] + list(df['unidade_coordenador_projeto'].unique()))

# Lógica de Filtragem
filtered_df = df.copy()

if search_query:
    # Busca global simples convertendo a linha para string e ignorando case
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

if f_area != "Todas":
    filtered_df = filtered_df[filtered_df['grande_area'] == f_area]
if f_status != "Todos":
    filtered_df = filtered_df[filtered_df['status'] == f_status]
if f_unidade != "Todas":
    filtered_df = filtered_df[filtered_df['unidade_coordenador_projeto'] == f_unidade]

st.markdown("#### Resultados")
tab1, tab2, tab3, tab4 = st.tabs(["👤 Pesquisador", "📄 Projeto", "🔬 Laboratório", "📚 Publicações"])

with tab1:
    st.dataframe(filtered_df[['nome_pesquisador', 'email']], use_container_width=True, hide_index=True)
with tab2:
    st.dataframe(filtered_df[['titulo_projeto', 'resumo', 'status']], use_container_width=True, hide_index=True)
with tab3:
    st.dataframe(filtered_df[['unidade_coordenador_projeto', 'laboratorio']], use_container_width=True, hide_index=True)
with tab4:
    st.dataframe(filtered_df[['titulo_projeto', 'publicacoes']], use_container_width=True, hide_index=True)

st.divider()

# ==========================================
# Tarefa 6: Chatbot Interativo de Triagem
# ==========================================
st.markdown("### 💬 Assistente Virtual UFG RESPONDE")
st.caption("Converse comigo para encontrar a informação que você precisa!")

# Inicializa histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o assistente de triagem. Diga-me qual assunto você procura (ex: 'Preciso de ajuda com análise de solo' ou 'Queria saber sobre carbono')"}
    ]

# Renderiza histórico de mensagens
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Se a mensagem tiver email associado, exibe botão de ação
        if "contact_email" in msg:
            st.markdown(f'<div class="email-btn">', unsafe_allow_html=True)
            st.button("✉️ Enviar E-mail de Contato", key=f"btn_hist_{i}")
            st.markdown('</div>', unsafe_allow_html=True)

# Input do usuário
if prompt := st.chat_input("Digite sua pergunta ou tema..."):
    # Adiciona pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Lógica simples de identificação de assunto cruzando palavras do prompt com resumo/título
    prompt_words = re.findall(r'\w+', prompt.lower())
    matched_row = None
    
    for idx, row in df.iterrows():
        # Verifica se alguma palavra-chave (com mais de 3 letras) do usuário está no texto do projeto
        texto_projeto = (str(row['resumo']) + " " + str(row['titulo_projeto'])).lower()
        if any(len(word) > 3 and word in texto_projeto for word in prompt_words):
            matched_row = row
            break
            
    if matched_row is not None:
        resposta = (f"Encontrei algo! Para esse tema, você pode procurar o **{matched_row['laboratorio']}**. "
                    f"O pesquisador responsável é **{matched_row['nome_pesquisador']}** e o e-mail de contato gerado é **{matched_row['email']}**.")
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": resposta,
            "contact_email": matched_row['email']
        })
        
        with st.chat_message("assistant"):
            st.markdown(resposta)
            st.markdown(f'<div class="email-btn">', unsafe_allow_html=True)
            st.button("✉️ Enviar E-mail de Contato", key=f"btn_new_{len(st.session_state.messages)}")
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        resposta = "Não encontrei um laboratório ou pesquisador exatamente com esse termo na nossa base de dados atual. Poderia tentar descrever usando outras palavras-chave?"
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)
