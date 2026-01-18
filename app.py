import streamlit as st
import os
import tempfile

# --- CONFIGURATION ---
st.set_page_config(page_title="IA Étudiant", layout="wide")
st.title("⚡ Assistant de Révision (Version Turbo)")

# --- BLOC D'IMPORTATION ---

# On tente d'importer les briques LangChain nécessaires au chargement PDF, découpage, vectorisation et génération de réponses.
# Si une dépendance manque, on affiche une erreur et on arrête l’application pour éviter un crash.

try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_ollama import OllamaEmbeddings, ChatOllama
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError as e:
    st.error(f"❌ Erreur d'import : {e}")
    st.stop()

# --- SIDEBAR ---

# Crée une barre latérale (sidebar) pour les éléments de configuration et l’upload du PDF.

with st.sidebar:
    st.header("Ton Cours")
    uploaded_file = st.file_uploader("Dépose ton PDF ici", type="pdf")

# --- FONCTION DE TRAITEMENT (OPTIMISÉE) ---

# Cette fonction permet de :
# 1) Sauvegarder temporairement le PDF uploadé sur le disque (LangChain PyPDFLoader travaille avec un chemin fichier),
# 2) Charger le PDF en documents,
# 3) Découper ces documents en chunks,
# 4) Transformer chaque chunk en vecteurs (embeddings),
# 5) Indexer les vecteurs dans FAISS pour permettre une recherche par similarité,
# 6) Supprimer le fichier temporaire et renvoie le vectorstore.

def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()
    
    # Découpage
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # Mémoire : ON UTILISE LE MODÈLE RAPIDE ICI !
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    
    os.remove(tmp_path)
    return vectorstore

# --- INTERFACE ---

# Après avoir uploadé un fichier, on lance la phase d’indexation puis le chat.

if uploaded_file:
    # 1. Mémorisation
    if "vectorstore" not in st.session_state:
        with st.spinner("⚡ Lecture ultra-rapide du document..."):
            try:
                st.session_state.vectorstore = process_pdf(uploaded_file)
                st.success("✅ Cours mémorisé en un éclair !")
            except Exception as e:
                st.error(f"Erreur : {e}")

    # 2. Chat
    if "vectorstore" in st.session_state:
        question = st.chat_input("Pose ta question sur le cours...")
        
        if question:
            with st.chat_message("user"):
                st.write(question)
            
            with st.chat_message("assistant"):
                with st.spinner("Je réfléchis..."):
                    # Recherche
                    docs = st.session_state.vectorstore.similarity_search(question, k=3)
                    context = "\n\n".join([doc.page_content for doc in docs])
                    
                    # Prompt
                    template = """Tu es un assistant pédagogique. Utilise le contexte suivant pour répondre à la question.
                    
                    Contexte :
                    {context}

                    Question :
                    {question}
                    """
                    prompt = ChatPromptTemplate.from_template(template)
                    
                    # Réponse (On garde Mistral pour l'intelligence)
                    llm = ChatOllama(model="mistral")
                    chain = prompt | llm | StrOutputParser()
                    
                    response = chain.invoke({"context": context, "question": question})
                    st.write(response)

# Si aucun PDF n’a été uploadé, on affiche un message d’aide.

else:
    st.info("👆 Dépose ton PDF pour tester la vitesse.")