"""
loaders.py

Loads university documents from:

1. PDFs
2. Official university webpages
"""

import os
import re
import requests

from bs4 import BeautifulSoup
from pypdf import PdfReader

from config import *
from urls import URLS


class Document:

    def __init__(
        self,
        text,
        source,
        doc_type,
        page=None
    ):

        self.text = text
        self.source = source
        self.doc_type = doc_type
        self.page = page


#########################################################
# Clean text
#########################################################

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    text = text.replace("\x00", "")

    return text.strip()


#########################################################
# Read one PDF
#########################################################

def read_pdf(pdf_path):

    documents = []

    reader = PdfReader(pdf_path)


    for page_number, page in enumerate(reader.pages):

        page_text = page.extract_text()


        if page_text:

            documents.append(

                {
                    "text": clean_text(page_text),

                    "page": page_number + 1

                }

            )


    return documents


#########################################################
# Load all PDFs
#########################################################

def load_pdfs():

    documents = []

    if not os.path.exists(PDF_FOLDER):

        print("PDF folder not found.")

        return documents


    for filename in os.listdir(PDF_FOLDER):

        if filename.lower().endswith(".pdf"):

            path = os.path.join(
                PDF_FOLDER,
                filename
            )

            print(f"Loading PDF: {filename}")


            pages = read_pdf(path)


            for page in pages:

                if len(page["text"]) > 100:


                    documents.append(

                        Document(

                            text=page["text"],

                            source=filename,

                            doc_type="PDF",

                            page=page["page"]

                        )

                    )


    return documents


#########################################################
# Download webpage
#########################################################

def download_page(url):

    try:

        response = requests.get(

            url,

            timeout=REQUEST_TIMEOUT,

            headers={

                "User-Agent":

                "Mozilla/5.0"

            }

        )

        response.raise_for_status()

        return response.text

    except Exception as e:

        print(f"Could not download {url}")

        print(e)

        return ""

#########################################################
# Extract webpage text
#########################################################

def html_to_text(html):

    soup = BeautifulSoup(html, "lxml")

    for tag in soup(

        [

            "script",

            "style",

            "header",

            "footer",

            "nav",

            "noscript",

            "svg"

        ]

    ):

        tag.decompose()

    text = soup.get_text(separator="\n")

    return clean_text(text)


#########################################################
# Load all webpages
#########################################################

def load_websites():

    documents = []

    for url in URLS:

        print(f"Loading Website: {url}")

        html = download_page(url)

        if html == "":

            continue

        text = html_to_text(html)

        if len(text) > 100:

            documents.append(

                Document(

                    text=text,

                    source=url,

                    doc_type="Website"

                )

            )

    return documents


#########################################################
# Load Everything
#########################################################

def load_documents():

    pdfs = load_pdfs()

    websites = load_websites()

    documents = pdfs + websites

    print()

    print("-----------------------------------")

    print(f"PDF Documents: {len(pdfs)}")

    print(f"Website Documents: {len(websites)}")

    print(f"Total Documents: {len(documents)}")

    print("-----------------------------------")

    return documents