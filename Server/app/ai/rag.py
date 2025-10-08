import os
from PyPDF2 import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


class RAG:
  def __init__(self,
                model_embedding: str = "sentence-transformers/all-MiniLM-L6-v2",
                  folder_path: str = None,
                  persist_directory: str = "app/database"):

    self.persist_directory = persist_directory

    self.model_embedding = HuggingFaceEmbeddings(
    model_name=model_embedding,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
    )

    self.folder_path = folder_path

    if os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
        print("🔁 Đang tải lại vector database từ app/database ...")
        self.vectorstores = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.model_embedding
        )
    else:
        print("🆕 Chưa có database, đang tạo mới...")
        self.documents = self.load_document()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
        )
        self.all_splits = self.text_splitter.split_documents(self.documents)

        self.vectorstores = Chroma.from_documents(
            documents=self.all_splits,
            embedding=self.model_embedding,
            persist_directory=self.persist_directory
        )
        print(f"✅ Đã lưu vector database tại: {self.persist_directory}")

  def load_document(self):
    documents = []
    for filename in os.listdir(self.folder_path):
      if filename.endswith(".txt"):
          full_path = os.path.join(self.folder_path, filename)
          with open(full_path, "r", encoding="utf-8") as file:
              content = file.read()
              documents.append(Document(page_content=content,
                                        metadata={"source": full_path}))
      if filename.endswith(".pdf"):
          full_path = os.path.join(self.folder_path, filename)
          reader = PdfReader(full_path)
          content = ""
          for page in reader.pages:
              content_tempt = page.extract_text()
              content += "\n" + content_tempt
          documents.append(Document(page_content=content,
                                    metadata={"source": full_path}))
    return documents


  def retriver(self, question: str, k: int = 3) -> list:
    retriver = self.vectorstores.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in retriver])
    return context
