import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

class Agent:
    def __init__(self, openai_api_key: str | None = None) -> None:
        # if openai_api_key is None, then it will look the enviroment variable OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        self.llm = ChatOpenAI(
            model_name='gpt-3.5-turbo-16k',
            temperature=0.7, 
            openai_api_key=openai_api_key,
            max_tokens=2000
        )

        self.chat_history = None
        self.chain = None
        self.db = None

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Your role is a senior English teacher who is specialized in teaching little students under 14 years old.Your task is to respond to students' inquiries on the unit: %s, using the dataset I have provided. Your task is to answer questions to trigger them to understand the core idea, development of ideas and suggestion to have inspiration for creativity.You should provide accurate and complete information ONLY IN the unit %s DO NOT USE INFORMATION OF OTHERS TOPIC and the specific question asked by the student. Your response should be concise with fun tone. If student asks out of the topic, you should redirect with questions to make sure that student understands unit: %s  and meet the responsibility you were given."
        else:
            response = self.chain({"question": question, "chat_history": self.chat_history})
            response = response["answer"].strip()
            self.chat_history.append((question, response))
        return response

    def ingest(self, file_path: os.PathLike) -> None:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        splitted_documents = self.text_splitter.split_documents(documents)

        if self.db is None:
            self.db = FAISS.from_documents(splitted_documents, self.embeddings)
            self.chain = ConversationalRetrievalChain.from_llm(self.llm, self.db.as_retriever())
            self.chat_history = []
        else:
            self.db.add_documents(splitted_documents)

    def forget(self) -> None:
        self.db = None
        self.chain = None
        self.chat_history = None
