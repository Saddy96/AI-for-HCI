from loaders import load_documents

documents = load_documents()

print()

for doc in documents:

    print("----------------------------------")
    print(doc.doc_type)
    print(doc.source)
    print(len(doc.text))