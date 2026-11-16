
import re
from pathlib import Path


def extract_email(text):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    return match.group(0) if match else "Not found"


def extract_phone(text):
    matches = re.findall(
        r"(?<!\d)(?:\+?\d{1,3}[-.\s]?)?(?:\d[-.\s]?){9,12}\d(?!\d)",
        text
    )

    for phone in matches:
        digits = re.sub(r"\D", "", phone)

        if 10 <= len(digits) <= 13:
            return phone.strip()

    return "Not found"


def extract_experience(text):
    text_lower = text.lower()

    # Extract years of experience
    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        text_lower
    )

    # Extract months of experience
    month_match = re.search(
        r"(\d+)\s*(?:months?|mos?)",
        text_lower
    )

    total_years = 0.0

    if year_match:
        total_years += float(year_match.group(1))

    if month_match:
        total_years += int(month_match.group(1)) / 12

    if year_match or month_match:
        return round(total_years, 2)

    # Check for fresher / entry-level candidates
    if re.search(r"\bfresher\b|\bentry.level\b", text_lower):
        return "Fresher"

    return "Not specified"


def extract_name(text, filename=""):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    excluded_words = [
        "resume",
        "curriculum vitae",
        "professional summary",
        "career objective",
        "contact",
        "education",
        "experience",
        "skills"
    ]

    for line in lines[:8]:
        if "@" in line or re.search(r"\d", line):
            continue

        cleaned_line = re.split(r"[|,]", line)[0].strip()

        if any(word in cleaned_line.lower() for word in excluded_words):
            continue

        if re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,59}", cleaned_line):
            words = cleaned_line.split()

            if 2 <= len(words) <= 4:
                return cleaned_line

    if filename:
        fallback_name = Path(filename).stem
        fallback_name = re.sub(r"[_-]+", " ", fallback_name)
        return fallback_name.strip().title()

    return "Not found"


def extract_candidate_details(resume_text, filename=""):
    return {
        "candidate_name": extract_name(resume_text, filename),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "experience": extract_experience(resume_text),
        "qualification": extract_qualification(resume_text)
    }


def extract_qualification(text):
    qualifications = [
        ("Bachelor of Engineering",
         r"\bBachelor\s+of\s+Engineering\b|\bB\.?\s*E\.?\b"),

        ("Bachelor of Technology",
         r"\bBachelor\s+of\s+Technology\b|\bB\.?\s*Tech\.?\b"),

        ("B.Sc.",
         r"\bBachelor\s+of\s+Science\b|\bB\.?\s*Sc\.?\b"),

        ("BCA",
         r"\bBachelor\s+of\s+Computer\s+Applications\b|\bBCA\b"),

        ("B.Com.",
         r"\bBachelor\s+of\s+Commerce\b|\bB\.?\s*Com\.?\b"),

        ("M.Tech",
         r"\bMaster\s+of\s+Technology\b|\bM\.?\s*Tech\.?\b"),

        ("M.Sc.",
         r"\bMaster\s+of\s+Science\b|\bM\.?\s*Sc\.?\b"),

        ("MCA",
         r"\bMaster\s+of\s+Computer\s+Applications\b|\bMCA\b"),

        ("MBA",
         r"\bMaster\s+of\s+Business\s+Administration\b|\bMBA\b"),

        ("Ph.D.",
         r"\bPh\.?\s*D\.?\b")
    ]

    lines = text.splitlines()
    education_text = ""
    inside_education = False

    for line in lines:
        lower_line = line.lower().strip()

        if any(section in lower_line for section in [
            "education",
            "academic qualification",
            "educational qualification",
            "academics"
        ]):
            inside_education = True
            education_text += line + "\n"
            continue

        if inside_education and any(section in lower_line for section in [
            "experience",
            "projects",
            "technical skills",
            "certifications",
            "achievements",
            "internships"
        ]):
            inside_education = False

        if inside_education:
            education_text += line + "\n"

    source_text = education_text if education_text.strip() else text

    found = []

    # Detect general bachelor's degree requirements
    if re.search(
        r"\bBachelor'?s?\s+degree\b|\bundergraduate\s+degree\b",
        source_text,
        re.IGNORECASE
    ):
        found.append("Bachelor's degree")

    for name, pattern in qualifications:
        if re.search(pattern, source_text, re.IGNORECASE):
            found.append(name)

    return list(dict.fromkeys(found)) if found else ["Not specified"]
