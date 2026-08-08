from pypdf import PdfReader

pdf = "data/DIGS - Collective Flyer 2025.pdf"

reader = PdfReader(pdf)

for i, page in enumerate(reader.pages):

    text = page.extract_text()

    print("PAGE:", i+1)

    print(text[:500])

    print("----------------")