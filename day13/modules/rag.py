"""RAG 文档问答模块"""

import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL

class RAGModule:
    """RAG 文档问答模块"""

    def __init__(self, docs_dir: str = None, llm=None):
        self.docs_dir = docs_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "documents")
        self.llm = llm
        self.retriever = None
        self._initialized = False
        self.document_count = 0
        self.chunk_count = 0

    def init(self):
        try:
            if not os.path.exists(self.docs_dir):
                return "文档目录不存在"
            loader = DirectoryLoader(self.docs_dir, glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
            docs = loader.load()
            if not docs:
                return "文档目录为空"
            self.document_count = len(docs)
            splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
            split_docs = splitter.split_documents(docs)
            self.chunk_count = len(split_docs)
            embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_BASE_URL)
            persist_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
            vs = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_dir)
            self.retriever = vs.as_retriever(search_kwargs={"k": 3})
            self._initialized = True
            return f"初始化完成：{self.document_count} 个文档，{self.chunk_count} 个文本块"
        except Exception as e:
            self._initialized = False
            return f"初始化失败：{e}"

    def query(self, question: str) -> str:
        if not self._initialized or not self.retriever:
            return "RAG 系统未初始化"
        try:
            docs = self.retriever.invoke(question)
            context = "\n\n".join(d.page_content for d in docs)
            if self.llm:
                prompt = ChatPromptTemplate.from_template("根据上下文回答问题。\n\n上下文：{context}\n\n问题：{question}\n\n回答：")
                return (prompt | self.llm | StrOutputParser()).invoke({"context": context, "question": question})
            return f"检索到 {len(docs)} 个相关文档"
        except Exception as e:
            return f"RAG 查询失败：{e}"

    def search_only(self, query: str) -> list:
        if not self._initialized or not self.retriever:
            return []
        return self.retriever.invoke(query)
