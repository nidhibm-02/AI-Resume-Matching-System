
import re

SKILLS = [
    "Python", "Java", "C++", "JavaScript",
    "React", "Node.js", "Django", "FastAPI",
    "HTML", "CSS", "SQL", "MySQL",
    "MongoDB", "PostgreSQL", "Machine Learning",
    "Deep Learning", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Scikit-learn",
    "Pandas", "NumPy", "Git", "Docker",
    "AWS", "Data Analysis", "REST API"
]


def extract_skills(resume_text):
    found_skills = []

    text = resume_text.lower()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills
