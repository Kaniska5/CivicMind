import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE = Path(__file__).parent.parent


def _load_folder(folder: Path, extension: str) -> list:
    """Load all files with given extension from a folder. Returns list of docs."""
    docs = []
    if not folder.exists():
        logger.warning(f"Folder not found, skipping: {folder}")
        return docs
    for filepath in folder.glob(f"*{extension}"):
        try:
            if extension == ".pdf":
                loader = PyPDFLoader(str(filepath))
            else:
                loader = TextLoader(str(filepath), encoding="utf-8")
            loaded = loader.load()
            docs.extend(loaded)
            logger.info(f"Loaded: {filepath.name}")
        except Exception as e:
            logger.error(f"Failed to load {filepath.name}: {e}")
    return docs


def ingest_documents(extra_folders=None):
    if extra_folders is None:
        extra_folders = []

    all_docs = []

    folders = [
        (BASE / "knowledge_base" / "central_schemes", ".pdf"),
        (BASE / "knowledge_base" / "legal_docs",      ".txt"),
        (BASE / "knowledge_base" / "state_docs",      ".pdf"),
        (BASE / "knowledge_base" / "budget",           ".txt"),
    ]

    for folder, ext in folders:
        all_docs.extend(_load_folder(folder, ext))

    for folder_path in extra_folders:
        folder = Path(folder_path)
        for ext in (".pdf", ".txt"):
            all_docs.extend(_load_folder(folder, ext))

    logger.info(f"Total documents loaded: {len(all_docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(all_docs)
    logger.info(f"Total chunks created: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    output_path = BASE / "backend" / "data" / "vector_store"
    output_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(output_path))
    logger.info(f"FAISS index saved to: {output_path}")


if __name__ == "__main__":
    ingest_documents()
