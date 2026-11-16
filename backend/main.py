from profile_extractor import extract_candidate_details
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from matching_engine import calculate_match
from typing import List
from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Resume Matching System",
    description="AI-powered resume matching and candidate ranking API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "AI Resume Matching System API is running!",
        "status": "success"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):

    results = []

    for file in files:
        try:
            filename = file.filename.lower()

            if not filename.endswith((".pdf", ".docx")):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file: {file.filename}"
                )

            file_bytes = await file.read()

            if not file_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Empty file: {file.filename}"
                )

            resume_text = extract_resume_text(
                file.filename,
                file_bytes
            )

            candidate_skills = extract_skills(resume_text)
            candidate_details = extract_candidate_details(
                 resume_text,
                 file.filename
                 )

            results.append({
                 "filename": file.filename,
                "extracted_text": resume_text,
                "candidate_details": candidate_details,
                "skills": candidate_skills,
                "status": "success"
            })

        except HTTPException:
            raise

        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e),
                "status": "failed"
            })

    return {
        "total_resumes": len(files),
        "results": results
    }

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Use OpenAPI 3.0 for Swagger file-picker compatibility
    schema["openapi"] = "3.0.3"

    components = schema.get("components", {}).get("schemas", {})

    for component in components.values():
        properties = component.get("properties", {})

        for prop in properties.values():

            # Fix multiple file uploads
            if prop.get("type") == "array":
                items = prop.get("items", {})

                if items.get("contentMediaType"):
                    items.pop("contentMediaType", None)
                    items["format"] = "binary"

            # Fix single file uploads
            elif prop.get("contentMediaType"):
                prop.pop("contentMediaType", None)
                prop["format"] = "binary"

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.post("/match-resumes")
async def match_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Please upload at least one resume."
        )

    candidates = []

    for file in files:
        try:
            filename = file.filename.lower()

            if not filename.endswith((".pdf", ".docx")):
                continue

            file_bytes = await file.read()

            resume_text = extract_resume_text(
                file.filename,
                file_bytes
            )

            if not resume_text.strip():
                continue

            candidate_skills = extract_skills(resume_text)
            candidate_details = extract_candidate_details(
                resume_text,
                file.filename
            )

            match_result = calculate_match(
                job_description,
                resume_text,
                candidate_skills
            )

            candidates.append({
                "candidate_name": file.filename.rsplit(".", 1)[0],
                "filename": file.filename,
                "skills": candidate_skills,
                "semantic_score": match_result["semantic_score"],
                "skill_score": match_result["skill_score"],
                "experience_score": match_result["experience_score"],
                "required_experience": match_result["required_experience"],
                "candidate_experience": match_result["candidate_experience"],
                "qualification_score": match_result["qualification_score"],
                "required_qualification": match_result["required_qualification"],
                "candidate_qualification": match_result["candidate_qualification"],
                "overall_score": match_result["overall_score"],
                "matched_skills": match_result["matched_skills"],
                "missing_skills": match_result["missing_skills"],
                "explanations": match_result["explanations"],
                "candidate_name": candidate_details["candidate_name"],
                "email": candidate_details["email"],
                "phone": candidate_details["phone"],
                "experience": candidate_details["experience"],
                "qualification": candidate_details["qualification"],
            })

        except Exception as e:
            candidates.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })

    successful_candidates = [
        c for c in candidates if "overall_score" in c
    ]

    successful_candidates.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )

    for rank, candidate in enumerate(successful_candidates, start=1):
        candidate["rank"] = rank

    return {
        "job_description": job_description,
        "total_resumes": len(files),
        "successful_matches": len(successful_candidates),
        "ranked_candidates": successful_candidates,
        "failed_resumes": [
            c for c in candidates if "status" in c
        ]
    }

