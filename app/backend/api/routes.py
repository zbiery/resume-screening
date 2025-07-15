import os
from fastapi import APIRouter, Request, UploadFile, File, Form,  HTTPException
from fastapi.responses import JSONResponse

from .schemas import JobText, ResumeText
from ..common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/resumes/upload")
async def upload_resume(request: Request, file: UploadFile = File(...)):
    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # Check if file is empty
        contents = await file.read()
        print(f"File size: {len(contents)} bytes")
        
        if not contents:
            raise HTTPException(status_code=400, detail="Empty file received")
        
        # Reset file pointer
        await file.seek(0)
        
        _, ext = os.path.splitext(file.filename) # type: ignore
        if not ext:
            raise HTTPException(status_code=400, detail="File has no extension")
        
        print(f"Processing file with extension: {ext}")
        
        # FIXED: Access file_processor from app.state instead of app.processor
        text_chunks = await request.app.state.file_processor.process(file.file, ext)
        extracted_text = "\n".join(text_chunks)
        
    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"filename": file.filename, "content": extracted_text}

@router.post("/jobs/upload")
async def upload_job(description: str = Form(...)):
    try:
        logger.info(f"Received job description upload request")
        logger.debug(f"Job description length: {len(description)} characters")
        
        if not description or not description.strip():
            logger.warning("Empty job description received")
            raise HTTPException(status_code=400, detail="Job description cannot be empty")
        
        logger.info("Job description uploaded successfully")
        return {"content": description}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload_job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/resumes/analyze")
async def analyze_resume(request: Request, resume: ResumeText):
    try:
        logger.info("Starting resume analysis")
        logger.debug(f"Resume content length: {len(resume.content)} characters")
        
        if not resume.content or not resume.content.strip():
            logger.warning("Empty resume content received for analysis")
            raise HTTPException(status_code=400, detail="Resume content cannot be empty")
        
        analyzer = request.app.state.analyzer
        if not analyzer:
            logger.error("Analyzer not found in app state")
            raise HTTPException(status_code=500, detail="Analyzer not available")
        
        logger.info("Calling analyzer.analyze_candidate")
        result = await analyzer.analyze_candidate(resume.content)
        
        if not result:
            logger.warning("Analyzer returned empty result")
            raise HTTPException(status_code=500, detail="Analysis failed - no result returned")
        
        logger.info("Resume analysis completed successfully")
        logger.debug(f"Analysis result keys: {list(result.keys()) if isinstance(result, dict) else 'Non-dict result'}")
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_resume: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")

@router.post("/jobs/analyze")
async def analyze_job(request: Request, job: JobText):
    try:
        logger.info("Starting job analysis")
        logger.debug(f"Job content length: {len(job.content)} characters")
        
        if not job.content or not job.content.strip():
            logger.warning("Empty job content received for analysis")
            raise HTTPException(status_code=400, detail="Job content cannot be empty")
        
        analyzer = request.app.state.analyzer
        if not analyzer:
            logger.error("Analyzer not found in app state")
            raise HTTPException(status_code=500, detail="Analyzer not available")
        
        logger.info("Calling analyzer.analyze_job")
        result = await analyzer.analyze_job(job.content)
        
        if not result:
            logger.warning("Analyzer returned empty result")
            raise HTTPException(status_code=500, detail="Analysis failed - no result returned")
        
        logger.info("Job analysis completed successfully")
        logger.debug(f"Analysis result keys: {list(result.keys()) if isinstance(result, dict) else 'Non-dict result'}")
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")