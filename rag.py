import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb


# ============================================================
# KISANAI RAG CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
DOCUMENT_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "farming_documents"
)

COLLECTION_NAME = "kisanai_documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# ============================================================
# CREATE CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ============================================================
# EXTRACT TEXT FROM PDF
# ============================================================

def extract_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ============================================================
# CREATE TEXT CHUNKS
# ============================================================

def create_chunks(
    text,
    chunk_size=800,
    overlap=100
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start = end - overlap

    return chunks


# ============================================================
# ADD PDF TO DATABASE
# ============================================================

def add_pdf_to_database(pdf_path):

    try:

        text = extract_pdf_text(pdf_path)

        if not text.strip():
            return 0

        chunks = create_chunks(text)

        if not chunks:
            return 0

        file_name = os.path.basename(pdf_path)

        embeddings = embedding_model.encode(
            chunks
        ).tolist()

        ids = [
            f"{file_name}_{i}"
            for i in range(len(chunks))
        ]

        collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=[
                {
                    "source": file_name
                }
                for _ in chunks
            ]
        )

        return len(chunks)

    except Exception as e:

        print("PDF processing error:", e)

        return 0


# ============================================================
# PROCESS ALL PDFs IN FARMING DOCUMENTS FOLDER
# ============================================================

def process_all_pdfs():

    total_chunks = 0
    processed_files = []

    if not os.path.exists(DOCUMENT_FOLDER):

        os.makedirs(DOCUMENT_FOLDER)

        return 0, []

    for file_name in os.listdir(DOCUMENT_FOLDER):

        if file_name.lower().endswith(".pdf"):

            pdf_path = os.path.join(
                DOCUMENT_FOLDER,
                file_name
            )

            chunks = add_pdf_to_database(
                pdf_path
            )

            if chunks > 0:

                total_chunks += chunks

                processed_files.append(
                    file_name
                )

    return total_chunks, processed_files


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(
    question,
    n_results=4
):

    try:

        question_embedding = embedding_model.encode(
            [question]
        ).tolist()

        results = collection.query(
            query_embeddings=question_embedding,
            n_results=n_results
        )

        documents = results.get(
            "documents",
            [[]]
        )

        if not documents:
            return []

        if not documents[0]:
            return []

        return documents[0]

    except Exception as e:

        print("Search error:", e)

        return []


# ============================================================
# GET DOCUMENT COUNT
# ============================================================

def get_document_count():

    try:

        return collection.count()

    except:

        return 0