# Assistant de Révision – Version Turbo

## Le concept de l’application 

**Assistant de Révision – Version Turbo** est une application web développée avec **Streamlit** qui permet d’interroger intelligemment un **cours au format PDF** grâce à une approche de type **RAG (Retrieval-Augmented Generation)**.

L’utilisateur dépose un PDF (cours, polycopié, support de formation), puis pose des questions en langage naturel.  
L’application :
1. lit et découpe le PDF,
2. transforme les morceaux de texte en vecteurs (embeddings),
3. stocke ces vecteurs dans une base de données vectorielle,
4. recherche les passages les plus pertinents pour chaque question,
5. génère une réponse contextualisée à l’aide d’un modèle de langage local via **Ollama**.

L'objectif est de **réviser plus vite, plus intelligemment, et sans dépendre d’API cloud payantes**.

---

## Concept technique (RAG simplifié)

Le fonctionnement repose sur trois briques principales :

1. **Indexation du cours**
   - Le PDF est découpé en morceaux (chunks).
   - Chaque chunk est transformé en vecteur sémantique (embedding).
   - Les vecteurs sont stockés dans une base FAISS.

2. **Recherche sémantique**
   - Lorsqu’une question est posée, l’application recherche les chunks les plus proches sémantiquement.

3. **Génération de la réponse**
   - Les passages retrouvés sont injectés dans un prompt.
   - Un modèle de langage (Mistral via Ollama) génère la réponse à partir de ce contexte.

---

## Installation et exécution du projet en local 

Avant d’installer le projet, assurez-vous d’avoir :

- **Python 3.9+**
- **Ollama** installé et fonctionnel  
  https://ollama.com/

Via un terminal (par exemple, PowerShell), exécuter la commande suivante afin de lancer Ollama :

  ollama serve

Laisser la fenêtre précédente ouverte. Ouvrez une nouvelle fenêtre et exécuter le code ci-dessous afin de vérifier qu'Ollama est bien lancé :

  ollama list

Exécuter les deux codes qui suivent pour vérifier que les modèles sont bien installés : 

  ollama pull mistral
  
  ollama pull nomic-embed-text

---

## Projet

Ouvrez le projet avec VS Code. Via le terminal, faites :

  git clone https://github.com/Jehovahni177/Projet-IA-gen.git

Avant de lancer le projet, ouvrez un nouveau terminal depuis VS Code afin d'installer les bibliothèques nécessaires du fichier requirements. Faites :

  pip install -r requirements.txt
  
  pip install streamlit langchain langchain-community langchain-text-splitters langchain-ollama faiss-cpu pypdf

Lancer le projet en exécutant dans le terminal le code ci-après :

  python -m streamlit run app.py

Copiez l'adresse indiquée dans votre barre de recherche pour ouvrir l'application.

---

## Les choix techniques et les éventuelles limitations

## Choix techniques

   Streamlit

Interface rapide à développer,

Idéal pour les prototypes IA interactifs,

Gestion simple du session_state.

  
   LangChain

Orchestration du pipeline RAG,

Découplage clair entre chargement, découpage, recherche et génération.

  
   Ollama (LLM local)

Pas d’API externe → confidentialité totale,

Exécution en local (CPU ou GPU),

Modèle Mistral choisi pour son bon compromis intelligence / vitesse.

  
   FAISS

Base vectorielle rapide et locale,

Parfait pour des volumes de documents modérés (cours, polycopiés).

  
   Chunking (1000 / 200)

Taille suffisante pour conserver du contexte,

Overlap pour éviter les ruptures sémantiques.


## Eventuelles limitations

Pas de persistance disque du vectorstore (rechargement à chaque redémarrage),

Pas de gestion multi-PDF ou multi-utilisateur,

Performances dépendantes de la machine (CPU/RAM),

Pas de citations précises ligne/paragraphe (uniquement du contexte global),


PDF scannés (images) non supportés sans OCR.



