import fitz  # PyMuPDF
import re


SECTION_HEADERS = {
    'education': ['education'],
    'experience': ['experience', 'work experience', 'internship'],
    'projects': ['projects'],
    'skills': ['skills', 'technical skills'],
    'certifications': ['certifications'],
    'achievements': ['achievements', 'awards'],
    'extracurriculars': ['extracurriculars', 'leadership', 'positions of responsibility'],
    'social_work': ['volunteer', 'social work', 'community service'],
    'summary': ['summary', 'about me', 'profile'],
}


def parse_resume(file_path):
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)

    parsed_data = {
        'raw_text': text,
        'email': extract_email(text),
        'phone': extract_phone(text),
        'summary': extract_summary(text),
        'keywords': extract_keywords(text),
    }

    for key, headers in SECTION_HEADERS.items():
        if key not in parsed_data:  # skip summary already handled
            parsed_data[key] = extract_section(text, headers)

    return parsed_data


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r'((\+91[\-\s]*)|0)?\d{10}\b', text)
    return match.group(0) if match else None


def extract_section(text, section_names):
    lines = text.splitlines()
    section_text = []
    section_start = -1

    for i, line in enumerate(lines):
        for name in section_names:
            if re.match(rf'^\s*{re.escape(name)}\s*$', line.strip(), re.IGNORECASE):
                section_start = i
                break
        if section_start != -1:
            break

    if section_start == -1:
        return None

    for i in range(section_start + 1, len(lines)):
        if any(re.match(rf'^\s*{re.escape(name)}\s*$', lines[i].strip(), re.IGNORECASE)
               for name in sum(SECTION_HEADERS.values(), [])):
            break
        if lines[i].strip() == "":
            continue
        section_text.append(lines[i])

    return "\n".join(section_text).strip()


def extract_summary(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if any(header in line.lower() for header in SECTION_HEADERS['summary']):
            return "\n".join(lines[i + 1:i + 5]).strip()
    return "\n".join(lines[:5]).strip()  # fallback


def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {'with', 'this', 'that', 'from', 'have', 'your', 'will', 'work', 'team'}
    keywords = {word for word in words if word not in stopwords}
    return sorted(keywords)