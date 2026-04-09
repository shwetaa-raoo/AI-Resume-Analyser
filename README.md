# 🤖 AI-Powered Resume Analyzer

An intelligent resume analysis platform that uses Natural Language Processing (NLP) to match candidate resumes with job descriptions, providing detailed match scores and personalized recommendations.

## ✨ Features

### For Job Seekers
- 📄 **Resume Upload** - Support for PDF and DOCX formats
- 🎯 **Smart Matching** - AI-powered skill matching with job requirements
- 📊 **Match Score** - Get percentage match scores using TF-IDF and NLP
- 🔍 **Skill Analysis** - Identify matched and missing skills
- 💡 **Recommendations** - Personalized suggestions to improve your resume
- 📈 **Detailed Reports** - Comprehensive analysis breakdown

### For Companies
- 💼 **Job Posting** - Easy job posting with detailed requirements
- 👥 **Application Management** - View and manage all applications
- 🏆 **Ranked Candidates** - Automatic ranking by match score
- 📉 **Analytics** - Application statistics and insights
- ⚡ **Quick Screening** - Instantly identify top candidates

## 🛠️ Technology Stack

- **Backend:** Python, Flask
- **NLP/ML:** scikit-learn, NLTK, spaCy
- **Resume Parsing:** PyPDF2, python-docx
- **Database:** SQLAlchemy (SQLite)
- **Frontend:** HTML5, CSS3, JavaScript
- **Data Analysis:** pandas, numpy

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "resume analyzer"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (required for NLP)**
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. **Initialize the database**
   ```bash
   python app.py
   ```
   The database will be created automatically on first run.

## 💻 Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

3. **For Job Seekers:**
   - Click "Find Jobs" to browse available positions
   - Select a job and click "Apply Now"
   - Fill in your details and upload your resume (PDF/DOCX)
   - View your instant match score and analysis

4. **For Companies:**
   - Click "Company Portal" to access the dashboard
   - Click "Post New Job" to create a job listing
   - View applications ranked by match score
   - Review candidate profiles and match analysis

## 📁 Project Structure

```
resume analyzer/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── resume_parser.py        # Resume parsing logic
├── nlp_matcher.py          # NLP matching algorithms
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── candidate_dashboard.html
│   ├── company_dashboard.html
│   ├── post_job.html
│   ├── apply_job.html
│   ├── application_result.html
│   ├── job_details.html
│   └── view_applications.html
├── static/
│   └── css/
│       └── style.css      # Styling
├── uploads/               # Resume storage
└── README.md             # Documentation
```

## 🔧 Configuration

Key settings in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_analyzer.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
```

## 🧠 How It Works

### 1. Resume Parsing
- Extracts text from PDF/DOCX files
- Identifies key information (email, phone, skills, experience, education)
- Processes content using regex and text parsing

### 2. NLP Matching
- **TF-IDF Vectorization:** Converts resume and job description to numerical vectors
- **Cosine Similarity:** Calculates similarity between vectors
- **Skill Matching:** Exact and fuzzy matching of skills
- **Keyword Analysis:** Identifies important terms and their frequency

### 3. Scoring Algorithm
```
Final Score = (TF-IDF Score × 35%) + (Skill Match × 45%) + (Keyword Match × 20%)
```

### 4. Recommendations
- AI-generated suggestions based on match score
- Missing skills identification
- Resume improvement tips

## 📊 Match Score Interpretation

- **80-100%** - Excellent Match (Highly qualified)
- **60-79%** - Good Match (Strong candidate)
- **40-59%** - Moderate Match (Some qualifications)
- **0-39%** - Limited Match (Needs development)

## 🎨 Features Breakdown

### Resume Parser
- Multi-format support (PDF, DOCX, DOC)
- Automatic skill extraction (100+ predefined skills)
- Education and experience parsing
- Contact information extraction

### NLP Matcher
- TF-IDF vectorization with unigrams and bigrams
- Skill synonym matching
- Weighted scoring system
- Detailed breakdown analysis

### Web Interface
- Responsive design
- Modern UI with smooth animations
- Real-time file upload preview
- Interactive charts and visualizations

## 🔒 Security Features

- File type validation
- File size limits (16MB)
- Secure filename handling
- SQL injection protection via SQLAlchemy ORM

## 🚀 Future Enhancements

- [ ] User authentication system
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] LinkedIn integration
- [ ] Video interview scheduling
- [ ] Automated email responses
- [ ] Machine learning model training
- [ ] Resume template suggestions

## 🐛 Troubleshooting

**Issue: Package installation errors**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

**Issue: Database errors**
```bash
# Delete the database and reinitialize
rm resume_analyzer.db
python app.py
```

**Issue: File upload errors**
- Check file size (max 16MB)
- Ensure file format is PDF or DOCX
- Verify uploads folder exists

## 📝 License

This project is open-source and available for educational purposes.

## 👨‍💻 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Support

For questions or support, please open an issue in the repository.

## 🙏 Acknowledgments

- Flask framework
- scikit-learn for NLP capabilities
- PyPDF2 and python-docx for document parsing
- Font Awesome for icons

---

**Made with ❤️ using Python and NLP**

*Happy Job Hunting! 🎯*
