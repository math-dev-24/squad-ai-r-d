import time
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from tools.vectorization import load_index
from tools.search import search_documents, estimate_category
from dotenv import load_dotenv

load_dotenv()
LIST_CATEGORIES: list[str] = ["compressor", "regulation", "maintenance"]


if __name__ == "__main__":
    time_start = time.time()

    query = "Sur les compresseur à vis, c'est quoi le VI variable ? détails moi le max que tu peux"

    categories_estimation = estimate_category(query, LIST_CATEGORIES)

    time_int_1 = time.time()
    print(f"Estimation de la catégorie: {categories_estimation}")

    text_for_request: str = ""

    for category in categories_estimation:
        if category.strip() not in LIST_CATEGORIES:
            continue

        index, documents = load_index(category)

        list_documents: list[tuple[Document, float]] = search_documents(index, query)
        best_document = sorted(list_documents, key=lambda x: x[1], reverse=True)[0]

        text_for_request += f"{category}-content: {best_document[0].page_content}\n\n"


    time_int_2 = time.time()
    print(f"Recherche des documents terminée en {time_int_2 - time_int_1} secondes")

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    requests: list[BaseMessage] = [
        SystemMessage(role="system", content="Tu es un super expert en système frigorifique, thermodynamique et énergétique (transfert d'énergie)."),
        HumanMessage(role="user", content=query),
        AIMessage(role="assistant", content=text_for_request)
    ]

    response = llm.invoke(requests)

    time_end = time.time()
    print(f"Recherche terminée en {time_end - time_start} secondes")
    print(response.content)


