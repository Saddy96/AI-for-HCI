from loaders import load_pdfs


documents = load_pdfs()


for doc in documents:

    print("\n====================")
    print("SOURCE:", doc.source)
    print("PAGE:", doc.page)

    text = doc.text.upper()

    if "KENTUCKY" in text or "NORTHERN" in text:

        print("FOUND KEYWORD")

        print(doc.text)

    else:

        print("No Kentucky found")