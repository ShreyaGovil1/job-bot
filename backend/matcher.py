from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs_with_resume(resume_data, jobs):
    vectorizer = TfidfVectorizer(stop_words='english')
    resume_vec = vectorizer.fit_transform([resume_data['raw_text']])
    results = []
    for job in jobs:
        combined_text = f"{job['title']} {job['summary']}"
        job_vec = vectorizer.transform([combined_text])
        score = cosine_similarity(resume_vec, job_vec)[0][0]
        job['score'] = score
        results.append(job)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:5]
