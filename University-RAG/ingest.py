"""
ingest.py

Creates FAISS vector database
from university PDFs and websites.
"""


from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document


from loaders import load_documents

from config import (
    EMBEDDING_MODEL,
    VECTOR_DB,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)



#################################################
# Convert Loader Documents
#################################################

def convert_documents(raw_documents):

    documents = []


    for doc in raw_documents:


        print("\n----------------")

        print("SOURCE:", doc.source)

        print("TYPE:", doc.doc_type)

        print("PAGE:", doc.page)

        print("TEXT LENGTH:", len(doc.text))

        print(doc.text[:200])



        metadata = {

            "source": doc.source,

            "type": doc.doc_type,

            "page": doc.page

        }


        documents.append(

            Document(

                page_content=doc.text,

                metadata=metadata

            )

        )


    return documents


#################################################
# Split Documents
#################################################

def split_documents(documents):


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP,

        separators=[

            "\n\n",

            "\n",

            ".",

            " "

        ]

    )


    chunks = splitter.split_documents(

        documents

    )


    return chunks



#################################################
# Create FAISS
#################################################

def create_database(chunks):


    print()

    print("Loading embedding model...")


    embeddings = HuggingFaceEmbeddings(

        model_name=EMBEDDING_MODEL

    )


    print("Creating vector database...")


    database = FAISS.from_documents(

        chunks,

        embeddings

    )


    database.save_local(

        VECTOR_DB

    )


    return database



#################################################
# Main
#################################################

def main():


    print("="*60)

    print("University RAG - Knowledge Base Builder")

    print("="*60)



    #
    # Load data
    #

    raw_documents = load_documents()



    print()

    print(

        f"Documents loaded: {len(raw_documents)}"

    )



    #
    # Convert format
    #

    documents = convert_documents(

        raw_documents

    )



    #
    # Split
    #

    print()

    print("Splitting documents...")


    chunks = split_documents(

        documents

    )


    print(

        f"Chunks created: {len(chunks)}"

    )



    #
    # Create database
    #

    create_database(

        chunks

    )



    print()

    print("="*60)

    print("FAISS database created successfully")

    print("="*60)



if __name__ == "__main__":

    main()