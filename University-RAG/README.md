# University Information Assistant

A Retrieval-Augmented Generation (RAG) chatbot built using:

- LangChain
- Ollama
- Llama 3.2
- FAISS
- Sentence Transformers
- Gradio

## Features

- Reads university PDF documents
- Reads official university webpages
- Answers student questions
- Uses semantic search
- Displays source documents
- Runs completely offline (except when downloading webpages)

## Installation

Install Ollama

https://ollama.com

Download the model

ollama pull llama3.2:3b

Install Python packages

pip install -r requirements.txt

Build the vector database

python ingest.py

Run the chatbot

python app.py