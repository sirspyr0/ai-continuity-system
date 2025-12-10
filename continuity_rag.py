"""
Continuity RAG System - Automatic Context Retrieval
Indexes all continuity documents and provides relevant context automatically.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


class ContinuityRAG:
    """RAG system for automatic continuity context retrieval."""
    
    def __init__(self, docs_root: str, index_file: str = "continuity.index"):
        self.docs_root = Path(docs_root)
        self.index_file = self.docs_root / index_file
        self.metadata_file = self.docs_root / f"{index_file}.meta.json"
        
        # Load embedding model (lightweight, runs locally)
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # 80MB model
        self.dimension = 384  # Model output dimension
        
        self.index = None
        self.documents = []
        self.metadata = []
        
    def index_documents(self, force_rebuild: bool = False):
        """Index all continuity documents."""
        
        if not force_rebuild and self.index_file.exists():
            print("Loading existing index...")
            self._load_index()
            return
            
        print("Building new document index...")
        self.documents = []
        self.metadata = []
        
        # Find all markdown files in the continuity system
        doc_patterns = [
            "**/PORTFOLIO_CONTEXT.md",
            "**/PROJECT_CONTEXT.md", 
            "**/SESSION_BRIEFING*.md",
            "**/CONTINUITY*.md",
            "**/*_CONTEXT.md",
            "**/README.md"
        ]
        
        for pattern in doc_patterns:
            for doc_path in self.docs_root.glob(pattern):
                if self._should_index(doc_path):
                    self._index_document(doc_path)
        
        if not self.documents:
            print("Warning: No documents found to index!")
            return
            
        # Create embeddings
        print(f"Creating embeddings for {len(self.documents)} document chunks...")
        embeddings = self.model.encode(self.documents, show_progress_bar=True)
        
        # Build FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Save index
        self._save_index()
        print(f"Index built: {len(self.documents)} chunks indexed")
        
    def _should_index(self, path: Path) -> bool:
        """Check if document should be indexed."""
        # Skip git directories and certain files
        excluded = ['.git', 'node_modules', '__pycache__', 'venv']
        return not any(ex in str(path) for ex in excluded)
    
    def _index_document(self, doc_path: Path):
        """Index a single document by chunking it."""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks (roughly 500 chars with overlap)
            chunks = self._chunk_text(content, chunk_size=500, overlap=100)
            
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) > 50:  # Skip tiny chunks
                    self.documents.append(chunk)
                    self.metadata.append({
                        'file': str(doc_path.relative_to(self.docs_root)),
                        'chunk_id': i,
                        'type': self._classify_doc(doc_path)
                    })
                    
        except Exception as e:
            print(f"Error indexing {doc_path}: {e}")
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk)
            start = end - overlap
            
        return chunks
    
    def _classify_doc(self, path: Path) -> str:
        """Classify document type based on name."""
        name = path.name.upper()
        
        if 'PORTFOLIO' in name:
            return 'portfolio'
        elif 'PROJECT' in name:
            return 'project'
        elif 'SESSION' in name:
            return 'session'
        elif 'CONTINUITY' in name:
            return 'theory'
        else:
            return 'general'
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve most relevant context for a query."""
        
        if self.index is None:
            self.index_documents()
        
        if not self.documents:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Search index
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            min(top_k, len(self.documents))
        )
        
        # Gather results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                results.append({
                    'content': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'relevance': float(1 / (1 + dist))  # Convert distance to relevance
                })
        
        return results
    
    def get_session_context(self, project_name: str = None) -> str:
        """Get comprehensive context for starting a session."""
        
        # Build context query
        if project_name:
            query = f"What do I need to know about the {project_name} project? What was the recent work and current state?"
        else:
            query = "What are the active projects and recent work? What is the current state?"
        
        # Retrieve relevant chunks
        results = self.retrieve_context(query, top_k=10)
        
        # Build context string
        context_parts = ["=== CONTINUITY CONTEXT ===\n"]
        
        # Group by document type
        by_type = {}
        for result in results:
            doc_type = result['metadata']['type']
            if doc_type not in by_type:
                by_type[doc_type] = []
            by_type[doc_type].append(result)
        
        # Portfolio context first
        if 'portfolio' in by_type:
            context_parts.append("\n## Portfolio Context:")
            for r in by_type['portfolio'][:2]:
                context_parts.append(f"\n{r['content']}\n")
        
        # Project context
        if 'project' in by_type:
            context_parts.append("\n## Project Context:")
            for r in by_type['project'][:3]:
                context_parts.append(f"\n{r['content']}\n")
        
        # Recent session info
        if 'session' in by_type:
            context_parts.append("\n## Recent Sessions:")
            for r in by_type['session'][:3]:
                context_parts.append(f"\n{r['content']}\n")
        
        # Theory/principles
        if 'theory' in by_type:
            context_parts.append("\n## Continuity Principles:")
            for r in by_type['theory'][:2]:
                context_parts.append(f"\n{r['content']}\n")
        
        context_parts.append("\n=== END CONTEXT ===")
        
        return "\n".join(context_parts)
    
    def _save_index(self):
        """Save index and metadata to disk."""
        faiss.write_index(self.index, str(self.index_file))
        
        with open(self.metadata_file, 'w') as f:
            json.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f)
    
    def _load_index(self):
        """Load index and metadata from disk."""
        self.index = faiss.read_index(str(self.index_file))
        
        with open(self.metadata_file, 'r') as f:
            data = json.load(f)
            self.documents = data['documents']
            self.metadata = data['metadata']


def main():
    """Test the RAG system."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python continuity_rag.py <docs_root> [query]")
        sys.exit(1)
    
    docs_root = sys.argv[1]
    rag = ContinuityRAG(docs_root)
    
    # Index documents
    rag.index_documents()
    
    if len(sys.argv) > 2:
        # Run query
        query = " ".join(sys.argv[2:])
        print(f"\nQuery: {query}\n")
        results = rag.retrieve_context(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} (relevance: {result['relevance']:.3f}) ---")
            print(f"File: {result['metadata']['file']}")
            print(f"Type: {result['metadata']['type']}")
            print(f"Content:\n{result['content'][:300]}...")
    else:
        # Get session context
        print("\n" + rag.get_session_context())


if __name__ == "__main__":
    main()
