import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letters(resume_data, matched_jobs):
    letters = []
    for job in matched_jobs:
        prompt = f"""
        Write a professional and concise cover letter for the following job:
        Job Title: {job['title']}
        Company: {job['company']}
        Job Summary: {job['summary']}
        Resume Content: {resume_data['raw_text'][:1000]}
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a career assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            job['cover_letter'] = response['choices'][0]['message']['content']
        except Exception as e:
            job['cover_letter'] = f"Failed to generate cover letter: {e}"
        letters.append(job)
    return letters
