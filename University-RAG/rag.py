"""
rag.py

Retrieval Augmented Generation Pipeline

Uses:
- FAISS
- HuggingFace Embeddings
- Ollama Llama 3.2
"""


from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_ollama import ChatOllama

from langchain_core.prompts import ChatPromptTemplate


from config import (
    VECTOR_DB,
    EMBEDDING_MODEL,
    OLLAMA_MODEL,
    TOP_K_RESULTS,
    MINIMUM_SCORE
)



#################################################
# Load Embeddings
#################################################

print("Loading embedding model...")


embeddings = HuggingFaceEmbeddings(

    model_name=EMBEDDING_MODEL

)



#################################################
# Load FAISS
#################################################

print("Loading FAISS database...")


vector_db = FAISS.load_local(

    VECTOR_DB,

    embeddings,

    allow_dangerous_deserialization=True

)



#################################################
# Load Local LLM
#################################################

print("Loading Ollama model...")


llm = ChatOllama(

    model=OLLAMA_MODEL,

    temperature=0

)



#################################################
# Prompt
#################################################

prompt = ChatPromptTemplate.from_template(
"""
You are a University Information Assistant.

Answer ONLY using the provided context.

Rules:
- Do not use outside knowledge.
- Do not guess.
- If the question asks for a list, include all matching items from the context.
- For campus/location questions, include campus name and complete address.
- Preserve addresses exactly as written.
- If information is missing, say:
"I could not find this information in the university resources."

Context:

{context}


Question:

{question}


Answer:

"""
)


#################################################
# Retrieve Documents
#################################################
def retrieve_documents(question):


    results = []


    # Semantic retrieval

    semantic_results = vector_db.similarity_search_with_score(
        question,
        k=15
    )


    for doc, score in semantic_results:

        results.append(
            {
                "doc": doc,
                "score": score
            }
        )



    # Exact keyword search

    keywords = question.lower().split()



    all_docs = vector_db.docstore._dict.values()



    for doc in all_docs:

        text = doc.page_content.lower()


        matches = sum(

            1 for word in keywords

            if word in text

        )


        if matches >= 2:

            results.append(

                {
                    "doc": doc,
                    "score": 0.0
                }

            )



    # Remove duplicates

    unique = {}


    for item in results:

        key = (

            item["doc"].metadata.get("source"),

            item["doc"].page_content[:100]

        )


        unique[key] = item["doc"]



    final_results = []


    for doc in unique.values():


        # PDF priority

        if doc.metadata.get("type") == "PDF":

            priority_score = -1

        else:

            priority_score = 1



        final_results.append(

            (
                doc,
                priority_score

            )

        )



    return final_results[:10]

#################################################
# Format Sources
#################################################

def format_source(metadata):


    source = metadata.get(

        "source",

        "Unknown"

    )


    page = metadata.get(

        "page",

        None

    )


    doc_type = metadata.get(

        "type",

        ""

    )


    if page:


        return (

            f"{source} "

            f"(Page {page})"

        )


    return source



#################################################
# Ask Question
#################################################

def ask_question(question):


    documents = retrieve_documents(question)


    if not documents:

        return {

            "answer":
            "No relevant information found.",

            "sources": []

        }



    context = ""

    sources = []



    selected_documents = []



    # ------------------------------------------------
    # 1. Prefer PDF documents
    # ------------------------------------------------

    for doc, score in documents:

        if doc.metadata.get("type") == "PDF":
            score = score - 50

            selected_documents.append(doc)



    # ------------------------------------------------
    # 2. Add other documents if needed
    # ------------------------------------------------

    for doc, score in documents:

        if doc not in selected_documents:

            selected_documents.append(doc)



    # ------------------------------------------------
    # 3. Limit context size
    # For testing, keep top 3
    # ------------------------------------------------

    selected_documents = selected_documents[:3]



    if not selected_documents:

        return {

            "answer":
            "I could not find reliable information in the university resources.",

            "sources": []

        }



    # ------------------------------------------------
    # 4. Build context and sources
    # ------------------------------------------------

    for doc in selected_documents:


        source_name = doc.metadata.get(
            "source",
            "Unknown"
        )


        context += (

            "\n\nSOURCE: "

            + str(source_name)

            + "\n"

            + doc.page_content

        )



        source = format_source(
            doc.metadata
        )


        if source not in sources:

            sources.append(source)



    # Debug

    print("\n========== CONTEXT SENT TO LLM ==========")

    print(context)

    print("==========================================\n")



    # ------------------------------------------------
    # 5. Create strict RAG prompt
    # ------------------------------------------------

    formatted_prompt = prompt.format(

        context=context,

        question=question

    )



    print("\n========== PROMPT SENT TO LLM ==========")

    print(formatted_prompt)

    print("=========================================\n")



    # ------------------------------------------------
    # 6. Generate answer
    # ------------------------------------------------

    response = llm.invoke(

        formatted_prompt

    )



    answer = response.content



    return {


        "answer":

        answer,


        "sources":

        sources

    }


#################################################
# Test
#################################################

if __name__ == "__main__":


    while True:


        question = input(

            "\nAsk question (exit to quit): "

        )


        if question.lower() == "exit":

            break



        result = ask_question(

            question

        )


        print("\nANSWER")

        print("----------------")

        print(

            result["answer"]

        )


        print("\nSOURCES")

        print("----------------")


        for source in result["sources"]:

            print(source)