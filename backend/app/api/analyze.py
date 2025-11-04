from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from app.core.security import get_current_user
from app.models.user import User
from app.services.resume_service import extract_text_from_pdf
from app.services.openai_service import analyze_resume
from app.services.pdf_service import generate_pdf_from_text
import io

router = APIRouter()


class AnalyzeResponse(BaseModel):
    score: int
    structure_feedback: str
    keyword_analysis: str
    improvements: list[str]
    improved_content: str


class ExportRequest(BaseModel):
    content: str


@router.post("/upload", response_model=AnalyzeResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    target_role: Optional[str] = Query(None, description="Optional target job role for tailored analysis"),
    current_user: User = Depends(get_current_user)
):
    """Upload resume PDF and get AI-powered analysis."""
    try:
        # Extract text from PDF
        resume_text = await extract_text_from_pdf(file)
        
        # Analyze with OpenAI
        analysis = await analyze_resume(resume_text, target_role)
        
        return AnalyzeResponse(**analysis)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing resume: {str(e)}"
        )


@router.post("/improve")
async def export_improved_resume(
    request: ExportRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate and download improved resume as PDF."""
    try:
        # Generate PDF
        pdf_buffer = generate_pdf_from_text(request.content)
        
        return StreamingResponse(
            io.BytesIO(pdf_buffer.read()),
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=improved_resume.pdf"
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )
