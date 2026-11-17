
import re
from onnx_embedding import engine
from sklearn.metrics.pairwise import cosine_similarity
from skill_extractor import SKILLS
from profile_extractor import extract_qualification, extract_experience

# Load the pretrained model once
model = engine


def calculate_similarity(job_description, resume_text):
    embeddings = model.encode([job_description, resume_text])
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(similarity) * 100, 2)


def extract_years(text):
    """
    Extract years of professional experience
    from experience-related text.
    """
    patterns = [
        r"(?:experience|worked|work|employment)[^\n.]{0,60}?(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\s+of\s+(?:professional\s+)?experience"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return float(match.group(1))

    return 0.0


def calculate_experience_score(job_description, resume_text):
    jd_lower = job_description.lower()

    required_years = extract_years(job_description)

    profile_experience = extract_experience(resume_text)

    if isinstance(profile_experience, (int, float)):
        candidate_years = float(profile_experience)
    elif profile_experience == "Fresher":
        candidate_years = 0.0
    else:
        candidate_years = extract_years(resume_text)

    # Check whether freshers are explicitly eligible
    fresher_allowed = bool(
        re.search(
            r"\bfreshers?\b|"
            r"\bno experience required\b|"
            r"\b0\s*(?:-|to)\s*1\s*years?\b",
            jd_lower
        )
    )

    # Calculate experience score
    if required_years == 0:
        score = 100.0

    elif fresher_allowed and candidate_years == 0:
        score = 100.0

    else:
        score = min(
            (candidate_years / required_years) * 100,
            100
        )

    return {
        "required_experience": required_years,
        "candidate_experience": candidate_years,
        "experience_score": round(score, 2)
    }


def calculate_qualification_score(job_description, resume_text):
    required = extract_qualification(job_description)
    candidate = extract_qualification(resume_text)

    if required == ["Not specified"]:
        score = 100.0

    elif candidate == ["Not specified"]:
        score = 0.0

    else:
        bachelor_degrees = {
            "bachelor's degree",
            "bachelor of engineering",
            "bachelor of technology",
            "b.sc.",
            "bca"
        }

        required_set = {q.lower() for q in required}
        candidate_set = {q.lower() for q in candidate}

        # A general bachelor's requirement accepts a recognized bachelor's degree
        if "bachelor's degree" in required_set:
            score = 100.0 if candidate_set.intersection(
                bachelor_degrees
            ) else 0.0

        # Treat listed degree options as alternatives
        elif required_set.intersection(candidate_set):
            score = 100.0

        else:
            score = 0.0

    return {
        "required_qualification": required,
        "candidate_qualification": candidate,
        "qualification_score": round(score, 2)
    }

def calculate_match(job_description, resume_text, resume_skills):
    semantic_score = calculate_similarity(
        job_description,
        resume_text
    )

    jd_lower = job_description.lower()

    required_skills = [
        skill for skill in SKILLS
        if skill.lower() in jd_lower
    ]

    # Identify alternative skills (FastAPI OR Django)
    alternative_groups = []

    if re.search(r"\bfastapi\s+or\s+django\b", jd_lower):
        required_skills = [
            skill for skill in required_skills
            if skill.lower() not in ["fastapi", "django"]
        ]

        alternative_groups.append(["FastAPI", "Django"])

    candidate_skills = set(resume_skills)

    matched_skills = [
        skill for skill in required_skills
        if skill in candidate_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in candidate_skills
    ]

    # Check alternative skills
    matched_alternatives = 0

    for group in alternative_groups:
        available = [
            skill for skill in group
            if skill in candidate_skills
        ]

        if available:
            matched_skills.extend(available)
            matched_alternatives += 1
        else:
            missing_skills.append("FastAPI or Django")

    # Calculate skill score
    total_requirements = (
        len(required_skills) + len(alternative_groups)
    )

    matched_count = (
        len(matched_skills) - len(
            [s for s in matched_skills if s in alternative_groups[0]]
        ) if alternative_groups and matched_alternatives
        else len(matched_skills)
    ) + matched_alternatives

    if total_requirements:
        skill_score = (
            matched_count / total_requirements
        ) * 100
    else:
        skill_score = semantic_score

    # Experience score
    experience_result = calculate_experience_score(
        job_description,
        resume_text
    )

    experience_score = experience_result["experience_score"]

    # Qualification score
    qualification_result = calculate_qualification_score(
        job_description,
        resume_text
    )

    qualification_score = qualification_result["qualification_score"]

    # Overall score
    overall_score = (
        0.50 * semantic_score
        + 0.20 * skill_score
        + 0.15 * experience_score
        + 0.15 * qualification_score
    )

    # Generate explanations
    explanations = []

    if semantic_score >= 70:
        explanations.append(
            "Strong semantic similarity with the job description."
        )
    elif semantic_score >= 40:
        explanations.append(
            "Moderate similarity with the job requirements."
        )
    else:
        explanations.append(
            "Low similarity with the job requirements."
        )

    if matched_skills:
        explanations.append(
            "Matched skills: " + ", ".join(matched_skills)
        )

    if missing_skills:
        explanations.append(
            "Missing skills: " + ", ".join(missing_skills)
        )

    if experience_score >= 100:
        explanations.append(
            "Candidate meets or exceeds the required experience."
        )
    else:
        explanations.append(
            "Candidate has less experience than required."
        )

    if qualification_score == 100:
        explanations.append(
            "Required educational qualification matched."
        )
    elif qualification_score == 0:
        explanations.append(
            "Required educational qualification was not identified in the resume."
        )
    else:
        explanations.append(
            "Educational qualification partially matches the requirement."
        )

    return {
        "semantic_score": round(semantic_score, 2),
        "skill_score": round(skill_score, 2),
        "experience_score": experience_score,
        "required_experience": experience_result["required_experience"],
        "candidate_experience": experience_result["candidate_experience"],
        "overall_score": round(overall_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "qualification_score": qualification_score,
        "required_qualification": qualification_result["required_qualification"],
        "candidate_qualification": qualification_result["candidate_qualification"],
        "explanations": explanations
    }

