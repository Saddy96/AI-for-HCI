from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import *


embedding = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


db = FAISS.load_local(
    VECTOR_DB,
    embedding,
    allow_dangerous_deserialization=True
)


results = db.similarity_search(
    "campus address",
    k=3
)


for r in results:

    print("--------------------")

    print(r.metadata)

    print(r.page_content[:300])