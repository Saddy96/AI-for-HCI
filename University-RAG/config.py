"""
config.py

Central configuration for University RAG system
"""


# -----------------------------
# Data
# -----------------------------

PDF_FOLDER = "data"

VECTOR_DB = "db"



# -----------------------------
# Embeddings
# -----------------------------

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)



# -----------------------------
# Local LLM
# -----------------------------

OLLAMA_MODEL = "llama3.2:3b"



# -----------------------------
# Chunking
# -----------------------------

CHUNK_SIZE = 400

CHUNK_OVERLAP = 100



# -----------------------------
# Retrieval
# -----------------------------

TOP_K_RESULTS = 10


# Minimum similarity score

MINIMUM_SCORE = 1.0


# -----------------------------
# Application
# -----------------------------

APP_TITLE = (
    "University Information Assistant"
)


APP_DESCRIPTION = """

A Retrieval-Augmented Generation chatbot
that answers questions using official
university documents and webpages.

"""

# -----------------------------
# Web Requests
# -----------------------------

REQUEST_TIMEOUT = 30