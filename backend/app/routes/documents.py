import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from ..models import DocumentMetadata, LearningRequest, LearningResponse
from ..services.rag_service import rag_service
from ..services.ai_service import AIService
from ..config import settings

router = APIRouter(prefix="/documents", tags=["Documents & RAG"])

@router.post("/upload", response_model=DocumentMetadata)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form("guest-user-1")
):
    """
    Accepts PDF file upload, validates format and size, extracts page-by-page text,
    creates overlapping chunks with page tracking, and stores in the RAG store.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. LearnBridge AI currently accepts only PDF documents."
        )

    # Save temporary file to validate size and process with PyMuPDF
    temp_path = settings.UPLOAD_DIR / f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size_mb = os.path.getsize(temp_path) / (1024 * 1024)
        if file_size_mb > settings.MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB (file is {file_size_mb:.1f}MB)."
            )

        # Process PDF through PyMuPDF RAG
        metadata = rag_service.process_pdf(
            file_path=str(temp_path),
            original_filename=file.filename,
            user_id=user_id
        )
        return metadata

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("", response_model=List[DocumentMetadata])
async def list_documents(user_id: str = Query("guest-user-1")):
    """Lists all uploaded documents for the specified user."""
    return rag_service.list_documents(user_id=user_id)

@router.get("/{document_id}", response_model=DocumentMetadata)
async def get_document(document_id: str, user_id: str = Query("guest-user-1")):
    """Retrieves metadata for a specific document."""
    doc = rag_service.get_document(document_id, user_id=user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or access denied.")
    return doc

@router.get("/{document_id}/status")
async def get_document_status(document_id: str, user_id: str = Query("guest-user-1")):
    """Checks processing status of an uploaded document."""
    doc = rag_service.get_document(document_id, user_id=user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "total_pages": doc.total_pages,
        "error_message": doc.error_message
    }

@router.post("/{document_id}/ask", response_model=LearningResponse)
async def ask_document(
    document_id: str,
    request: LearningRequest
):
    """
    Asks a question targeting the specified document using RAG.
    Preserves exact page citations and respects source_mode ('pdf_and_ai', 'pdf_only', 'general_ai').
    """
    request.document_id = document_id
    response = await AIService.process_learning_request(request)
    return response

@router.delete("/{document_id}")
async def delete_document(document_id: str, user_id: str = Query("guest-user-1")):
    """Deletes an uploaded document and purges its stored chunks."""
    deleted = rag_service.delete_document(document_id, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found or unauthorized.")
    return {"success": True, "message": f"Document {document_id} and its index deleted successfully."}
