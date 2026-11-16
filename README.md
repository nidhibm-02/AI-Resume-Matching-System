# AI-Based Resume Matching and Candidate Ranking System

## Project Overview

The AI-Based Resume Matching and Candidate Ranking System is a web application designed to simplify the recruitment process.

It analyzes candidate resumes against a given job description, calculates matching scores, identifies relevant and missing skills, and ranks candidates based on their suitability for the role.

## Key Features

- Job description input.
- Batch resume upload (PDF and DOCX).
- Automatic resume text extraction.
- Candidate information extraction.
- Technical skill identification.
- Semantic similarity-based resume matching.
- Experience and qualification comparison.
- Candidate match scores from 0 to 100.
- Matched and missing skill identification.
- Candidate ranking dashboard.
- Individual candidate analysis.
- Candidate search functionality.

## Technology Stack

**Frontend**
- React.js
- Vite
- Tailwind CSS
- Recharts
- Lucide React

**Backend**
- Python
- FastAPI
- PyMuPDF
- python-docx

**Machine Learning**
- Sentence Transformers
- Scikit-learn
- NumPy

## Matching Algorithm

The application evaluates candidates using four components:

| Component | Weight |
|---|---:|
| Semantic Similarity | 50% |
| Technical Skills | 20% |
| Experience | 15% |
| Qualification | 15% |
| **Total** | **100%** |

Sentence Transformers are used to calculate semantic similarity between the job description and candidate resumes.

The final score is calculated using the weighted combination of all four components.

## Project Structure

```text
AI-Resume-Matching-System/
│
├── backend/
│   ├── main.py
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   ├── profile_extractor.py
│   └── matching_engine.py
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.css
│       └── api.js
│
├── sample_resumes/
│
└── README.md
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Start the backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment and install the required dependencies.

```bash
pip install fastapi "uvicorn[standard]" python-multipart pymupdf python-docx spacy sentence-transformers scikit-learn numpy pandas sqlalchemy
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend URL: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 3. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: http://localhost:5173/

## Application Workflow

1. Enter the job description.
2. Upload multiple candidate resumes.
3. Click Analyze and Rank Candidates.
4. View the candidate rankings and match scores.
5. Explore individual candidate profiles and matching explanations.
6. Search for candidates using the search bar.

## Current Limitations

- Experience and qualification extraction use rule-based patterns and may require manual verification.
- Resume parsing accuracy depends on document quality and formatting.
- The matching scores are decision-support indicators and should not be treated as automatic hiring decisions.

## Future Enhancements

- Database integration for persistent candidate records.
- Advanced candidate filtering.
- Improved experience and qualification extraction.
- Exportable candidate evaluation reports.
- Authentication and recruiter management.

## Project Status

Functional prototype developed using React, FastAPI, and machine learning-based semantic matching.