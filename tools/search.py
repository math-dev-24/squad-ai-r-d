from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI

def search_documents(index: FAISS, query: str, top_k: int = 5) -> list[tuple[Document, float]]:
    """
    :param index: FAISS index
    :param query: query to search
    :param top_k: number of documents to return
    :return: list of documents
    """
    return index.similarity_search_with_score(query, top_k=top_k)


def estimate_category(query: str, categories: list[str]) -> list[str]:
    """
    Ask the LLM to estimate the category of query
    :param query: query to search
    :param categories: list categories available
    :return: list of categories
    """

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    requests: list[BaseMessage] = [
        SystemMessage(role="system", content="Tu as un rôle très précis est important! Tu as un query et une liste de catégories à ta disposition. Tu dois répondre uniquement avec une liste de catégories séparer par une virgule, pas d'autres informations."),
        HumanMessage(role="user", content=f"Query: {query}"),
        AIMessage(role="assistant", content=f"Categories à ta disposition: {categories}")
    ]

    response = llm.invoke(requests)
    return response.content.split(",")