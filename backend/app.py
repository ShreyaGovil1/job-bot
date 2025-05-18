from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from job_scraper import scrape_indeed_jobs
from resume_parser import parse_resume
from matcher import match_jobs_with_resume
from letter_generator import generate_cover_letters

app = Flask(__name__)
CORS(app)

@app.route('/apply', methods=['POST'])
def apply_jobs():
    role = request.form.get('role')
    location = request.form.get('location')
    resume_file = request.files.get('resume')

    if not role or not location or not resume_file:
        return jsonify({'error': 'Missing parameters'}), 400

    resume_file = request.files['resume']
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    resume_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(resume_path)


    resume_data = parse_resume(resume_path)
    print("Parsed Resume Data:", resume_data)
    job_listings = scrape_indeed_jobs(role, location)
    print("Scraped Job Listings:", job_listings)
    matched_jobs = match_jobs_with_resume(resume_data, job_listings)
    results = generate_cover_letters(resume_data, matched_jobs)

    return jsonify(matched_jobs)

if __name__ == '__main__':
    app.run(debug=True)