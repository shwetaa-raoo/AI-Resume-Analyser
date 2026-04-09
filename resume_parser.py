import PyPDF2
import docx
import re
import os

class ResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        # Common skills keywords
        self.skills_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 
            'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'sql', 'html', 
            'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
            'spring', 'hibernate', '.net', 'asp.net', 
            
            # Frameworks & Libraries
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 
            'opencv', 'nltk', 'spacy', 'fastapi', 'bootstrap', 'jquery', 'redux',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle',
            'sql server', 'cassandra', 'dynamodb', 'firebase',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
            'terraform', 'ansible', 'linux', 'bash', 'nginx', 'apache',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'nlp', 'computer vision', 
            'data analysis', 'data visualization', 'statistics', 'big data', 
            'hadoop', 'spark', 'tableau', 'power bi',
            
            # Other Skills
            'agile', 'scrum', 'rest api', 'graphql', 'microservices', 'testing',
            'junit', 'selenium', 'jira', 'confluence', 'project management',
            'communication', 'leadership', 'problem solving', 'teamwork'
        ]
        
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'diploma', 'degree', 'b.tech', 'm.tech',
            'mba', 'b.sc', 'm.sc', 'be', 'me', 'bca', 'mca', 'university', 'college',
            'education', 'qualification', 'certification'
        ]
        
        self.experience_keywords = [
            'experience', 'work history', 'employment', 'worked', 'working',
            'developer', 'engineer', 'manager', 'analyst', 'consultant', 'intern',
            'years', 'months', 'present', 'current'
        ]
    
    def parse_resume(self, file_path):
        """
        Parse resume and extract information
        Returns a dictionary with extracted data
        """
        try:
            # Read file content based on extension
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.pdf':
                text = self._extract_text_from_pdf(file_path)
            elif ext in ['.docx', '.doc']:
                text = self._extract_text_from_docx(file_path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            # Extract information
            result = {
                'raw_text': text,
                'email': self._extract_email(text),
                'phone': self._extract_phone(text),
                'skills': self._extract_skills(text),
                'education': self._extract_education(text),
                'experience': self._extract_experience(text)
            }
            
            return result
            
        except Exception as e:
            print(f"Error parsing resume: {str(e)}")
            return {
                'raw_text': '',
                'email': '',
                'phone': '',
                'skills': '',
                'education': '',
                'experience': ''
            }
    
    def _extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {str(e)}")
        return text
    
    def _extract_email(self, text):
        """Extract email address from text"""
        match = re.search(self.email_pattern, text)
        return match.group(0) if match else ""
    
    def _extract_phone(self, text):
        """Extract phone number from text"""
        match = re.search(self.phone_pattern, text)
        return match.group(0) if match else ""
    
    def _extract_skills(self, text):
        """Extract skills from text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skills_keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        # Remove duplicates and return as comma-separated string
        found_skills = list(set(found_skills))
        return ', '.join(found_skills)
    
    def _extract_education(self, text):
        """Extract education information"""
        lines = text.split('\n')
        education_section = []
        in_education_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if this line contains education keywords
            if any(keyword in line_lower for keyword in self.education_keywords):
                in_education_section = True
                education_section.append(line)
            elif in_education_section:
                # Continue adding lines until we hit another section
                if any(keyword in line_lower for keyword in self.experience_keywords + ['skills', 'projects']):
                    break
                if line.strip():
                    education_section.append(line)
                if len(education_section) > 10:  # Limit to 10 lines
                    break
        
        return '\n'.join(education_section[:10])
    
    def _extract_experience(self, text):
        """Extract experience information"""
        lines = text.split('\n')
        experience_section = []
        in_experience_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if this line contains experience keywords
            if any(keyword in line_lower for keyword in self.experience_keywords):
                in_experience_section = True
                experience_section.append(line)
            elif in_experience_section:
                # Continue adding lines until we hit another section
                if any(keyword in line_lower for keyword in self.education_keywords + ['skills', 'projects']):
                    break
                if line.strip():
                    experience_section.append(line)
                if len(experience_section) > 15:  # Limit to 15 lines
                    break
        
        return '\n'.join(experience_section[:15])
