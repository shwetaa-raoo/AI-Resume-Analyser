from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, Job, Resume, Application
from resume_parser import ResumeParser
from nlp_matcher import NLPMatcher
import json

app = Flask(__name__)

# Add custom filter for JSON parsing in templates
@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except:
        return []

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///resume_analyzer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc'}

db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/candidate')
def candidate_dashboard():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.posted_date.desc()).all()
    return render_template('candidate_dashboard.html', jobs=jobs)

@app.route('/company')
def company_dashboard():
    jobs = Job.query.order_by(Job.posted_date.desc()).all()
    return render_template('company_dashboard.html', jobs=jobs)

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form.get('title')
        company = request.form.get('company')
        location = request.form.get('location')
        description = request.form.get('description')
        required_skills = request.form.get('required_skills')
        experience = request.form.get('experience')
        salary_range = request.form.get('salary_range')
        
        if not all([title, company, description, required_skills]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('post_job'))
        
        job = Job(
            title=title,
            company=company,
            location=location,
            description=description,
            required_skills=required_skills,
            experience=experience,
            salary_range=salary_range
        )
        
        db.session.add(job)
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('company_dashboard'))
    
    return render_template('post_job.html')

@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', job=job)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if 'resume' not in request.files:
            flash('No resume file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['resume']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse resume
            parser = ResumeParser()
            resume_data = parser.parse_resume(filepath)
            
            # Save resume
            resume = Resume(
                filename=filename,
                filepath=filepath,
                name=name,
                email=email,
                phone=phone,
                skills=resume_data.get('skills', ''),
                education=resume_data.get('education', ''),
                experience=resume_data.get('experience', ''),
                raw_text=resume_data.get('raw_text', '')
            )
            db.session.add(resume)
            db.session.flush()
            
            # Perform NLP matching
            matcher = NLPMatcher()
            match_result = matcher.match_resume_to_job(resume_data, job)
            
            # Create application
            application = Application(
                job_id=job.id,
                resume_id=resume.id,
                match_score=match_result['score'],
                matched_skills=json.dumps(match_result['matched_skills']),
                missing_skills=json.dumps(match_result['missing_skills']),
                recommendations=json.dumps(match_result['recommendations'])
            )
            db.session.add(application)
            db.session.commit()
            
            # Store application ID in session for results page
            session['last_application_id'] = application.id
            
            flash('Resume submitted successfully!', 'success')
            return redirect(url_for('application_result', application_id=application.id))
        else:
            flash('Invalid file type. Please upload PDF or DOCX', 'error')
            return redirect(request.url)
    
    return render_template('apply_job.html', job=job)

@app.route('/application/<int:application_id>')
def application_result(application_id):
    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    resume = Resume.query.get(application.resume_id)
    
    matched_skills = json.loads(application.matched_skills)
    missing_skills = json.loads(application.missing_skills)
    recommendations = json.loads(application.recommendations)
    
    return render_template('application_result.html', 
                         application=application,
                         job=job,
                         resume=resume,
                         matched_skills=matched_skills,
                         missing_skills=missing_skills,
                         recommendations=recommendations)

@app.route('/job/<int:job_id>/applications')
def view_applications(job_id):
    job = Job.query.get_or_404(job_id)
    # Get all applications and sort by match score (highest first)
    applications = Application.query.filter_by(job_id=job_id)\
        .join(Resume)\
        .order_by(Application.match_score.desc()).all()
    
    # Calculate statistics
    stats = {
        'total': len(applications),
        'high_match': len([a for a in applications if a.match_score >= 70]),
        'avg_score': sum([a.match_score for a in applications]) / len(applications) if applications else 0
    }
    
    return render_template('view_applications.html', job=job, applications=applications, stats=stats)

@app.route('/toggle-job/<int:job_id>')
def toggle_job(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    db.session.commit()
    
    status = "activated" if job.is_active else "deactivated"
    flash(f'Job {status} successfully!', 'success')
    return redirect(url_for('company_dashboard'))

@app.route('/delete-job/<int:job_id>')
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Delete associated applications
    Application.query.filter_by(job_id=job_id).delete()
    
    db.session.delete(job)
    db.session.commit()
    
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('company_dashboard'))

@app.route('/application/<int:application_id>/update-status', methods=['POST'])
def update_application_status(application_id):
    application = Application.query.get_or_404(application_id)
    new_status = request.form.get('status')
    
    if new_status in ['Pending', 'Reviewed', 'Shortlisted', 'Rejected', 'Interview']:
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}!', 'success')
    else:
        flash('Invalid status', 'error')
    
    return redirect(url_for('view_applications', job_id=application.job_id))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded resume files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/jobs')
def api_jobs():
    """API endpoint to get all active jobs"""
    jobs = Job.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'required_skills': job.required_skills
    } for job in jobs])

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
