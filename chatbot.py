# chatbot.py

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

class ChatBot:
    def __init__(self):
        self.chat = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini"
        )

        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index("deepseek-r1-rag")

        self.vectorstore = PineconeVectorStore(
            index=index,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
            text_key="text"
        )

    def augment_prompt(self, query):
        results = self.vectorstore.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in results])

        return f"""
        Answer based on the context below:

        Context:
        {context}

        Question:
        {query}
        """

    def get_response(self, query):
        prompt = self.augment_prompt(query)
        response = self.chat.invoke(prompt)
        return response.content