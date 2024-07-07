from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb import QueryResult
import os

class VectorFileDatabase():
    DB_NAME = 'LocalFiles'

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n"], chunk_size=1, chunk_overlap=0)
        self.db = chromadb.Client().get_or_create_collection(name=self.DB_NAME)

    def add_file(self, path: str = ''): 
        if not os.path.isfile(path):
            print(f'VectorFileDatabase error in adding file, file does not exist: {path}')

        # TODO: open different kinds of files such as pdfs, docx, etc. 
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()

        chunks = self.text_splitter.split_text(text)

        self.db.upsert(documents=chunks, ids=[f'{path}[{str(i)}]' for i, _ in enumerate(chunks)])

    def search_file(self, prompt: str = '', n_results: int = 4):
        docs : QueryResult = self.db.query(query_texts=[prompt], n_results = n_results)

        return ''.join(docs['documents'][0])


