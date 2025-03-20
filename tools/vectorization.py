import os
from dotenv import load_dotenv
import pandas as pd
import fitz
import pickle
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAI


load_dotenv()
VECTOR_PATH: str = "./../vectors/"
LLM = OpenAI(model="text-embedding-3-large")
EMBEDDING_MODEL = OpenAIEmbeddings()


def load_pdf_text(file_path: str) -> str:
    """
    :param file_path: path to the pdf file
    :return: content from the pdf file
    """
    doc = fitz.open(file_path)
    content = ""
    for page in doc:
        content += page.get_text()
    return content


def load_xlsx_text(file_path: str) -> str:
    """
    :param file_path: path to the xlsx file
    :return: content from the xlsx file
    """
    content = ""
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        content += row["text"] + "\n"
    return content


def load_files_by_category(category: dict[str,str]) -> dict[str, list[str]]:
    """
    :param category: list des catégories
    :return: list all category with all files
    """
    doc_by_category: dict[str, list[str]] = {}

    for category_name, category_path in category.items():
        documents: list[str] = []
        for root, _, files in os.walk(category_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Fichier trouvé : {file_path}")

                if file_path.endswith(".txt"):
                    with open(file_path, "r") as f:
                        documents.append(f.read())

                elif file_path.endswith(".pdf"):
                    documents.append(load_pdf_text(file_path))

                elif file_path.endswith(".xlsx"):
                    documents.append(load_xlsx_text(file_path))

        doc_by_category[category_name] = documents
    return doc_by_category


def vectorize_category(category_name: str, documents: list[str]) -> None:
    """
    :param category_name: name of the category
    :param documents: list of documents
    :return: None
    """
    print(f"Vectorizing {category_name} documents...")
    index_path = f"{VECTOR_PATH}{category_name}_index.faiss"
    metadata_path = f"{VECTOR_PATH}{category_name}_metadata.pkl"

    index = FAISS.from_texts(documents, EMBEDDING_MODEL)
    index.save_local(index_path)

    with open(metadata_path, "wb") as f:
        pickle.dump(documents, f)
    print(f"{category_name} vectorized successfully!")



def main_vectorization(category: list[str]) -> None:
    """
    :param category: list of categories
    :return: None
    """

    categories: dict[str, str] = {}

    for category_name in category:
        categories[category_name] = f"../../sources/{category_name}/"

    # load documents by category
    all_documents = load_files_by_category(categories)

    # vectorize documents by category
    for name_category, documents_list in all_documents.items():
        if len(documents_list) > 0:
            vectorize_category(name_category, documents_list)



def load_index(category_name: str) -> tuple[FAISS, list[str]]:
    """
    :param category_name: name of the category
    :return: FAISS index and list of documents
    """
    index_path = f"./vectors/{category_name}_index.faiss"
    metadata_path = f"./vectors/{category_name}_metadata.pkl"

    index = FAISS.load_local(index_path, EMBEDDING_MODEL, allow_dangerous_deserialization=True)

    with open(metadata_path, "rb") as f:
        documents = pickle.load(f)
    return index, documents