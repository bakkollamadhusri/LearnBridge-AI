import os
import re
import math
import uuid
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import pymupdf  # PyMuPDF
from ..models import DocumentMetadata, Citation

class DocumentChunk:
    def __init__(self, chunk_id: str, document_id: str, page_number: int, text: str, user_id: str):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.page_number = page_number
        self.text = text
        self.user_id = user_id
        self.tokens = self._tokenize(text)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_\u0C00-\u0C7F\u0900-\u097F]+\b', text) if len(w) > 1]

class RAGService:
    def __init__(self):
        # In-memory document registry & chunk storage
        # Keyed by document_id for strict isolation
        self.documents: Dict[str, DocumentMetadata] = {}
        self.chunks_by_doc: Dict[str, List[DocumentChunk]] = {}

    def process_pdf(self, file_path: str, original_filename: str, user_id: str = "guest-user-1") -> DocumentMetadata:
        doc_id = str(uuid.uuid4())
        file_size = os.path.getsize(file_path)

        # Validate file
        if file_size == 0:
            raise ValueError("Uploaded PDF file is empty (0 bytes).")

        try:
            doc = pymupdf.open(file_path)
            total_pages = len(doc)
            if total_pages == 0:
                raise ValueError("PDF contains no readable pages.")

            all_extracted_chunks: List[DocumentChunk] = []
            preview_texts: List[str] = []

            for page_index in range(total_pages):
                page = doc[page_index]
                page_num = page_index + 1  # 1-indexed page number
                text = page.get_text("text").strip()

                if not text:
                    # Check for scanned page
                    images = page.get_images()
                    if images:
                        text = f"[Scanned/Image-based Page {page_num} containing {len(images)} graphic element(s)]"

                if text:
                    if len(preview_texts) < 3:
                        preview_texts.append(text[:200])

                    # Chunk page text with 400-word chunks and 50-word overlap
                    words = text.split()
                    chunk_size = 350
                    overlap = 50
                    start = 0

                    if len(words) <= chunk_size:
                        c_id = f"{doc_id}_p{page_num}_c0"
                        all_extracted_chunks.append(DocumentChunk(c_id, doc_id, page_num, text, user_id))
                    else:
                        chunk_idx = 0
                        while start < len(words):
                            chunk_words = words[start:start + chunk_size]
                            chunk_text = " ".join(chunk_words)
                            c_id = f"{doc_id}_p{page_num}_c{chunk_idx}"
                            all_extracted_chunks.append(DocumentChunk(c_id, doc_id, page_num, chunk_text, user_id))
                            start += (chunk_size - overlap)
                            chunk_idx += 1

            doc.close()

            summary = " ".join(preview_texts)[:300] + "..." if preview_texts else "PDF parsed successfully."

            metadata = DocumentMetadata(
                id=doc_id,
                filename=original_filename,
                file_size_bytes=file_size,
                total_pages=total_pages,
                uploaded_at=datetime.now(),
                status="ready",
                user_id=user_id,
                summary_preview=summary
            )

            # Store in registry
            self.documents[doc_id] = metadata
            self.chunks_by_doc[doc_id] = all_extracted_chunks
            return metadata

        except Exception as e:
            if doc_id in self.documents:
                self.documents[doc_id].status = "error"
                self.documents[doc_id].error_message = str(e)
            raise RuntimeError(f"Failed to process PDF: {str(e)}")

    def get_document(self, document_id: str, user_id: str = "guest-user-1") -> Optional[DocumentMetadata]:
        doc = self.documents.get(document_id)
        if doc and doc.user_id == user_id:
            return doc
        return None

    def list_documents(self, user_id: str = "guest-user-1") -> List[DocumentMetadata]:
        return [doc for doc in self.documents.values() if doc.user_id == user_id]

    def delete_document(self, document_id: str, user_id: str = "guest-user-1") -> bool:
        if document_id in self.documents and self.documents[document_id].user_id == user_id:
            del self.documents[document_id]
            if document_id in self.chunks_by_doc:
                del self.chunks_by_doc[document_id]
            return True
        return False

    def retrieve_relevant_chunks(
        self,
        document_id: str,
        query: str,
        user_id: str = "guest-user-1",
        top_k: int = 4
    ) -> Tuple[List[Citation], str]:
        """
        Retrieves top_k relevant chunks STRICTLY from the specified document_id and user_id.
        Guarantees isolation against other documents and users.
        """
        doc = self.get_document(document_id, user_id)
        if not doc:
            return [], ""

        chunks = self.chunks_by_doc.get(document_id, [])
        if not chunks:
            return [], ""

        STOP_WORDS = {
            "what", "is", "the", "of", "in", "a", "an", "to", "for", "on", "at", "by",
            "with", "from", "as", "into", "and", "or", "how", "why", "who", "which",
            "are", "was", "were", "be", "been", "being", "have", "has", "had", "do",
            "does", "did", "can", "could", "would", "should", "tell", "explain", "about", "me"
        }
        all_tokens = [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_\u0C00-\u0C7F\u0900-\u097F]+\b', query) if len(w) > 1]
        query_tokens = [w for w in all_tokens if w not in STOP_WORDS] or all_tokens
        
        if not query_tokens:
            top_chunks = chunks[:top_k]
            citations = [
                Citation(
                    document_id=document_id,
                    filename=doc.filename,
                    page_number=c.page_number,
                    text_snippet=c.text[:400] + "...",
                    score=0.5
                ) for c in top_chunks
            ]
            context = "\n\n".join([f"[Page {c.page_number}]: {c.text}" for c in top_chunks])
            return citations, context

        scored_chunks: List[Tuple[float, DocumentChunk]] = []

        # Calculate BM25 / TF-IDF style lexical overlap on meaningful tokens
        for chunk in chunks:
            chunk_tokens_set = set(chunk.tokens)
            overlap_count = sum(1 for q in query_tokens if q in chunk_tokens_set)
            
            # Phrase boost only for meaningful multi-word or exact keyword matches
            chunk_lower = chunk.text.lower()
            phrase_boost = 1.5 if any(q in chunk_lower for q in query_tokens if len(q) >= 3) else 0.0

            if overlap_count > 0:
                score = (overlap_count / (math.sqrt(len(chunk.tokens) + 10))) + phrase_boost
                scored_chunks.append((score, chunk))

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_matches = scored_chunks[:top_k]

        citations: List[Citation] = []
        context_parts: List[str] = []

        for score, chunk in top_matches:
            citations.append(Citation(
                document_id=document_id,
                filename=doc.filename,
                page_number=chunk.page_number,
                text_snippet=chunk.text[:400] + ("..." if len(chunk.text) > 400 else ""),
                score=round(float(score), 3)
            ))
            context_parts.append(f"--- [Document: {doc.filename} | Page {chunk.page_number}] ---\n{chunk.text}")

        full_context = "\n\n".join(context_parts)
        return citations, full_context

rag_service = RAGService()
