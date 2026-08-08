from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import *


embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


db = FAISS.load_local(
    VECTOR_DB,
    embeddings,
    allow_dangerous_deserialization=True
)


results = db.similarity_search(
    "NORTHERN KENTUCKY Richard R. Knock Building 410 Meijer Drive Florence KY",
    k=10
)


for r in results:

    print("\n------------------------")

    print(r.metadata)

    print(r.page_content[:500])