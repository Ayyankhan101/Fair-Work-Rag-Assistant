import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

from fastembed import TextEmbedding



# ---------------------------------------------------
# Vector Store Path
# ---------------------------------------------------

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

VECTOR_STORE_DIR = os.path.join(
    ROOT,
    "vector_store"
)



# ---------------------------------------------------
# FastEmbed Wrapper
# ---------------------------------------------------

class FastEmbeddings(Embeddings):

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):

        self._model = TextEmbedding(
            model_name=model_name
        )


    def embed_documents(
        self,
        texts
    ):

        return [
            list(e)
            for e in self._model.embed(texts)
        ]


    def embed_query(
        self,
        text
    ):

        return list(
            self._model.embed([text])
        )[0]



# ---------------------------------------------------
# PDF Ingestion
# ---------------------------------------------------

def ingest_pdf(uploaded_file):


    # -----------------------------
    # Save Temporary PDF
    # -----------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:


        temp.write(
            uploaded_file.read()
        )


        pdf_path = temp.name



    # -----------------------------
    # Load PDF
    # -----------------------------

    loader = PyPDFLoader(
        pdf_path
    )


    documents = loader.load()



    # -----------------------------
    # Chunking
    # 500 tokens approx
    # 100 overlap
    # -----------------------------

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=100,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]

    )


    chunks = splitter.split_documents(
        documents
    )



    # -----------------------------
    # Metadata
    # -----------------------------

    for index, chunk in enumerate(chunks):


        chunk.metadata["source"] = (
            uploaded_file.name
        )


        chunk.metadata["chunk_id"] = (
            index
        )


        if "page" in chunk.metadata:

            chunk.metadata["page"] = (
                chunk.metadata["page"] + 1
            )

        else:

            chunk.metadata["page"] = 1



    # -----------------------------
    # Embeddings
    # -----------------------------

    embeddings = FastEmbeddings()



    # -----------------------------
    # Create FAISS Store
    # -----------------------------

    vector_store = FAISS.from_documents(

        chunks,

        embeddings

    )



    # -----------------------------
    # Save Vector Store
    # -----------------------------

    os.makedirs(

        VECTOR_STORE_DIR,

        exist_ok=True

    )


    vector_store.save_local(

        VECTOR_STORE_DIR

    )



    # -----------------------------
    # Cleanup
    # -----------------------------

    os.remove(
        pdf_path
    )



    return {

        "file": uploaded_file.name,

        "chunks": len(chunks),

        "status": "success"

    }