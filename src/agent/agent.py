import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import create_qa_with_sources_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.vectorstores import Chroma
from src.utils.redis_utils import get_key_redis, set_key_redis
import ujson
import json

class Agent:
    def __init__(self, openai_api_key: str | None = None) -> None:
        # if openai_api_key is None, then it will look the enviroment variable OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        self.llm = ChatOpenAI(
            model_name='gpt-3.5-turbo-16k',
            temperature=0.7,
            openai_api_key=openai_api_key,
            max_tokens=800
        )
        self.chain = None
        self.db = None
        self.chat_history = None

    def ask(self, topic: str, unit: str, question: str) -> str:
        prompt_define = """
            Only reply in English. 

            Your role is a senior English teacher who is specialized in teaching little students under 14 years old.

            Your task is to ask questions one by one based on {} to brainstorm with Student in order to trigger them to understand the core idea, development of ideas and suggestion to have inspiration and creativity to write {} into 300 words essay.
            The questions should have some replies matched with the previous answer from Student with fun voice tone.Please take note that you only ask one question at one time.\n
                
            You are chatting with the kid via the ChatGPT mobile app. This means most of the time your lines should be a sentence or two, unless the user's request requires reasoning or long-form outputs.
            You're required to simplify your answers for kids under 6 years old understand easily.

            If Student answers out of the topic, you should redirect with questions to make sure that Student understands {} and meet the responsibility you were given.
        """.format(
            topic + " " + unit,
            topic + " " + unit,
            topic + " " + unit,
        )
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        store_memory = []
        if question != "Get Started":
            store_memory = get_key_redis(
                key=f"memory:{topic.lower().replace(' ', '-')}:{unit.lower().replace(' ','-')}"
            )
            if store_memory:
                store_memory = ujson.loads(store_memory)
                for m in store_memory[:10]:
                    memory.save_context({"question": m[0]}, {"answer": m[1]})
            else:
                store_memory = []
        else:
            store_memory = []

        # prompt = PromptTemplate(
        #     input_variables=['chat_history'], template=prompt_define
        # )

        # qa_chain = create_qa_with_sources_chain(
        #     llm=self.llm, 
        # )
        # doc_prompt = PromptTemplate(
        #     template="Content: {page_content}\nSource: {source}",
        #     input_variables=["page_content", "source"],
        # )
        # final_qa_chain = StuffDocumentsChain(
        #     llm_chain=qa_chain,
        #     document_variable_name="context",
        #     document_prompt=doc_prompt,
        # )
        # llm_chain = LLMChain(
        #     llm=self.llm, 
        #     prompt=prompt, 
        # )
        # messages = [
        #     SystemMessagePromptTemplate.from_template(template=prompt_define),
        #     HumanMessagePromptTemplate.from_template(question)
        # ]
        # qa_prompt = ChatPromptTemplate.from_messages(messages)
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.db.as_retriever(search_kwargs={"k": 3}), 
            # memory=memory,
            get_chat_history=lambda h : h,
            return_source_documents=True,
            condense_question_llm=self.llm
            # combine_docs_chain_kwargs={"prompt": prompt_define},
        )
        self.chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate.from_template(prompt_define, chat_history=store_memory)
        # self.chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate.from_template(template=prompt_define)
        answer = self.chain.invoke({"question": question, "chat_history": store_memory})
        # result = json.loads(answer["answer"])
        answer = answer["answer"]
        store_memory.append((question, answer))
        set_key_redis(
            key=f"memory:{topic.lower().replace(' ', '-')}:{unit.lower().replace(' ','-')}",
            value=ujson.dumps(store_memory),
            expire_time=60 * 30
        )
        return answer

    def ingest(self, file_path: os.PathLike) -> None:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        splitted_documents = self.text_splitter.split_documents(documents)
        for i, splitted_document in enumerate(splitted_documents):
            splitted_document.metadata["source"] = f"{i}-pl"
        if self.db is None:
            self.db = Chroma.from_documents(splitted_documents, self.embeddings)
            self.chat_history = []

        else:
            self.db.add_documents(splitted_documents)

    def forget(self) -> None:
        self.db = None
        self.chain = None
        self.chat_history = None

