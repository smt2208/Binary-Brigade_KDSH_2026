import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pathway as pw
from pathway.xpacks.llm.document_store import DocumentStore
from pathway.xpacks.llm.servers import DocumentStoreServer
from pathway.xpacks.llm.embedders import OpenAIEmbedder
from pathway.stdlib.indexing.nearest_neighbors import UsearchKnnFactory
from pathway.xpacks.llm.splitters import RecursiveSplitter

from config.config import (
    EMBEDDING_MODEL, EMBEDDING_DIMENSIONS, CHUNK_SIZE, CHUNK_OVERLAP,
    SERVER_HOST, PATHWAY_PORT_MONTE_CRISTO, RESERVED_SPACE
)


def main():
    print("🚀 Starting Pathway Vector Store Server - The Count of Monte Cristo")
    print("📚 Indexing: The Count of Monte Cristo.txt")
    
    data_sources = pw.io.fs.read(
        "./data/Books/The Count of Monte Cristo.txt",
        format="binary",
        with_metadata=True,
        mode="streaming"
    )
    
    print(f"🔧 Initializing OpenAI embedder ({EMBEDDING_MODEL})...")
    embedder = OpenAIEmbedder(
        model=EMBEDDING_MODEL,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    print("🧠 Setting up Usearch KNN retriever (HNSW-based)...")
    retriever_factory = UsearchKnnFactory(
        embedder=embedder,
        dimensions=EMBEDDING_DIMENSIONS,
        reserved_space=RESERVED_SPACE
    )
    
    text_splitter = RecursiveSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n"]
    )
    
    print("📄 Building document store...")
    store = DocumentStore(
        docs=data_sources,
        retriever_factory=retriever_factory,
        splitter=text_splitter,
        parser=None
    )
    
    print("✅ Document store ready!")
    
    print("\n" + "="*80)
    print(f"🌐 Monte Cristo Server running at http://{SERVER_HOST}:{PATHWAY_PORT_MONTE_CRISTO}")
    print("📊 Endpoints:")
    print(f"   POST http://localhost:{PATHWAY_PORT_MONTE_CRISTO}/v1/retrieve")
    print("="*80)
    print("Press Ctrl+C to stop\n")
    
    server = DocumentStoreServer(
        host=SERVER_HOST,
        port=PATHWAY_PORT_MONTE_CRISTO,
        document_store=store
    )
    
    server.run(threaded=False, with_cache=True)


if __name__ == "__main__":
    main()
